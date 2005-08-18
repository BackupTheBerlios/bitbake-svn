DESCRIPTION = "library for easy implementation of a RDP/VNC server"
SECTION = "libs"
PRIORITY = "optional"
DEPENDS = "zlib jpeg"
LICENSE = "GPL"
PACKAGES = "libvncserver-storepasswd libvncserver-javaapplet"
FILES_libvncserver-storepasswd = "${bindir}/storepasswd"
FILES_libvncserver-javaapplet = "/${datadir}fbvncserver/classes/index.vnc \
			         /${datadir}fbvncserver/classes/VncViewer.jar"

SRC_URI = "${SOURCEFORGE_MIRROR}/libvncserver/LibVNCServer-${PV}.tar.gz"

CFLAGS_append = " -D_REENTRANT"
S = "${WORKDIR}/LibVNCServer-${PV}"

inherit autotools

do_stage () {
	install -d ${STAGING_INCDIR}/rfb
	install -m 0644 rfb/rfb.h rfb/rfbproto.h rfb/rfbint.h rfb/rfbconfig.h \
		    rfb/rfbclient.h rfb/rfbregion.h rfb/keysym.h \
		    rfb/default8x16.h ${STAGING_INCDIR}/rfb

	oe_libinstall -a -C libvncclient libvncclient ${STAGING_LIBDIR}/
	oe_libinstall -a libvncserver ${STAGING_LIBDIR}/
}

do_install () {
	install -d ${D}${bindir}
	install -m 0755 examples/storepasswd ${D}${bindir}
	install -d ${D}${datadir}fbvncserver/classes
	install -m 0644 classes/index.vnc ${D}${datadir}fbvncserver/classes/
	install -m 0644 classes/VncViewer.jar ${D}${datadir}fbvncserver/classes/
}
