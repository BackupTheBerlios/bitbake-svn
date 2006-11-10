
build: bitbakec.so
	echo "Done"

lemon: lemon.c
	$(CC) -o lemon lemon.c

bitbakescanner.cc: bitbakescanner.l
	flex -t bitbakescanner.l > bitbakescanner.cc

bitbakeparser.cc: lemon bitbakeparser.y python_output.h 
	./lemon bitbakeparser.y
	mv bitbakeparser.c bitbakeparser.cc

bitbakec.c: bitbakec.pyx
	pyrexc bitbakec.pyx

bitbakec-processed.c: bitbakec.c
	cat bitbakec.c | sed -e"s/__pyx_f_8bitbakec_//" > bitbakec-processed.c

bitbakec.o: bitbakec-processed.c
	$(CC) $(CFLAGS) -c bitbakec-processed.c -o bitbakec.o -fPIC

bitbakeparser.o: bitbakeparser.cc 
	$(CXX) $(CXXFLAGS) -c bitbakeparser.cc -fPIC

bitbakescanner.o: bitbakescanner.cc
	$(CXX) $(CXXFLAGS) -c bitbakescanner.cc -fPIC

bitbakec.so: bitbakec.o bitbakeparser.o bitbakescanner.o
	$(CXX) -dynamiclib -fPIC bitbakeparser.o bitbakescanner.o bitbakec.o -o bitbakec.so $(LDFLAGS)

clean:
	rm -f *.out
	rm -f *.cc
	rm -f bitbakec.c
	rm -f bitbakec-processed.c
	rm -f *.o
	rm -f *.so
	rm -f *.dylib
	rm -f bitbakec.h
	rm -f bitbakec.pxi
	rm -f bitbakeparser.h 
