AM_CPPFLAGS = -I$(top_srcdir)/include \
	      $(BBDLL_EXPORTS)

lib_LTLIBRARIES = libbitbake.la
libbitbake_la_SOURCES = data.c
libbitbake_la_CFLAGS = $(GLIB2_CFLAGS)
libbitbake_la_LIBADD = $(GLIB2_LIBS)
libbitbake_la_LDFLAGS = -version-info $(PACKAGE_LTCUR):$(PACKAGE_LTREV):$(PACKAGE_LTAGE) \
			-release $(PACKAGE_LTRELEASE) -export-dynamic

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
