include ecore.inc
PROVIDES += "virtual/ecore"
DEPENDS += "evas-x11"
PR = "r1"

EXTRA_OECONF = "--enable-ecore-fb \
		--enable-ecore-job \
		--enable-ecore-file \
		--enable-ecore-dbus \
		--enable-ecore-evas-fb \
		--enable-ecore-evas-x \
		--disable-ecore-evas-gl \
		--enable-ecore-con \
		--enable-ecore-ipc \
		--enable-ecore-txt \
		--enable-ecore-x \
		--enable-ecore-config \
		--disable-openssl \
		--x-includes=${STAGING_INCDIR}/X11 \
		--x-libraries=${STAGING_LIBDIR}	"

parts = "Ecore Ecore_Job Ecore_File Ecore_DBus \
	 Ecore_Txt Ecore_Fb Ecore_Con \
	 Ecore_Ipc Ecore_Evas Ecore_Config \
	 Ecore_X"
