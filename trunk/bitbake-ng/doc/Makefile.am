docs: apidocs

apidocs: doxygen/html/index.html

doxygen/html/index.html: $(top_srcdir)/$(subdir)/Doxyfile
	cd $(top_builddir); doxygen $(srcdir)/$(subdir)/Doxyfile

clean-local:
	rm -rf doxygen

maintainer-clean-local:
	rm -f $(srcdir)/Makefile.in
