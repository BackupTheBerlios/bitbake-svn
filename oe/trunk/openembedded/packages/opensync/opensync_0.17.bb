SRC_URI = "http://ewi546.ewi.utwente.nl/OE/source/libopensync-0.17.tar.gz"

LICENSE = "LGPL"
DEPENDS = "swig-native sqlite3 dbus"

inherit autotools pkgconfig

S = "${WORKDIR}/libopensync-${PV}"

EXTRA_OECONF = "--enable-engine --disable-python"

