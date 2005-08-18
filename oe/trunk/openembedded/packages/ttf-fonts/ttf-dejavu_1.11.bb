DESCRIPTION = "DejaVu font - TTF Edition"
LICENSE = "Bitstream Vera"
HOMEPAGE = "http://dejavu.sourceforge.net/wiki/index.php/Main_Page"

SRC_URI = "${SOURCEFORGE_MIRROR}/dejavu/dejavu-ttf-${PV}.tar.gz"

include ttf.inc

S = "${WORKDIR}/dejavu-ttf-${PV}"

PACKAGES = "ttf-dejavu-sans ttf-dejavu-sans-mono ttf-dejavu-sans-condensed \
	    ttf-dejavu-serif ttf-dejavu-serif-condensed"

FILES_ttf-dejavu-sans = "${datadir}/fonts/truetype/DejaVuSans.ttf ${datadir}/fonts/truetype/DejaVuSans-*.ttf"
FILES_ttf-dejavu-sans-mono = "${datadir}/fonts/truetype/DejaVuSansMono.ttf ${datadir}/fonts/truetype/DejaVuSansMono-*.ttf"
FILES_ttf-dejavu-sans-condensed = "${datadir}/fonts/truetype/DejaVuSansCondensed.ttf ${datadir}/fonts/truetype/DejaVuSansCondensed-*.ttf"
FILES_ttf-dejavu-serif = "${datadir}/fonts/truetype/DejaVuSerif.ttf ${datadir}/fonts/truetype/DejaVuSerif-*.ttf"
FILES_ttf-dejavu-serif-condensed = "${datadir}/fonts/truetype/DejaVuSerifCondensed.ttf ${datadir}/fonts/truetype/DejaVuSerifCondensed-*.ttf"
