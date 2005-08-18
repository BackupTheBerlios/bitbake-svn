PV = "1.1.5+cvs${CVSDATE}"
DEFAULT_PREFERENCE = "-1"
PR = "r2"

SRC_URI = "cvs://readonly:readonly@cvs.kaffe.org/cvs/kaffe;module=kaffe"
S = "${WORKDIR}/kaffe"

include kaffe.inc

inherit native

EXTRA_OECONF = "--disable-alsatest \
	--disable-esdtest \
	--disable-sound \
	--with-jikes \
	--without-classpath-gtk-awt \
	--without-gmp \
	--enable-pure-java-math \
	--disable-native-awt \
	--disable-sound \
	--without-x \
	--without-kaffe-x-awt \
	--disable-debug \
	--disable-gcj"

do_stage() {
	install -m 0755 kaffe/kaffeh/kaffeh ${STAGING_BINDIR}/
}
