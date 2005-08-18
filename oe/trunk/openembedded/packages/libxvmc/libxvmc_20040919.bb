DESCRIPTION = "X Video Motion Compensation extension library."
SECTION = "x11/libs"
DEPENDS = "x11 xext libxv drm xserver-xorg"
PR = "r2"

SRC_URI = "cvs://anoncvs@cvs.freedesktop.org/cvs/xlibs;module=XvMC;date=${PV};method=pserver \
	cvs://anonymous@cvs.sourceforge.net/cvsroot/unichrome;module=libxvmc;date=${PV};method=pserver \
	file://via.patch;patch=1 \
	file://true.patch"
S = "${WORKDIR}/XvMC"

CFLAGS += "-I${STAGING_INCDIR}/X11/extensions -I${STAGING_INCDIR}/xserver-xorg"

# this one is for via only atm.
COMPATIBLE_HOST = 'i.86.*-linux'

inherit autotools pkgconfig 

do_configure_prepend() {
	install -d ${S}/hw/via
	cp ${WORKDIR}/libxvmc/*.[ch] ${S}/hw/via/
	( cd ${S}/hw/via ; patch < ${WORKDIR}/true.patch )
}

do_compile() {
	oe_runmake
	oe_runmake -C hw/via
}

do_stage() {
	oe_runmake install prefix=${STAGING_DIR} \
	       bindir=${STAGING_BINDIR} \
	       includedir=${STAGING_INCDIR} \
	       libdir=${STAGING_LIBDIR} \
	       datadir=${STAGING_DATADIR} \
	       mandir=${STAGING_DATADIR}/man
	oe_libinstall -so -C hw/via libviaXvMC ${STAGING_LIBDIR}
	install hw/via/vldXvMC.h ${STAGING_INCDIR}/X11/extensions/
}
