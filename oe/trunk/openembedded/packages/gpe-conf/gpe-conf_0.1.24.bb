PACKAGES = "gpe-conf gpe-conf-panel"
LICENSE = "GPL"
SECTION = "gpe"
PRIORITY = "optional"

inherit gpe
PR="r0"

DEPENDS = "gtk+ libgpewidget libxsettings libxsettings-client pcmcia-cs xst xset ipaq-sleep ntp gpe-login gpe-icons"
RDEPENDS_${PN} = "xst xset ipaq-sleep ntpdate gpe-login gpe-icons"
RDEPENDS_gpe-conf-panel = "gpe-conf"
FILES_${PN} = "${sysconfdir} ${bindir} ${datadir}/pixmaps \
		${datadir}/applications/gpe-conf-* ${datadir}/gpe/pixmaps \
		${datadir}/gpe-conf"
FILES_gpe-conf-panel = "${datadir}/applications/gpe-conf.desktop"

do_compile () {
	oe_runmake PREFIX=${prefix}
	oe_runmake all-desktop PREFIX=${prefix}
}

do_install () {
        oe_runmake PREFIX=${prefix} DESTDIR=${D} install-program
}


