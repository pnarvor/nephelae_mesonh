#include <iostream>
#include <thread>
#include <chrono>
using namespace std;

#include <Ivy/ivyloop.h>
#include <Ivy/ivy.h>

bool run;
void loop()
{
    while(run)
    {
        IvySendMsg("Message source NO_TYPE coucou");
        cout << "sent : 'Message source NO_TYPE coucou'" << endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

int main(int argc, char** argv)
{
    std::string address("127.255.255.255");
    if(argc > 1)
        address = argv[1];

	/* Mainloop management */
	IvyInit("Message source", "Message source READY", NULL, NULL, NULL, NULL);
	//IvyStart("127.255.255.255");
	IvyStart(address.c_str());

    run = true;
    std::thread th(loop);


    IvyMainLoop();
    //getchar();

    run = false;
    th.join();

	return 0;
}




