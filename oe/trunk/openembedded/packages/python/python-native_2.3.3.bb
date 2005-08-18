DESCRIPTION = "Python Programming Language"
HOMEPAGE = "http://www.python.org"
LICENSE = "PSF"
SECTION = "devel/python"
PRIORITY = "optional"
MAINTAINER = "Michael 'Mickey' Lauer <mickey@Vanille.de>"
DEPENDS = ""
PR = "r1"

SRC_URI = "ftp://www.python.org/pub/python/${PV}/Python-${PV}.tar.bz2 \
           file://bindir-libdir.patch;patch=1             \
	   file://cross-distutils.patch;patch=1"
S = "${WORKDIR}/Python-${PV}"

inherit autotools native

EXTRA_OECONF = "--with-threads --with-pymalloc --with-cyclic-gc --without-cxx --with-signal-module --with-wctype-functions \
		--with-prefix=${STAGING_DIR} --with-exec-prefix=${STAGING_DIR}/${BUILD_SYS}"
EXTRA_OEMAKE = 'BUILD_SYS="" HOST_SYS=""'

do_configure () {
	oe_runconf
}

do_stage_append() {
	# install pgen for later usage with non-native builds
	install Parser/pgen ${STAGING_DIR}/${BUILD_SYS}/bin/
}

