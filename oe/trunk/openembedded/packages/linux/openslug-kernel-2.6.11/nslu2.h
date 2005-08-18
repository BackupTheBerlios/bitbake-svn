/*
 * include/asm-arm/arch-ixp4xx/nslu2.h
 *
 * NSLU2 platform specific definitions
 *
 * Author: Mark Rakes <mrakes AT mac.com>
 * Maintainers: http://www.nslu2-linux.org
 *
 * based on ixdp425.h:
 *	Copyright 2004 (c) MontaVista, Software, Inc.
 *
 * This file is licensed under  the terms of the GNU General Public
 * License version 2. This program is licensed "as is" without any
 * warranty of any kind, whether express or implied.
 */

// GPIO 8 is used as the power input so is not free for use as a PCI IRQ
// kas11 11-2-04

#ifndef __ASM_ARCH_HARDWARE_H__
#error "Do not include this directly, instead #include <asm/hardware.h>"
#endif

#define	NSLU2_FLASH_BASE	IXP4XX_EXP_BUS_CS0_BASE_PHYS
#define	NSLU2_FLASH_SIZE	IXP4XX_EXP_BUS_CSX_REGION_SIZE

#define	NSLU2_SDA_PIN		7
#define	NSLU2_SCL_PIN		6

/*
 * NSLU2 PCI IRQs
 */
#define NSLU2_PCI_MAX_DEV	3
#define NSLU2_PCI_IRQ_LINES	3


/* PCI controller GPIO to IRQ pin mappings */
#define NSLU2_PCI_INTA_PIN	11
#define NSLU2_PCI_INTB_PIN	10
#define	NSLU2_PCI_INTC_PIN	9
//#define	NSLU2_PCI_INTD_PIN	8


