.PHONY:

all: protobuf

protobuf: econ.proto
	protoc --cpp_out=. econ.proto
	protoc --python_out=. econ.proto
	cp econ.pb.h ~/ARGoS/iAnt-ARGoS-master/source/econ.pb.h
	cp econ.pb.cc ~/ARGoS/iAnt-ARGoS-master/source/econ.pb.cc

clean:
	rm -f econ.pb.h
	rm -f econ.pb.cc
	rm -f econ_pb2.py
	rm -f ~/ARGoS/iAnt-ARGoS-master/source/econ.pb.h
	rm -f ~/ARGoS/iAnt-ARGoS-master/source/econ.pb.cc
