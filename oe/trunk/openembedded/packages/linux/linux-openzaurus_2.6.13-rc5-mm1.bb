DESCRIPTION = "2.6 Linux Development Kernel for Zaurus devices and iPAQ hx2750."
SECTION = "kernel"
MAINTAINER = "Richard Purdie <rpurdie@rpsys.net>, Michael 'Mickey' Lauer <mickey@vanille.de>"
LICENSE = "GPL"
#KV = "${@bb.data.getVar('PV',d,True).split('-')[0]}"
KV = "${@bb.data.getVar('PV',d,True)}"

PR = "r8"

DOSRC = "http://www.do13.in-berlin.de/openzaurus/patches"
RPSRC = "http://www.rpsys.net/openzaurus/patches"
JLSRC = "http://www.cs.wisc.edu/~lenz/zaurus/files"
BASRC = "http://www.orca.cx/zaurus/patches"

# Handy URLs
# http://www.kernel.org/pub/linux/kernel/people/alan/linux-2.6/2.6.10/patch-2.6.10-ac8.gz;patch=1 \
# ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing/patch-2.6.11-rc5.bz2;patch=1 \
# http://www.kernel.org/pub/linux/kernel/v2.6/snapshots/patch-2.6.12-rc4-git1.bz2;patch=1 \
# ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing/patch-2.6.12-rc6.bz2;patch=1 \

#           ${RPSRC}/rmk_devbuff-r0.patch;patch=1 \
#           ${RPSRC}/corgi_tspmu-r2.patch;patch=1 \
#           ${RPSRC}/w100_core-r1.patch;patch=1 \
#           ${RPSRC}/w100_corgi-r1.patch;patch=1 \
#           ${RPSRC}/corgikbd_compilefix-r0.patch;patch=1 \
#           ${RPSRC}/corgikbd_pm-r0.patch;patch=1 \
#           ${RPSRC}/corgikbd_tidyup-r0.patch;patch=1 \
#           ${RPSRC}/corgikbd_switch-r0.patch;patch=1 \
#           ${RPSRC}/corgikbd_temphack-r0.patch;patch=1 \
#           ${RPSRC}/2.6.13-rc3-mm3_fix-r0.patch;patch=1 \
#           ${RPSRC}/mmc_sd-r5.patch;patch=1 \
#           ${RPSRC}/preempt_nwfpe-r2.patch;patch=1 \
#           ${RPSRC}/oprofile_typo-r0.patch;patch=1 \
#           ${RPSRC}/mmc_bytefix-r0.patch;patch=1 \
#           ${RPSRC}/mmc_pxa_roswitch-r0.patch;patch=1 \
#           ${RPSRC}/mmc_corgi_roswitch-r0.patch;patch=1 \
#           ${RPSRC}/corgi_base_extras1-r4.patch;patch=1 \	   


# Patches submitted upstream are towards top of this list 
SRC_URI = "ftp://ftp.kernel.org/pub/linux/kernel/v2.6/linux-2.6.12.tar.gz \
           ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing/patch-2.6.13-rc5.bz2;patch=1 \
           ftp://ftp.kernel.org/pub/linux/kernel/people/akpm/patches/2.6/2.6.13-rc5/2.6.13-rc5-mm1/2.6.13-rc5-mm1.bz2;patch=1 \
           ${RPSRC}/reverse_pagefault-r3.patch;patch=1 \
           ${RPSRC}/corgi_tspmufix-r0.patch;patch=1 \
           ${RPSRC}/nwfpe_x80-r0.patch;patch=1 \
           ${RPSRC}/pxa_rtc-r1.patch;patch=1 \
           ${RPSRC}/pxa_irda-r2.patch;patch=1 \
           ${RPSRC}/sharp_multi_pcmcia-r3.patch;patch=1 \
           ${RPSRC}/input_power-r2.patch;patch=1 \
           ${RPSRC}/corgi_irda-r2.patch;patch=1 \
           ${RPSRC}/corgi_base_extras4-r0.patch;patch=1 \
           ${RPSRC}/jffs2_longfilename-r0.patch;patch=1 \
           ${RPSRC}/corgi_power-r24.patch;patch=1 \
           ${RPSRC}/corgi_power1-r1.patch;patch=1 \
           ${DOSRC}/mmc-bulk-r0.patch;patch=1 \
           ${RPSRC}/mmc_timeout-r0.patch;patch=1 \	   
           ${RPSRC}/corgi_snd-r10.patch;patch=1 \
           ${DOSRC}/rmk-i2c-pxa-r0.patch;patch=1 \
           ${RPSRC}/spitz_mtd-r0.patch;patch=1 \
           ${RPSRC}/ipaq/hx2750_base-r20.patch;patch=1 \
           ${RPSRC}/ipaq/hx2750_bl-r1.patch;patch=1 \
           ${RPSRC}/ipaq/hx2750_pcmcia-r1.patch;patch=1 \
           ${RPSRC}/ipaq/pxa_keys-r2.patch;patch=1 \
           ${RPSRC}/ipaq/tsc2101-r7.patch;patch=1 \
           ${RPSRC}/ipaq/hx2750_test1-r2.patch;patch=1 \
           ${DOSRC}/tosa-detection-r0.patch;patch=1 \
           ${BASRC}/spitz-detection-r0.patch;patch=1 \
           ${DOSRC}/pxa2xx-ir-dma-r0.patch;patch=1 \
           ${DOSRC}/tc6393-device-r4.patch;patch=1 \
           ${DOSRC}/tc6393_nand-r6.patch;patch=1 \
           ${DOSRC}/tosa-machine-base-r6.patch;patch=1 \
           ${DOSRC}/tosa-keyboard-r6.patch;patch=1 \
           ${DOSRC}/tc6393fb-r6.patch;patch=1 \
           ${DOSRC}/tosa-power-r5.patch;patch=1 \
           ${DOSRC}/tosa-mmc-r3.patch;patch=1 \
           ${DOSRC}/tosa-udc-r3.patch;patch=1 \
           ${DOSRC}/tosa-irda-r2.patch;patch=1 \
           ${DOSRC}/tosa-lcd-r3.patch;patch=1 \
           ${DOSRC}/tosa-2.6.13-r1.patch;patch=1 \
           ${RPSRC}/temp/tosa-bl-r5.patch;patch=1 \
           ${RPSRC}/pxa27x_extraregs-r1.patch;patch=1 \
           ${RPSRC}/spitzbase-r3.patch;patch=1 \
           ${RPSRC}/spitzkbd-r0.patch;patch=1 \
           ${RPSRC}/spitzssp-r4.patch;patch=1 \
           ${RPSRC}/spitzbl-r1.patch;patch=1 \
           ${RPSRC}/spitzts-r1.patch;patch=1 \
           ${RPSRC}/spitzcf-r1.patch;patch=1 \
           ${RPSRC}/pcmcia_dev_ids-r0.patch;patch=1 \
           ${RPSRC}/pxa_cf_initorder_hack-r0.patch;patch=1 \
           ${RPSRC}/pxa_pcmcia_init-r0.patch;patch=1 \
           file://add-oz-release-string.patch;patch=1 \
           file://add-elpp-stuff.patch;patch=1 \
           file://pxa-serial-hack.patch;patch=1 \
           ${RPSRC}/jl1/pxa-linking-bug.patch;patch=1 \
           file://dtl1_cs-add-socket-revE.patch;patch=1 \
           file://defconfig-c7x0 \
           file://defconfig-ipaq-pxa-2.6 \
           file://defconfig-collie \
           file://defconfig-poodle \
           file://defconfig-spitz \
           file://defconfig-tosa "

#           ${JLSRC}/zaurus-local-2.6.11.diff.gz;patch=1 \
#           ${JLSRC}/zaurus-base-2.6.11.diff.gz;patch=1 \
#           ${JLSRC}/zaurus-leds-2.6.11.diff.gz;patch=1 \

SRC_URI_append_collie = "${RPSRC}/jl1/collie_keymap.patch;patch=1 "
SRC_URI_append_poodle = "${JLSRC}/zaurus-lcd-2.6.11.diff.gz;patch=1 \
                         ${RPSRC}/rpextra_poodle-r0.patch;patch=1 "
SRC_URI_append_tosa = "${DOSRC}/nand-readid-r1.patch;patch=1 \
		       ${DOSRC}/pxa-ac97-alsa-r1.patch;patch=1 \
		       ${DOSRC}/pxa-ac97-alsa-resume-r0.patch;patch=1 \
		       ${DOSRC}/ac97-bus-r0.patch;patch=1 \
		       ${DOSRC}/wm9712-ts-r2.patch;patch=1 \
                       ${DOSRC}/tosa-pxaac97-r1.patch;patch=1 \
        	       ${DOSRC}/tosa-bluetooth-r0.patch;patch=1 "

S = "${WORKDIR}/linux-2.6.12"

inherit kernel

##############################################################
# Compensate for sucky bootloader on all Sharp Zaurus models
#
FILES_kernel-image = ""
ALLOW_EMPTY = 1

EXTRA_OEMAKE = "OPENZAURUS_RELEASE=-${DISTRO_VERSION}"
COMPATIBLE_HOST = "arm.*-linux"

CMDLINE_CON = "console=ttyS0,115200n8 console=tty1 noinitrd"
CMDLINE_ROOT = "root=/dev/mtdblock2 rootfstype=jffs2 "
CMDLINE_ROOT_poodle = "root=/dev/mtdblock1 rootfstype=jffs2 "

##############################################################
# Configure memory/ramdisk split for collie
#
export mem = ${@bb.data.getVar("COLLIE_MEMORY_SIZE",d,1) or "32"}
export rd  = ${@bb.data.getVar("COLLIE_RAMDISK_SIZE",d,1) or "32"}

CMDLINE_MEM_collie = "mem=${mem}M"
CMDLINE = "${CMDLINE_CON} ${CMDLINE_ROOT} ${CMDLINE_MEM} debug"

###############################################################
# Enable or disable ELPP via local.conf - default is "no"
#
ENABLE_ELPP = ${@bb.data.getVar("OZ_KERNEL_ENABLE_ELPP",d,1) or "no"}

do_configure() {

	install -m 0644 ${WORKDIR}/defconfig-${MACHINE} ${S}/.config || die "No default configuration for ${MACHINE} available."

	if [ "${MACHINE}" == "collie" ]; then
		mempos=`echo "obase=16; $mem * 1024 * 1024" | bc`
		rdsize=`echo "$rd * 1024" | bc`
		total=`expr $mem + $rd`
		addr=`echo "obase=16; ibase=16; C0000000 + $mempos" | bc`
	 	if [ "$rd" == "0" ]
	 	then
		    echo "No RAMDISK"
			echo "# CONFIG_MTD_MTDRAM_SA1100 is not set" >> ${S}/.config
		else
		    echo "RAMDIR = $rdsize on $addr"
			echo "CONFIG_MTD_MTDRAM_SA1100=y"           >> ${S}/.config
			echo "CONFIG_MTDRAM_TOTAL_SIZE=$rdsize"     >> ${S}/.config
			echo "CONFIG_MTDRAM_ERASE_SIZE=1"           >> ${S}/.config
			echo "CONFIG_MTDRAM_ABS_POS=$addr"          >> ${S}/.config
		fi
	fi

	echo "CONFIG_CMDLINE=\"${CMDLINE}\"" >> ${S}/.config

	if [ "${ENABLE_ELPP}" == "yes" ]; then
                echo "# Enhanced Linux Progress Patch"  >> ${S}/.config
                echo "CONFIG_FB_ELPP=y"                 >> ${S}/.config
                echo "CONFIG_LOGO=y"                    >> ${S}/.config
                echo "CONFIG_LOGO_LINUX_CLUT224=y"      >> ${S}/.config
	else
		echo "# CONFIG_FB_ELPP is not set"	>> ${S}/.config
	fi

	yes '' | oe_runmake oldconfig
}

# Check the kernel is below the 1272*1024 byte limit for the c7x0
do_compile_append() {
	if [ "${MACHINE}" == "c7x0" ]; then
		size=`ls arch/${ARCH}/boot/${KERNEL_IMAGETYPE} -s | cut -d ' ' -f 1`
		if [ $size -ge 1271 ]; then
			rm arch/${ARCH}/boot/${KERNEL_IMAGETYPE}
			die "This kernel is too big for the c7x0 and will destroy your machine if you flash it!!!"
		fi
	fi
}

do_deploy() {
        install -d ${DEPLOY_DIR}/images
        install -m 0644 arch/${ARCH}/boot/${KERNEL_IMAGETYPE} ${DEPLOY_DIR}/images/${KERNEL_IMAGETYPE}-${PV}-${MACHINE}-${DATETIME}.bin
}

do_deploy[dirs] = "${S}"

addtask deploy before do_build after do_compile
