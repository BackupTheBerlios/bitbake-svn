m4_include([config/version.m4])
AC_INIT(bitbake-ng, LIBFOO_PKGVER, kergoth@handhelds.org)
AC_PREREQ(2.59)

AC_CONFIG_SRCDIR([src/main.c])
AC_CONFIG_AUX_DIR(config)
AM_CONFIG_HEADER([config.h])

AM_INIT_AUTOMAKE

PACKAGE_LTRELEASE=LIBFOO_RELVER
AC_SUBST([PACKAGE_LTRELEASE])

PACKAGE_LTCUR=LIBFOO_LT_CUR
AC_SUBST([PACKAGE_LTCUR])

PACKAGE_LTREV=LIBFOO_LT_REV
AC_SUBST([PACKAGE_LTREV])

PACKAGE_LTVERSION="\$(PACKAGE_LTCUR):\$(PACKAGE_LTREV)"
AC_SUBST([PACKAGE_LTVERSION])


# paths
auxdir="\$(top_srcdir)/$ac_aux_dir"
AC_SUBST(auxdir)

reldatadir="\$(datadir)/bitbake-ng-\$(PACKAGE_LTRELEASE)"
rellibdir="\$(libdir)/bitbake-ng-\$(PACKAGE_LTRELEASE).\$(PACKAGE_LTCUR)"
relincludedir="\$(includedir)/bitbake-ng-\$(PACKAGE_LTRELEASE)"
AC_SUBST([reldatadir])
AC_SUBST([rellibdir])
AC_SUBST([relincludedir])


# programs
AC_PROG_CC

AC_PROG_LIBTOOL
AC_SUBST(LIBTOOL_DEPS)


# other
AM_BINRELOC

AC_CONFIG_FILES([Makefile
                 src/Makefile
		 doc/Makefile])
AC_OUTPUT
