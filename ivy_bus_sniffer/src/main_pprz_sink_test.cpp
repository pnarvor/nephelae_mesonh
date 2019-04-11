#include <iostream>
using namespace std;

#include <Ivy/ivyloop.h>
#include <Ivy/ivy.h>

void Callback(IvyClientPtr app, void *user_data, int argc, char *argv[])
{
	cout << IvyGetApplicationName(app) << " sent ";
	for(int i = 0; i < argc; i++)
	    cout << " '" << argv[i] << "'";
    cout << endl;
}

void CallbackGPS(IvyClientPtr app, void *user_data, int argc, char *argv[])
{
	cout << IvyGetApplicationName(app) << " sent GPS : ";
	for(int i = 0; i < argc; i++)
	    cout << " '" << argv[i] << "'";
    cout << endl;
}

void CallbackGPS1(IvyClientPtr app, void *user_data, int argc, char *argv[])
{
	cout << IvyGetApplicationName(app) << "   sent GPS   1 : ";
	for(int i = 0; i < argc; i++)
	    cout << " '" << argv[i] << "'";
    cout << endl;
}

void CallbackGPS2(IvyClientPtr app, void *user_data, int argc, char *argv[])
{
	cout << IvyGetApplicationName(app) << " sent GPS 142 : ";
	for(int i = 0; i < argc; i++)
	    cout << " '" << argv[i] << "'";
    cout << endl;
}

int main(int argc, char** argv)
{
    std::string address("127.255.255.255");
    if(argc > 1)
        address = argv[1];

	/* Mainloop management */
	IvyInit("Message dump", "Message dump READY", NULL, NULL, NULL, NULL);
    IvyBindMsg(Callback, NULL, "(.*)");
    //IvyBindMsg(Callback, NULL, "(.*\ GPS\ .*)");
    //IvyBindMsg(CallbackGPS, NULL, "^\\S* GPS (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)");
    //IvyBindMsg(CallbackGPS1, NULL, "1 GPS (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)");
    //IvyBindMsg(CallbackGPS2, NULL, "142 GPS (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)");

	//IvyStart("127.255.255.255");
	IvyStart(address.c_str());

	IvyMainLoop ();

	return 0;
}



