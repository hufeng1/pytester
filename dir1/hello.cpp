#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/types.h>
using namespace std;

int main(){
    pid_t pid;
    ofstream fout;
    fout.open("./log/mytestlog.txt");
    while(1){
        sleep(5);
        pid=getpid();
        fout<<"hello world!"<<" pid is "<<pid<<endl;
    }
}
