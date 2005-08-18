LICENSE = "LGPL"
SECTION = "x11/libs"
DEPENDS = "glib-2.0 fontconfig freetype zlib x11 libxft xt"
DESCRIPTION = "The goal of the Pango project is to provide an \
Open Source framework for the layout and rendering of \
internationalized text."

SRC_URI = "http://ftp.gnome.org/pub/gnome/sources/pango/1.2/pango-${PV}.tar.bz2 \
	   file://ft2.patch;patch=1 \
	   file://m4.patch;patch=1 \
	   file://no-tests.patch;patch=1"

inherit autotools  pkgconfig

EXTRA_OECONF = "--disable-glibtest \
		--enable-explicit-deps=no"

FILES_${PN} = "/etc ${bindir} ${libdir}/libpango*.so.*"

LIBV = "1.2.0"

do_stage () {
	for lib in pango pangox pangoft2 pangoxft; do
		oe_libinstall -so -C pango lib$lib-1.0 ${STAGING_LIBDIR}/
	done
	install -d ${STAGING_INCDIR}/pango
	install -m 0644 ${S}/pango/pango*.h ${STAGING_INCDIR}/pango/
}

python populate_packages_prepend () {
	modules_root = bb.data.expand('${libdir}/pango/${LIBV}/modules', d)

	do_split_packages(d, modules_root, '^pango-(.*)\.so$', 'pango-module-%s', 'Pango module %s', 'pango-querymodules > /etc/pango/pango.modules')
}
