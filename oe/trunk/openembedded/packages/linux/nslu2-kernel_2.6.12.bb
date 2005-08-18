# Kernel for NSLU2
PR = "r3"
include nslu2-kernel.inc

# N2K_EXTRA_PATCHES - list of patches to apply (can include
#   patches to the files installed above)
# N2K_PATCHES - full list of patches to apply, defaults to:
#   file://nslu2_2.6.11.patch;patch=1
#   file://usbnet.patch;patch=1
#   file://ixp4xx_copy_from.patch;patch=1
#   ${N2K_EXTRA_PATCHES}
#

N2K_PATCHES = "\
	file://nslu2-arch.patch;patch=1 \
	file://x1205-rtc.patch;patch=1 \
	file://ixp4xx-regs.patch;patch=1 \
	file://compile-switches.patch;patch=1 \
	file://ixp4xx_copy_from.patch;patch=1 \
	file://anonymiser.patch;patch=1 \
	file://xscale-reset.patch;patch=1 \
	file://x1205-rtc.c-id.patch;patch=1 \
	file://mtd-shutdown.patch;patch=1 \
	file://timer.patch;patch=1 \
"
