SECTION = "base"
DESCRIPTION = "tslib is a touchscreen access library."
PV = "0.0cvs${CVSDATE}"
PR = "r29"

SRC_URI_OVERRIDES_PACKAGE_ARCH = "0"
PACKAGE_ARCH_tslib-conf = "${MACHINE}"
PACKAGE_ARCH_mnci = "${MACHINE}"

SRC_URI = "cvs://cvs:@pubcvs.arm.linux.org.uk/mnt/src/cvsroot;module=tslib \
	   file://ts.conf \
	   file://ts.conf-h3600 file://ts.conf-h3600-2.4 file://ts.conf-h2200 \
	   file://ts.conf-corgi file://ts.conf-corgi-2.4 \
	   file://tslib.sh"
SRC_URI_append_mnci += " file://devfs.patch;patch=1"
SRC_URI_append_mnci += " file://event1.patch;patch=1"
S = "${WORKDIR}/tslib"
LICENSE = "LGPL"
CONFFILES_${PN} = "${sysconfdir}/ts.conf"

inherit autotools

PACKAGES = "tslib-conf libts libts-dev tslib-tests tslib-calibrate"
EXTRA_OECONF        = "--enable-shared"
EXTRA_OECONF_mnci   = "--enable-shared --disable-h3600 --enable-input --disable-corgi --disable-collie --disable-mk712 --disable-arctic2 --disable-ucb1x00 "

do_stage () {
	oe_libinstall -so -C src libts-0.0 ${STAGING_LIBDIR}
	ln -sf libts-0.0.so ${STAGING_LIBDIR}/libts.so
	install -m 0644 src/tslib.h ${STAGING_INCDIR}/
	install -m 0644 src/tslib-private.h ${STAGING_INCDIR}/
}

do_install_prepend () {
	install -m 0644 ${WORKDIR}/ts.conf ${S}/etc/ts.conf
}

do_install_append() {
	install -d ${D}${sysconfdir}/profile.d/
	install -m 0755 ${WORKDIR}/tslib.sh ${D}${sysconfdir}/profile.d/
	case ${MACHINE} in
	h3600 | h3900 | h1940 | ipaq-pxa270)
		install -d ${D}${datadir}/tslib
		for f in ts.conf-h3600 ts.conf-h3600-2.4 ts.conf-h2200; do
			install -m 0644 ${WORKDIR}/$f ${D}${datadir}/tslib/
		done
		rm -f ${D}${sysconfdir}/ts.conf
		;;
	c7x0 | spitz | akita | tosa)
		install -d ${D}${datadir}/tslib
		for f in ts.conf-corgi ts.conf-corgi-2.4; do
			install -m 0644 ${WORKDIR}/$f ${D}${datadir}/tslib/
		done
		rm -f ${D}${sysconfdir}/ts.conf
		;;
	*)
		;;
	esac
}

RDEPENDS_libts = "tslib-conf"

FILES_tslib-conf = "${sysconfdir}/ts.conf ${sysconfdir}/profile.d/tslib.sh ${datadir}/tslib"
FILES_libts = "${libdir}/*.so.* ${libdir}/ts/*.so*"
FILES_libts-dev = "${FILES_tslib-dev}"
FILES_tslib-calibrate += "${bindir}/ts_calibrate"
FILES_tslib-tests = "${bindir}/ts_harvest ${bindir}/ts_print ${bindir}/ts_print_raw ${bindir}/ts_test"
