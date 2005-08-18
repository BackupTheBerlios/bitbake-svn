LICENSE = "GPL"
SECTION = "x11/utils"
PR = "r0"
S = "${WORKDIR}/gnumeric-${PV}"
DEPENDS = "libgsf gtk+ libxml2 goffice libglade libart-lgpl intltool-native libgnomecanvas libgnomeprint libgnomeprintui"
DESCRIPTION = "Gnumeric spreadsheet for GNOME"

inherit gnome flow-lossage

SRC_URI += "file://remove-docs.patch;patch=1"

EXTRA_OECONF=" --without-perl "

python populate_packages_prepend () {
	gnumeric_libdir = bb.data.expand('${libdir}/gnumeric/${PV}/plugins', d)

	do_split_packages(d, gnumeric_libdir, '(.*)', 'gnumeric-plugin-%s', 'Gnumeric plugin for %s', allow_dirs=True)
}
