DESCRIPTION = "Engage is the E17 icon dock"
DEPENDS = "evas-x11 ecore-x11 esmart imlib2-x11 edje ewl e"
LICENSE = "MIT"
SECTION = "e/apps"
MAINTAINER = "Justin Patrin <papercrane@reversefold.com>"
PR = "r1"

SRC_URI = "cvs://anonymous@cvs.sourceforge.net/cvsroot/enlightenment;module=misc/engage \
           file://no-local-includes.patch;patch=1"
S = "${WORKDIR}/engage"

inherit autotools pkgconfig binconfig

EXTRA_OECONF = "--with-edje-cc=${STAGING_BINDIR}/edje_cc"

do_prepsources () {
  make clean distclean || true
}
addtask prepsources after do_fetch before do_unpack

FILES_${PN} = "${bindir}/* ${libdir}/* ${datadir} ${sysconfdir} ${sbindir}"

