AM_CPPFLAGS = -I$(top_srcdir)/include \
	      $(BBDLL_EXPORTS)
AM_LDFLAGS = -L$(top_srcdir)/src

if BB_TESTS
noinst_PROGRAMS = metadata_1
metadata_1_SOURCES = metadata_1.c
metadata_1_CFLAGS = $(GLIB2_CFLAGS)
metadata_1_LDADD = $(GLIB2_LIBS) -lbitbake
endif

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
