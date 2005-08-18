include ecore.inc
PROVIDES += "virtual/ecore"
PR = "r0"

EXTRA_OECONF = "--enable-ecore-fb \
		--enable-ecore-job \
		--enable-ecore-file \
		--enable-poll \
		--enable-ecore-dbus \
		--enable-ecore-evas \
		--enable-ecore-evas-fb \
		--disable-ecore-evas-x \
		--disable-ecore-evas-gl \
		--enable-ecore-con \
		--enable-ecore-config \
		--enable-ecore-ipc \
		--enable-ecore-txt \
		--disable-ecore-x \
		--enable-ecore-config \
		--disable-openssl"

parts = "Ecore Ecore_Job Ecore_File Ecore_DBus \
	 Ecore_Txt Ecore_Fb Ecore_Con \
	 Ecore_Ipc Ecore_Evas Ecore_Config"
