DESCRIPTION	= "Multisync is a GUI for OpenSync"
LICENSE		= "GPL"
HOMEPAGE	= "http://www.opensync.org"

DEPENDS		= "gtk+ opensync"
RRECOMMENDS	= ""
SRC_URI		= "http://ewi546.ewi.utwente.nl/OE/source/multisync-${PV}.tar.gz"

inherit autotools pkgconfig

