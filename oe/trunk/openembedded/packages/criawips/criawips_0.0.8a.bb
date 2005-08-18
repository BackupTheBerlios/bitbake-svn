DESCRIPTION	= "Criawips is a presentantion manager"
LICENSE		= "GPL"
HOMEPAGE	= "http://www.nongnu.org/criawips/index.html"

DEPENDS		= "gtk+ libgsf gnome-vfs libgnomeui libglade libgnome"

SRC_URI		= "http://savannah.nongnu.org/download/criawips/criawips-${PV}.tar.gz"

inherit autotools pkgconfig
