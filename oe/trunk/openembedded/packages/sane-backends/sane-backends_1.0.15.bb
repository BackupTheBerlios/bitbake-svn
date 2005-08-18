MAINTAINER = "Oyvind Repvik <nail@nslu2-linux.org>"
DESCRIPTION = "Scanner drivers for SANE"
PR = "r4"
DEPENDS = "jpeg libusb"
LICENCE = "LGPL"

SRC_URI = "ftp://ftp.sane-project.org/pub/sane/sane-backends-${PV}/sane-backends-${PV}.tar.gz \
	file://sane-plustek.patch;patch=1 \
	file://Makefile.in.patch;patch=1 \
	file://saned.xinetd \
	"
	
EXTRA_OECONF = "--disable-translations"

inherit autotools

do_install_append() {
	install -d "${D}/${sysconfdir}/xinetd.d"
	install -m 755 "${S}/tools/.libs/sane-find-scanner" "${D}/${bindir}"
	install -m 644 "${WORKDIR}/saned.xinetd" "${D}/${sysconfdir}/xinetd.d/saned"
}

PACKAGES = "libsane saned sane-utils"

FILES_libsane = "/usr/lib/sane/*.so.* /usr/lib/lib*.so.* /etc"
PKG_libsane = "libsane"
RCONFLICTS = "sane-backends"
RRECOMMENDS_libsane = "saned sane-utils"

RDEPENDS_saned = "libsane"
RRECOMMENDS_saned = "xinetd"
FILES_saned = "/usr/sbin/saned"

RDEPENDS_sane-utils = "libsane"
FILES_sane-utils = "/usr/bin"

CONFFILES_libsane = "${sysconfdir}/sane.d/abaton.conf ${sysconfdir}/sane.d/agfafocus.conf ${sysconfdir}/sane.d/apple.conf ${sysconfdir}/sane.d/artec.conf ${sysconfdir}/sane.d/avision.conf ${sysconfdir}/sane.d/bh.conf ${sysconfdir}/sane.d/canon.conf ${sysconfdir}/sane.d/canon630u.conf ${sysconfdir}/sane.d/coolscan.conf ${sysconfdir}/sane.d/coolscan2.conf ${sysconfdir}/sane.d/dc25.conf ${sysconfdir}/sane.d/dmc.conf ${sysconfdir}/sane.d/epson.conf ${sysconfdir}/sane.d/fujitsu.conf ${sysconfdir}/sane.d/gt68xx.conf ${sysconfdir}/sane.d/hp.conf  ${sysconfdir}/sane.d/leo.conf ${sysconfdir}/sane.d/matsushita.conf ${sysconfdir}/sane.d/microtek.conf ${sysconfdir}/sane.d/microtek2.conf ${sysconfdir}/sane.d/mustek.conf ${sysconfdir}/sane.d/mustek_usb.conf ${sysconfdir}/sane.d/nec.conf ${sysconfdir}/sane.d/pie.conf ${sysconfdir}/sane.d/plustek.conf ${sysconfdir}/sane.d/plustek_pp.conf ${sysconfdir}/sane.d/ricoh.conf ${sysconfdir}/sane.d/s9036.conf ${sysconfdir}/sane.d/sceptre.conf ${sysconfdir}/sane.d/sharp.conf ${sysconfdir}/sane.d/sp15c.conf ${sysconfdir}/sane.d/st400.conf ${sysconfdir}/sane.d/tamarack.conf ${sysconfdir}/sane.d/test.conf ${sysconfdir}/sane.d/teco1.conf ${sysconfdir}/sane.d/teco2.conf ${sysconfdir}/sane.d/teco3.conf ${sysconfdir}/sane.d/umax.conf ${sysconfdir}/sane.d/umax_pp.conf ${sysconfdir}/sane.d/umax1220u.conf ${sysconfdir}/sane.d/artec_eplus48u.conf ${sysconfdir}/sane.d/ma1509.conf ${sysconfdir}/sane.d/ibm.conf ${sysconfdir}/sane.d/hp5400.conf ${sysconfdir}/sane.d/u12.conf ${sysconfdir}/sane.d/snapscan.conf ${sysconfdir}/sane.d/dc210.conf ${sysconfdir}/sane.d/dc240.conf ${sysconfdir}/sane.d/gphoto2.conf ${sysconfdir}/sane.d/qcam.conf ${sysconfdir}/sane.d/v4l.conf ${sysconfdir}/sane.d/net.conf ${sysconfdir}/sane.d/dll.conf ${sysconfdir}/sane.d/saned.conf"

