AM_CFLAGS = -I$(top_srcdir)/include

noinst_PROGRAMS = main
noinst_HEADERS = binreloc.h

main_SOURCES = main.c binreloc.c main.h
main_CFLAGS = $(BINRELOC_CFLAGS)
main_LDADD = $(BINRELOC_LIBS)

relinclude_HEADERS = main.h

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
