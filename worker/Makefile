.PHONY: 

all: cpp

cpp: worker

clean:
	rm -f gaworker
	rm -f ~/ARGoS/iAnt-ARGoS-master/gaworker

worker: gaworker.cpp cpfa.pb.cc
	c++ gaworker.cpp cpfa.pb.cc -o gaworker -lzmq -lprotobuf
	cp gaworker ~/ARGoS/iAnt-ARGoS-master
	