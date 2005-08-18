LICENSE = "LGPL"
DESCRIPTION = "C++ bindings for the GTK+ toolkit."
HOMEPAGE = "http://www.gtkmm.org/"
SECTION = "libs"
PRIORITY = "optional"
MAINTAINER = "Johan Bilien <jobi@via.ecp.fr>"
DEPENDS = "glibmm"
PR = "r0"

SRC_URI = "ftp://ftp.gnome.org/pub/GNOME/sources/gtkmm/2.6/gtkmm-${PV}.tar.bz2"

inherit autotools pkgconfig flow-lossage

FILES_${PN} = "${libdir}/lib*.so.*"


LIBV = "2.6.2"

do_stage () {
	oe_libinstall -so -C atk/atkmm libatkmm-1.6 ${STAGING_LIBDIR}
	oe_libinstall -so -C pango/pangomm libpangomm-1.4 ${STAGING_LIBDIR}
	oe_libinstall -so -C gdk/gdkmm libgdkmm-2.6 ${STAGING_LIBDIR}
	oe_libinstall -so -C gtk/gtkmm libgtkmm-2.6 ${STAGING_LIBDIR}

	autotools_stage_includes

	install -m 0644 gdk/gdkmmconfig.h ${STAGING_INCDIR}/gtkmm-2.6
	install -m 0644 gtk/gtkmmconfig.h ${STAGING_INCDIR}/gtkmm-2.6
}
