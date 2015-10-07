#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include "zmq.hpp"
#include "cpfa.pb.h"
using namespace std;
using namespace zmq;

void PrintWorker(const proto::Cpfa& cpfa) {
    cout << "(Worker) " << cpfa.probabilityofswitchingtosearching() << std::endl;
    cout << "(Worker) " << cpfa.probabilityofreturningtonest() << std::endl;
    cout << "(Worker) " << cpfa.uninformedsearchvariation() << std::endl;
    cout << "(Worker) " << cpfa.rateofinformedsearchdecay() << std::endl;
    cout << "(Worker) " << cpfa.rateofsitefidelity() << std::endl;
    cout << "(Worker) " << cpfa.rateoflayingpheromone() << std::endl;
    cout << "(Worker) " << cpfa.rateofpheromonedecay() << std::endl;
}

int main ()
{
    // Verify that the version of the library that we linked against is
    // compatible with the version of the headers we compiled against.
    GOOGLE_PROTOBUF_VERIFY_VERSION;
    
    // Prepare our context and socket...
    context_t context(1);
    socket_t socket(context, ZMQ_PAIR);
    socket.connect("tcp://localhost:5556");
    
    cout << "(Worker) Worker connected!" << std::endl;
    
    bool stop = false;
    
    while (!stop)
    {
        // Receive the worker response...
        zmq::message_t request;
        socket.recv(&request);
        std::string data = std::string(static_cast<char*>(request.data()), request.size());
        
        // Print the worker response details...
        proto::Cpfa cpfa;
        
        {
            if (!cpfa.ParseFromString(data)) {
                cerr << "(Worker) Failed to parse worker details..." << endl;
                return -1;
            }
        }
        
        PrintWorker(cpfa);
        
        string payload;
        
        if (cpfa.probabilityofswitchingtosearching() > 2 && cpfa.probabilityofswitchingtosearching() < 3)
        {
            payload = "HeyYo";
            stop = true;
        }
        else
        {
            payload = "YoHey";
        }
        
        // Completed work, send to server...
        zmq::message_t reply(payload.size());
        memcpy((void *) reply.data(), payload.data(), payload.size());
        std::cout << "(Worker) Sending completed work to server..." << std::endl;
        socket.send(reply);
    }
    
    std::cout << "(Worker) Exiting..." << std::endl;
    
    // Delete all global objects allocated by libprotobuf...
    google::protobuf::ShutdownProtobufLibrary();
    
    return 0;
}