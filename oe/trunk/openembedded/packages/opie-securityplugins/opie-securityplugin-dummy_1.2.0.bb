DESCRIPTION = "Dummy plugin for opie-security authentication. \
This is a very simple authentication plugin (you just have \
to press a button basically), for demonstration purpose."
SECTION = "opie/security"
PRIORITY = "optional"
MAINTAINER = "Team Opie <opie@handhelds.org>"
LICENSE = "GPL"
I18N_FILES = "libmultiauthdummyplugin.ts"
RDEPENDS = "opie-security"

APPNAME = "multiauthdummyplugin"


SRC_URI = "${HANDHELDS_CVS};tag=${TAG};module=opie/noncore/securityplugins/dummy \
           ${HANDHELDS_CVS};tag=${TAG};module=opie/pics "

S = "${WORKDIR}/dummy"

inherit opie

# FILES plugins/security/libmultiauthdummyplugin.so* pics/security/dummyplugin.png
do_install() {
        install -d ${D}${palmtopdir}/pics/security
        install -m 0644 ${WORKDIR}/pics/security/dummyplugin.png ${D}${palmtopdir}/pics/security/
}

