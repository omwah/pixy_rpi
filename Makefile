CC=g++
LIBS=-lwiringPi
CFLAGS=-I.
DEPS = Pixy.h

%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

echo: echo.o
	$(CC) -o echo echo.o $(LIBS)

clean:
	rm -f *.o echo
