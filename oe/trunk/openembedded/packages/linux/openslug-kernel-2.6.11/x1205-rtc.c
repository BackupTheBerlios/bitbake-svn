/*
    x1205 - an 12c driver for the Xicor X1205 RTC
    Copyright 2004 Karen Spearel

    please send all reports to:
	kas11 at tampabay dot rr dot com
      
    based on linux/drivers/acron/char/pcf8583.h
    Copyright (C) 2000 Russell King
    
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*/
/*

 * i2c_adapter is the structure used to identify a physical i2c bus along
 * with the access algorithms necessary to access it.

struct i2c_adapter {
	struct module *owner;
	unsigned int id;  == is algo->id | hwdep.struct->id, for registered values see below
	unsigned int class;
	struct i2c_algorithm *algo; the algorithm to access the bus
	void *algo_data;

	--- administration stuff.
	int (*client_register)(struct i2c_client *);
	int (*client_unregister)(struct i2c_client *);

	 data fields that are valid for all devices
	struct semaphore bus_lock;
	struct semaphore clist_lock;

	int timeout;
	int retries;
	struct device dev;		the adapter device 
	struct class_device class_dev;	the class device

#ifdef CONFIG_PROC_FS 
	No need to set this when you initialize the adapter
	int inode;
#endif def CONFIG_PROC_FS

	int nr;
	struct list_head clients;
	struct list_head list;
	char name[I2C_NAME_SIZE];
	struct completion dev_released;
	struct completion class_dev_released;
};
*/


/*========== Driver for the X1205 on the Linksys NSLU2 ==================*/

#include <linux/init.h>
#include <linux/i2c.h>
#include <linux/slab.h>
#include <linux/string.h>
#include <linux/errno.h>
#include <linux/bcd.h>
#include <linux/rtc.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>
#include <linux/miscdevice.h>
#include <linux/device.h>
#include <asm/uaccess.h>
#include <asm/system.h>
#include <linux/moduleparam.h>

#define		RTC_GETDATETIME		0
#define		RTC_SETTIME		1
#define		RTC_SETDATETIME		2

#define		I2C_M_WR		0	// just for consistancy

//  offsets into read buf - add 2 for write buf
#define		CCR_SEC			0
#define		CCR_MIN			1
#define		CCR_HOUR		2
#define		CCR_MDAY		3
#define		CCR_MONTH		4
#define		CCR_YEAR		5
#define		CCR_WDAY		6
#define		CCR_Y2K			7

#define		X1205_I2C_BUS_ADDR	0x6f	// hardwired into x1205
#define		X1205_ALM0_BASE		0x00	// Base address of the ALM0
#define		X1205_CCR_BASE		0x30	// Base address of the CCR
#define		X1205_SR_ADDR		0x3f	// Status Register
#define		X1205_SR_WEL		0x02	// Write Enable Latch bit
#define		X1205_SR_RWEL		0x04	// Register Write Enable Bit
#define		X1205_MILBIT		0x80	// this bit set in ccr.hour for 24 hr mode
#define		NOERR			0
#define		RTC_NODATE		0
#define		RTC_DATETOO		1

// comment out next line is your x1205 can't do page writes
//#define 	X1205PAGEWRITE		1
#ifdef X1205PAGEWRITE
#define		DRIVERNAME		"Xicor x1205 RTC Driver v0.9.3.3"
#else
#define		DRIVERNAME		"Xicor x1205 RTC Dvr v0.9.3.3NPW"
#endif

#define		DEBUG			KERN_DEBUG


static int x1205_get_datetime(struct i2c_client *client, struct rtc_time *tm, u8 reg_base);
static int x1205_set_datetime(struct i2c_client *client, struct rtc_time *tm, int datetoo, u8 reg_base);
static int x1205_attach(struct i2c_adapter *adapter);
static int x1205_detach(struct i2c_client *client);
static int x1205_validate_tm(struct rtc_time *tm);
static int x1205_command(struct i2c_client *client, unsigned int cmd, void *arg);
static int x1205_sync_rtc(void);
static int x1205_read(struct file *file, char *buf, size_t count, loff_t *ptr);
static int x1205_ioctl(struct inode *inode, struct file *file, unsigned int cmd, unsigned long arg);
static int x1205_read_proc(char *buf, char **start, off_t off, int len, int *eof, void *data);

static struct i2c_driver x1205_driver = {
	.owner		= THIS_MODULE,
	.name		= DRIVERNAME,
	.id		= I2C_DRIVERID_X1205,
	.flags		= I2C_DF_NOTIFY,
	.attach_adapter = &x1205_attach,		//we don't need to probe...x1205 is hardwired @ 0x6f
	.detach_client	= &x1205_detach,
	.command	= &x1205_command,		//this prolly never gets called...used internally tho
};

static struct i2c_client x1205_i2c_client = {
	.id		=	I2C_DRIVERID_X1205,
	.flags		=	0,
	.addr		=	X1205_I2C_BUS_ADDR,	// chip address - NOTE: 7bit
	.adapter	=	NULL,			// the adapter we sit on assigned in attach
	.driver		=	&x1205_driver,		// and our access routines
	.usage_count	=	0,			// How many accesses currently to this client
	.dev		=	{},			// the device structure
	.list		=	{},
	.name		=	DRIVERNAME,
	.released	=	{},
};

static struct file_operations rtc_fops = {
	owner:		THIS_MODULE,
	ioctl:		x1205_ioctl,
	read:		x1205_read,
};

static struct miscdevice x1205_miscdev = {
	.minor		= RTC_MINOR,
	.name		= "rtc",
	.fops		= &rtc_fops,
};
extern int (*set_rtc)(void);
static unsigned epoch = 1900;		//coresponds to year 0
static unsigned  rtc_epoch = 2000;
static const unsigned char days_in_mo[] = 
{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

//===================================CODE======================================
// in the routines that deal directly with the x1205 hardware, we use
// rtc_time -- month 0-11, hour 0-23, yr = calendar year-epoch
// Epoch is inited as 2000. Time is set to UT
//=============================================================================   
static int x1205_get_datetime(struct i2c_client *client, struct rtc_time *tm, u8 reg_base)
{
	static unsigned char addr[2] = { 0,} ;
	unsigned char buf[8];	
	struct i2c_msg msgs[2] = {
		{ client->addr, I2C_M_WR, 2, addr },	//msg 1 = send base address
		{ client->addr, I2C_M_RD, 8, buf },	//msg 2 = read sequential data
	};
	addr[1] = reg_base;
	if ((i2c_transfer(client->adapter, msgs, 2)) == 2) {	//did we read 2 messages?
		printk(KERN_DEBUG "raw x1205 read data  - sec-%02x min-%02x hr-%02x mday-%02x mon-%02x year-%02x wday-%02x y2k-%02x\n", 
			buf[0],buf[1],buf[2],buf[3],buf[4],buf[5],buf[6], buf[7]);
		tm->tm_sec  = BCD2BIN(buf[CCR_SEC]);
		tm->tm_min  = BCD2BIN(buf[CCR_MIN]);
		buf[CCR_HOUR] &= ~X1205_MILBIT;
		tm->tm_hour = BCD2BIN(buf[CCR_HOUR]);		//hr is 0-23
		tm->tm_mday = BCD2BIN(buf[CCR_MDAY]);
		tm->tm_mon  = BCD2BIN(buf[CCR_MONTH]);
		rtc_epoch   = BCD2BIN(buf[CCR_Y2K]) * 100;
		tm->tm_year = BCD2BIN(buf[CCR_YEAR]) + rtc_epoch - epoch;
		tm->tm_wday = buf[CCR_WDAY];
		printk(KERN_DEBUG "rtc_time output data - sec-%02d min-%02d hr-%02d mday-%02d mon-%02d year-%02d wday-%02d epoch-%d rtc_epoch-%d\n",
			tm->tm_sec,tm->tm_min,tm->tm_hour,tm->tm_mday,tm->tm_mon,tm->tm_year,tm->tm_wday,epoch, rtc_epoch);
	} else {
		printk(KERN_DEBUG "i2c_transfer Read Error\n");
		return -EIO;
	}		
	
	return NOERR;
}
// x1205pagewrite allows writing a block of registers in msg3 even though the x1205 says
// nothing about this in its spec. 
// it needs more testing as it is possible some x1205s are actually not-completely-
// functional x1226s and there is a reason for the multiple write to not be in the spec.
// anyhow, it is enabled for the time being...and we even push out luck by sending 10 bytes

static int x1205_set_datetime(struct i2c_client *client, struct rtc_time *tm, int datetoo, u8 reg_base)
{
	static unsigned char wel[3]   = { 0, X1205_SR_ADDR, X1205_SR_WEL };
	static unsigned char rwel[3]  = { 0, X1205_SR_ADDR, X1205_SR_WEL | X1205_SR_RWEL };
	static unsigned char diswe[3] = { 0, X1205_SR_ADDR, 0 };

#ifdef X1205PAGEWRITE

	static unsigned char buf[10]   = { 0, X1205_CCR_BASE, };		
	struct i2c_msg msgs[4] = {
		{ client->addr, I2C_M_WR, 3, wel   },	//msg 1 = write WEL to to ccr sr
		{ client->addr, I2C_M_WR, 3, rwel  },	//msg 2 = write RWEL to ccr sr
		{ client->addr, I2C_M_WR, 10, buf   },	//msg 3 = write ccr base addr +seq data
		{ client->addr, I2C_M_WR, 3, diswe },	//msg 4 = 0 to ccr sr to disable writes
	};

	msgs[2].len = 5;					// 5 bytes + addr to set time only
	buf [1] = reg_base;
	buf[CCR_SEC+2]  = BIN2BCD(tm->tm_sec);
	buf[CCR_MIN+2]  = BIN2BCD(tm->tm_min);
	buf[CCR_HOUR+2] = BIN2BCD(tm->tm_hour) | X1205_MILBIT; // set 24 hour format
	if (datetoo == 1) {
		buf[CCR_MDAY+2]  = BIN2BCD(tm->tm_mday);
		buf[CCR_MONTH+2] = BIN2BCD(tm->tm_mon);		// input is 0-11	
		buf[CCR_YEAR+2]  = BIN2BCD((tm->tm_year + epoch - rtc_epoch));	// input is yrs since 1900
		buf[CCR_WDAY+2]  = tm->tm_wday & 7;
		buf[CCR_Y2K+2]   = BIN2BCD((rtc_epoch/100));
		msgs[2].len += 5;				//5 more bytes to set date
	}
	printk(KERN_DEBUG "rtc_time input - sec-%02d min-%02d hour-%02d mday-%02d mon-%02d year-%02d wday-%02d epoch-%d rtc_epoch-%d\n",
		tm->tm_sec,tm->tm_min,tm->tm_hour,tm->tm_mday,tm->tm_mon,tm->tm_year,tm->tm_wday, epoch, rtc_epoch);
	printk(KERN_DEBUG "BCD write data - sec-%02x min-%02x hour-%02x mday-%02x mon-%02x year-%02x wday-%02x y2k-%02x\n",
		buf[2],buf[3],buf[4],buf[5],buf[6], buf[7], buf[8], buf[9]);

	if ((i2c_transfer(client->adapter, msgs, 4)) != 4)
		return -EIO;
	return NOERR;
	
#else		//do this if page writes aren't working

	int i,xfer;
	static unsigned char data[3]  = { 0,};
	static unsigned char buf[8];

	buf[CCR_SEC]  = BIN2BCD(tm->tm_sec);
	buf[CCR_MIN]  = BIN2BCD(tm->tm_min);
	buf[CCR_HOUR] = BIN2BCD(tm->tm_hour) | X1205_MILBIT; // set 24 hour format
	if (datetoo == 1) {
		buf[CCR_MDAY]  = BIN2BCD(tm->tm_mday);
		buf[CCR_MONTH] = BIN2BCD(tm->tm_mon);		// input is 0-11	
		buf[CCR_YEAR]  = BIN2BCD((tm->tm_year + epoch - rtc_epoch));	// input is yrs since 1900
		buf[CCR_WDAY]  = tm->tm_wday & 7;
		buf[CCR_Y2K]   = BIN2BCD((rtc_epoch/100));
	}
	printk(KERN_DEBUG "rtc_time input - sec-%02d min-%02d hour-%02d mday-%02d mon-%02d year-%02d wday-%02d epoch-%d rtc_epoch-%d\n",
		tm->tm_sec,tm->tm_min,tm->tm_hour,tm->tm_mday,tm->tm_mon,tm->tm_year,tm->tm_wday, epoch, rtc_epoch);

	xfer = i2c_master_send(client, wel, 3);
	printk(KERN_DEBUG "wen - %x\n", xfer);
	if (xfer != 3)
		return -EIO;

	xfer = i2c_master_send(client, rwel, 3);
	printk(KERN_DEBUG "wenb - %x\n", xfer);
	if (xfer != 3)
		return -EIO;

	for (i = 0; i < 8; i++) {
		data[1] = i + reg_base;
		data[2] =  buf[i];
		xfer = i2c_master_send(client, data, 3);
		printk(KERN_DEBUG "xfer - %d addr - %02x  data - %02x\n", xfer, data[1], data[2]);
		if (xfer != 3)
			return -EIO;
	};

	xfer = i2c_master_send(client, diswe, 3);
	printk(KERN_DEBUG "wdis - %x\n", xfer);
	if (xfer != 3)
		return -EIO;		
	return NOERR;
#endif
}
//=============================================================================

static int x1205_attach(struct i2c_adapter *adapter)
{
	struct rtc_time tm;
	struct timespec tv;
	int errno;
		
	x1205_i2c_client.adapter = adapter;
	x1205_i2c_client.id++;

	if ((x1205_get_datetime(&x1205_i2c_client, &tm, X1205_CCR_BASE)) != NOERR)	//test for functional driver 
		return -EIO;
	
	if ((errno = i2c_attach_client(&x1205_i2c_client)) != NOERR)
		return errno;

	tv.tv_nsec = tm.tm_sec * 10000000;
	tv.tv_sec  = mktime(tm.tm_year+epoch, tm.tm_mon, tm.tm_mday, tm.tm_hour,
						tm.tm_min, tm.tm_sec);
	do_settimeofday(&tv);
	set_rtc = x1205_sync_rtc;
	
	printk(KERN_DEBUG "%s attached on adapter %s\n",x1205_i2c_client.name,
		x1205_i2c_client.adapter->name); //why is this name a null string?

	return NOERR;
}

static int x1205_detach(struct i2c_client *client)
{
	int errno;
	
	if ((errno = i2c_detach_client(client)) != 0) {
		printk(KERN_DEBUG "i2c_detach failed - errno = %d\n", errno);
		return errno;
	}

	return NOERR;
}

// make sure the rtc_time values are in bounds
static int x1205_validate_tm(struct rtc_time *tm)
{
	tm->tm_year += 1900;

	if (tm->tm_year < 1970)
		return -EINVAL;

	if ((tm->tm_mon > 11) || (tm->tm_mday == 0))
		return -EINVAL;

	if (tm->tm_mday > (days_in_mo[tm->tm_mon] + ( (tm->tm_mon == 1) && 
		((!(tm->tm_year % 4) && (tm->tm_year % 100) ) || !(tm->tm_year % 400)))))
		return -EINVAL;

	if ((tm->tm_year -= epoch) > 255)
		return -EINVAL;
			
	if ((tm->tm_hour >= 24) || (tm->tm_min >= 60) || (tm->tm_sec >= 60))
		return -EINVAL;
	return NOERR;
}

static int x1205_command(struct i2c_client *client, unsigned int cmd, void *tm)
{
	int errno, dodate = RTC_DATETOO;

	if (client == NULL || tm == NULL)
		return -EINVAL;
	if (!capable(CAP_SYS_TIME))
		return -EACCES;

	printk(KERN_DEBUG "x1205_command %d\n", cmd);

	switch (cmd) {
	case RTC_GETDATETIME:
		return x1205_get_datetime(client, tm, X1205_CCR_BASE);

	case RTC_SETTIME:		// note fall thru
		dodate = RTC_NODATE;
	case RTC_SETDATETIME:
		if ((errno = x1205_validate_tm(tm)) < NOERR)
			return errno;
		return x1205_set_datetime(client, tm, dodate, X1205_CCR_BASE);

	default:
		return -EINVAL;
	}
}

static int x1205_sync_rtc(void)
{
	struct rtc_time new_tm, old_tm;
	unsigned long cur_secs = xtime.tv_sec;

	printk(KERN_DEBUG "x1205_sync_rtc entry\n");

	if (x1205_command(&x1205_i2c_client, RTC_GETDATETIME, &old_tm))
		return 0;

//	xtime.tv_nsec = old_tm.tm_sec * 10000000;   //FIXME:
	new_tm.tm_sec  = cur_secs % 60;
	cur_secs /= 60;
	new_tm.tm_min  = cur_secs % 60;
	cur_secs /= 60;
	new_tm.tm_hour = cur_secs % 24;

	/*
	 * avoid writing when we're going to change the day
	 * of the month.  We will retry in the next minute.
	 * This basically means that if the RTC must not drift
	 * by more than 1 minute in 11 minutes.
	 */
	if ((old_tm.tm_hour == 23 && old_tm.tm_min == 59) ||
	    (new_tm.tm_hour == 23 && new_tm.tm_min == 59))
		return 1;
	printk(KERN_DEBUG "x1205_sync_rtc exit\n");

	return x1205_command(&x1205_i2c_client, RTC_SETTIME, &new_tm);
}

static int x1205_read(struct file *file, char *buf, size_t count, loff_t *ptr)
{
	struct rtc_time tm;

	if ((x1205_get_datetime(&x1205_i2c_client, &tm, X1205_CCR_BASE)) < NOERR)
		return -EIO;
	return copy_to_user(buf, &tm, sizeof(tm)) ? -EFAULT : NOERR;
}

//==============================================================================

static int x1205_ioctl(struct inode *inode, struct file *file, unsigned int cmd,
		     unsigned long arg)
{
	struct rtc_time tm;
	int errno;

	printk(KERN_DEBUG "ioctl = %x\n", cmd);
	
	switch (cmd) {
	case RTC_RD_TIME:
		if ((x1205_get_datetime(&x1205_i2c_client, &tm, X1205_CCR_BASE)) < NOERR)
			return -EIO;
		break;
		
	case RTC_SET_TIME:
		if (!capable(CAP_SYS_TIME))
			return -EACCES;

		if (copy_from_user(&tm, (struct rtc_time *) arg, sizeof(struct rtc_time))) 
			return -EFAULT;
		if ((errno = x1205_validate_tm(&tm)) < NOERR)
			return errno;
		return x1205_set_datetime(&x1205_i2c_client, &tm, RTC_DATETOO, X1205_CCR_BASE);

	case RTC_ALM_SET:						//FIXME: set Control Regs
		if (copy_from_user(&tm, (struct rtc_time *) arg, sizeof(struct rtc_time))) 
			return -EFAULT;
		return x1205_set_datetime(&x1205_i2c_client, &tm, RTC_DATETOO, X1205_ALM0_BASE);

	case RTC_ALM_READ:
		if ((x1205_get_datetime(&x1205_i2c_client, &tm, X1205_ALM0_BASE)) < NOERR)
			return -EIO;
		break;

	case RTC_EPOCH_READ:

		return put_user (epoch, (unsigned long __user *)arg);

	case RTC_EPOCH_SET:
		if (arg < 1900)
			return -EINVAL;

		if (!capable(CAP_SYS_TIME))
			return -EACCES;

		epoch = arg;
		return 0;

	default:
		return -ENOTTY;
	}
	return copy_to_user((void __user *)arg, &tm, sizeof tm) ? -EFAULT : 0;

}

static int x1205_read_proc(char *buf, char **start, off_t off, int len, int *eof, void *data)
{
	struct rtc_time tm;
	int slen, errno;

	if ((errno = x1205_get_datetime(&x1205_i2c_client, &tm, X1205_CCR_BASE)) < NOERR)
		return errno;

//	here we return the real year and the month as 1-12 since it is human-readable
	slen = sprintf(buf, "rtc_time\t: %02d:%02d:%02d\nrtc_date\t: %04d-%02d-%02d\n",
		tm.tm_hour, tm.tm_min, tm.tm_sec, tm.tm_year + 1900, tm.tm_mon+1, tm.tm_mday);
 	printk(KERN_DEBUG "raw rtc_time\t: %02d:%02d:%02d\nraw rtc_date\t: %04d-%02d-%02d\n",
		tm.tm_hour, tm.tm_min, tm.tm_sec, tm.tm_year, tm.tm_mon, tm.tm_mday);

	if (slen <= off + len)
		*eof = 1;
	*start = buf + off;
	slen -= off;
	if (slen > len)
		slen = len;
	if ( slen < 0 )
		slen = 0;

	return slen;
}

static int __init x1205_init(void)
{
	struct	rtc_time tm;
	int errno;
	printk(KERN_INFO "LOADED %s\n", DRIVERNAME);

	if ((errno = i2c_add_driver(&x1205_driver)) != NOERR) {
		dev_dbg(x1205_i2c_client.dev, "x1205_init failed - errno = %d\n", errno);
		return (errno);
	}
	if ((errno = misc_register(&x1205_miscdev)) != NOERR) {
		dev_dbg(x1205_i2c_client.dev, "Register Misc Driver failed - errno = %d\n", errno);
		i2c_del_driver(&x1205_driver);
		return errno; 
	}
	if (create_proc_read_entry("driver/rtc", 0, NULL, x1205_read_proc, NULL) < NOERR)
		return -ENOMEM;
	if ((x1205_get_datetime(&x1205_i2c_client, &tm, X1205_CCR_BASE)) != NOERR)	//test for functionality
		return -EIO;

	return NOERR;	
}

static void __exit x1205_exit(void)
{
	remove_proc_entry("driver/rtc", NULL);
	misc_deregister(&x1205_miscdev);
	i2c_del_driver(&x1205_driver);
	set_rtc = NULL;
}

MODULE_AUTHOR("Karen Spearel <kas11@tampabay.rr.com>");
MODULE_DESCRIPTION("Xicor X1205-RTC Driver");
MODULE_LICENSE("GPL");
static int debug = 7;
module_param(debug, bool, 0644);
MODULE_PARM_DESC(debug, "Debugging enabled = 1");

module_init(x1205_init);
module_exit(x1205_exit);
