AM_CPPFLAGS = -I$(top_srcdir)/include \
	      $(BBDATA_DLL_EXPORTS)

lib_LTLIBRARIES = libbitbake-data-0.0.la
libbitbake_data_0_0_la_SOURCES = backend-sqlite3.c
libbitbake_data_0_0_la_CFLAGS = $(GLIB2_CFLAGS) -DLOCALSTATEDIR="\"@localstatedir@\""
libbitbake_data_0_0_la_LIBADD = $(GLIB2_LIBS)
libbitbake_data_0_0_la_LDFLAGS = -version-info $(LT_CURRENT):$(LT_REVISION):$(LT_AGE) \
				 -export-dynamic

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
