AM_CPPFLAGS = -I$(top_srcdir)/include \
	      $(BBDLL_EXPORTS)

lib_LTLIBRARIES = libbitbake.la
libbitbake_la_SOURCES = data.c
libbitbake_la_CFLAGS = $(GLIB2_CFLAGS)
libbitbake_la_LIBADD = $(GLIB2_LIBS)

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
