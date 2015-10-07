#include <iostream>
#include <fstream>
#include <string>
#include "cpfa.pb.h"
using namespace std;

void ListParams(const proto::Cpfa& cpfa) {
    cout << cpfa.probabilityofswitchingtosearching() << "\n";
    cout << cpfa.probabilityofreturningtonest() << "\n";
    cout << cpfa.uninformedsearchvariation() << "\n";
    cout << cpfa.rateofinformedsearchdecay() << "\n";
    cout << cpfa.rateofsitefidelity() << "\n";
    cout << cpfa.rateoflayingpheromone() << "\n";
    cout << cpfa.rateofpheromonedecay() << "\n";
}


int main(int argc, char* argv[]) {
    // Verify that the version of the library that we linked against is
    // compatible with the version of the headers we compiled against.
    GOOGLE_PROTOBUF_VERIFY_VERSION;
    
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " CPFA_FILE" << endl;
        return -1;
    }
    
    proto::Cpfa cpfa;
    
    {
        // Read the existing worker parameters.
        fstream input(argv[1], ios::in | ios::binary);
        if (!cpfa.ParseFromIstream(&input)) {
            cerr << "Failed to parse CPFA parameters." << endl;
            return -1;
        }
    }
    
    ListParams(cpfa);
    
    // Optional:  Delete all global objects allocated by libprotobuf.
    google::protobuf::ShutdownProtobufLibrary();
    
    return 0;
}