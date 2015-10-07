.PHONY: 

all: 
	cd config; make
	cd proto; make

clean:
	cd config; make clean
	cd proto; make clean
	