DESCRIPTION = "A driver for wireless LAN cards based on Hermes(Orinoco) cards. \
Also contains support for cards using downloadable firmware, i.e. the Symbol/Socket family."
SECTION = "kernel/modules"
PRIORITY = "optional"
PROVIDES = "spectrum-modules"
MAINTAINER = "Michael 'Mickey' Lauer <mickey@Vanille.de>"
LICENSE = "GPL"
PR = "r0"

PARALLEL_MAKE = ""
EXTRA_OEMAKE = 'KERNEL_SRC="${KERNEL_STAGING_DIR}"'

# seems to cause problems on arm
DEFAULT_PREFERENCE_arm = "-1"

SRC_URI = "cvs://anoncvs:@savannah.gnu.org/cvsroot/orinoco;module=orinoco;method=ext;rsh=ssh \
           file://list-move.patch;patch=1 \
           file://spectrum-firmware.patch;patch=1 \
           file://spectrum.conf \
           file://spectrum_fw.h \
	   file://orinoco_cs.conf"
S = "${WORKDIR}/orinoco"

inherit module

do_compile_prepend() {
	install ${WORKDIR}/spectrum_fw.h ${S}/
}

do_install() {
	install -d ${D}${base_libdir}/modules/${KERNEL_VERSION}/net/
        install -d ${D}${sysconfdir}/pcmcia
	install -m 0644 *${KERNEL_OBJECT_SUFFIX} ${D}${base_libdir}/modules/${KERNEL_VERSION}/net/
        install -m 0644 ${WORKDIR}/spectrum.conf ${D}${sysconfdir}/pcmcia/
        install -m 0644 hermes.conf ${D}${sysconfdir}/pcmcia/
	install -d ${D}${sysconfdir}/modutils
	install -m 0644 ${WORKDIR}/orinoco_cs.conf ${D}${sysconfdir}/modutils/
}

PACKAGES = "orinoco-modules-cs orinoco-modules-pci orinoco-modules-usb orinoco-modules-nortel orinoco-modules"
FILES_orinoco-modules-cs = "/lib/modules/${KERNEL_VERSION}/net/*_cs${KERNEL_OBJECT_SUFFIX} /${sysconfdir}"
FILES_orinoco-modules-pci = "/lib/modules/${KERNEL_VERSION}/net/orinoco_p*${KERNEL_OBJECT_SUFFIX}"
FILES_orinoco-modules-usb = "/lib/modules/${KERNEL_VERSION}/net/*_usb${KERNEL_OBJECT_SUFFIX}"
FILES_orinoco-modules-nortel = "/lib/modules/${KERNEL_VERSION}/net/orinoco_tmd${KERNEL_OBJECT_SUFFIX} \
				/lib/modules/${KERNEL_VERSION}/net/orinoco_nortel${KERNEL_OBJECT_SUFFIX}"
FILES_orinoco-modules = "/lib/modules/"
RDEPENDS_orinoco-modules-cs = "orinoco-modules"
RDEPENDS_orinoco-modules-pci = "orinoco-modules"
RDEPENDS_orinoco-modules-usb = "orinoco-modules"
RDEPENDS_orinoco-modules-nortel = "orinoco-modules"
