
build: bitbake-helper
	echo "Done"

lemon: lemon.c
	$(CC) -o lemon lemon.c

bitbakescanner.cc: bitbakescanner.l
	flex -t bitbakescanner.l > bitbakescanner.cc

bitbakeparser.cc: lemon bitbakeparser.y python_output.h 
	./lemon bitbakeparser.y
	mv bitbakeparser.c bitbakeparser.cc

bitbakeparser.o: bitbakeparser.cc 
	$(CXX) $(CXXFLAGS) -c bitbakeparser.cc

bitbakescanner.o: bitbakescanner.cc
	$(CXX) $(CXXFLAGS) -c bitbakescanner.cc

main.o:
	$(CXX) $(CXXFLAGS) -c main.cxx

bitbake-helper: main.o bitbakeparser.o bitbakescanner.o
	$(CXX) bitbakeparser.o bitbakescanner.o  main.o -o bitbake-helper $(LDFLAGS)

clean:
	rm -f *.out
	rm -f *.cc
	rm -f bitbakec.c
	rm -f bitbakec-processed.c
	rm -f *.o
	rm -f bitbakec.h
	rm -f bitbakec.pxi
	rm -f bitbakeparser.h 
