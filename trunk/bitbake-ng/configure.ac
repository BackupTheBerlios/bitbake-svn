m4_include([config/version.m4])
AC_INIT(bitbake-ng, BITBAKE_PKGVER, kergoth@handhelds.org)
AC_PREREQ(2.57)

AC_CONFIG_SRCDIR([include/bitbake.h])
AC_CONFIG_AUX_DIR(config)
AM_CONFIG_HEADER([config.h])

AM_INIT_AUTOMAKE

PACKAGE_LTRELEASE=BITBAKE_RELVER
AC_SUBST([PACKAGE_LTRELEASE])

PACKAGE_LTCUR=BITBAKE_LT_CUR
AC_SUBST([PACKAGE_LTCUR])

PACKAGE_LTREV=BITBAKE_LT_REV
AC_SUBST([PACKAGE_LTREV])

PACKAGE_LTVERSION="\$(PACKAGE_LTCUR):\$(PACKAGE_LTREV)"
AC_SUBST([PACKAGE_LTVERSION])


# system
AC_CANONICAL_SYSTEM


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
BB_DEFAULT_FLAGS

AC_PROG_CC
BB_CC_HIDDEN_VISIBILITY

AC_PROG_CXX
BB_CXX_HIDDEN_VISIBILITY_INLINES

AC_PROG_LIBTOOL
AC_SUBST(LIBTOOL_DEPS)


# other
AM_BINRELOC

# This variable is used to indicate whether we're compiling
# a part of our library itself, or external binaries.
BBDLL_EXPORTS="-DBBDLL_EXPORTS"
AC_SUBST([BBDLL_EXPORTS])

AC_CONFIG_FILES([Makefile
                 src/Makefile
		 doc/Makefile])
AC_OUTPUT
