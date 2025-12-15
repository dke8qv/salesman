# Makefile

CXX = g++
CXXFLAGS = -O3 -std=c++17 -Wall -Wextra

PY = python3

default: all

all: datareader sales

# building city data reader example
datareader: datareader.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

# traveling salesman solver
sales: sales.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f datareader sales *.o *~ *.png *.pdf *.csv route*.dat

