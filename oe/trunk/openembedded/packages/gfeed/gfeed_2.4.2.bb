DESCRIPTION 	= "RSS reader"
HOMEPAGE 	= "http://sourceforge.net/projects/gfeed"
LICENSE		= "GPL"

SRC_URI 	= "${SOURCEFORGE_MIRROR}/gfeed/gfeed-${PV}.tar.gz"
DEPENDS 	= "libxml gnet"

inherit autotools
