include ${PN}.inc

PV      = "1.2.0+cvs-${CVSDATE}"
SRC_URI = "${HANDHELDS_CVS};module=opie/development/translation/opie-lupdate \
           ${HANDHELDS_CVS};module=opie/development/translation/shared"
