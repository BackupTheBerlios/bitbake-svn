AM_CPPFLAGS = -I$(top_srcdir)/include \
	      $(BBDLL_EXPORTS)

noinst_LTLIBRARIES = libmain.la
noinst_HEADERS = binreloc.h

libmain_la_SOURCES = main.c binreloc.c main.h
libmain_la_CFLAGS = $(BINRELOC_CFLAGS) $(GLIB2_CFLAGS)
libmain_la_LIBADD = $(BINRELOC_LIBS) $(GLIB2_LIBS)

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
