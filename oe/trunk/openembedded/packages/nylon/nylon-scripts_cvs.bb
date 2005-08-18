DESCRIPTION = "This package provides the nylon specific init and configuration scripts."
HOMEPAGE = "http://meshcube.org/meshwiki/NyLon"
DEPENDS = "hostap-utils"
SECTION = "base"
PRIORITY = "optional"
MAINTAINER = "Bruno Randolf <bruno.randolf@4g-systems.biz>"
LICENSE = "GPLv2"
PV = "cvs${CVSDATE}"

SRC_URI = "svn://meshcube.org/svn/scripts;module=${PN};proto=http"
S = "${WORKDIR}/${PN}"

do_install() {
	(cd ${S}; tar -c --exclude .svn -f - . ) | tar -C ${D} -xpf -
}

pkg_postinst() {
if test "x$D" != "x"; then
	exit 1
else
	update-rc.d -s hostap defaults 14
	update-rc.d -s bridge defaults 15
	update-rc.d -s ipaliases defaults 16
	update-rc.d -s firewall defaults 20
	update-rc.d -s routing defaults 20
	update-rc.d -s emergency-ip defaults 98
	update-rc.d -s flash-backup start 38 S . stop 38 0 6 .
	update-rc.d -s dummydate start 50 S . stop 50 0 6 .
	
	if ! grep -q flash-backup /etc/cron/crontabs/root; then
		echo "adding flash-backup crontab"
		test -d /etc/cron/crontabs || mkdir -p /etc/cron/crontabs
		echo "0 * * * *    /etc/init.d/flash-backup backup" >> /etc/cron/crontabs/root
	fi
	 
	if ! grep -q reset-wlan /etc/cron/crontabs/root; then
		echo "adding reset-wlan crontab"
		test -d /etc/cron/crontabs || mkdir -p /etc/cron/crontabs
		echo "0 3 * * *    /usr/sbin/reset-wlan" >> /etc/cron/crontabs/root
	fi

	update-rc.d -s busybox-cron defaults
fi
}

pkg_postrm() {
#!/bin/sh -e
update-rc.d hostap remove
update-rc.d bridge remove
update-rc.d ipaliases remove
update-rc.d firewall remove
update-rc.d routing remove
update-rc.d emergency-ip remove
update-rc.d flash-backup remove
update-rc.d dummydate remove
}

CONFFILES_${PN} = "/etc/nylon/backup.list /etc/nylon/bridge.conf /etc/nylon/configip.conf /etc/nylon/hostap.conf /etc/nylon/interfaces.conf /etc/nylon/macfilter.list /etc/nylon/route.list"
