PV = "0.0cvs${CVSDATE}"
LICENSE = "MIT"
DEPENDS = "x11 xext"
DESCRIPTION = "X display information utility"
MAINTAINER = "Phil Blundell <pb@handhelds.org>"
SECTION = "x11/base"

SRC_URI = "cvs://anoncvs:anoncvs@pdx.freedesktop.org/cvs/xapps;module=xdpyinfo"
S = "${WORKDIR}/xdpyinfo"

inherit autotools pkgconfig 
