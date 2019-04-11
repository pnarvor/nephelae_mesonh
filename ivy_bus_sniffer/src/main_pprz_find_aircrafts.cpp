#include <iostream>
#include <thread>
#include <chrono>
#include <unistd.h>
using namespace std;

#include <Ivy/ivyloop.h>
#include <Ivy/ivy.h>

int requestCount;
int pid;

void Callback(IvyClientPtr app, void *user_data, int argc, char *argv[])
{
	cout << IvyGetApplicationName(app) << " : ";
	for(int i = 0; i < argc; i++)
	    cout << " '" << argv[i] << "'";
    cout << endl;
}

bool run;
void loop()
{
    while(run)
    {
        //IvyBindMsg(Callback, NULL, "%d_%d ground AIRCRAFTS ((\\d+),)+",pid,requestCount);
        //IvyBindMsg(Callback, NULL, "%d_%d ground AIRCRAFTS (?:(\\d+)(?=\\,))+",pid,requestCount);
        IvyBindMsg(Callback, NULL, "%d_%d ground AIRCRAFTS (\\S*)",pid,requestCount);
        IvySendMsg("aircraft_finder %d_%d AIRCRAFTS_REQ", pid, requestCount);
        requestCount++;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

int main(int argc, char** argv)
{
	/* Mainloop management */
    requestCount = 0;
    pid = getpid();
	IvyInit("Aircraft finder", "Aircraft finder READY", NULL, NULL, NULL, NULL);
    //IvyBindMsg(Callback, NULL, "(.*)");
    //IvyBindMsg(CallbackGPS, NULL, "^\\S* GPS (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)");
    //IvyBindMsg(CallbackGPS, NULL, "^\\S* ground AIRCRAFTS .*");
	IvyStart("127.255.255.255");

    run = true;
    std::thread th(loop);

	IvyMainLoop ();

    run = false;
    th.join();

	return 0;
}



