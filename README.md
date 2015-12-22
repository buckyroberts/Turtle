# Python Reverse Shell

This is a multi-client, multi-threaded reverse shell written in Python. There is still a lot of work to do, so feel free to help out with development.

To learn more about this program, watch the [YouTube Python Reverse Shell Tutorial Series](https://www.youtube.com/watch?v=1ObzpG_W_0o&list=PL6gx4Cwl9DGCbpkBEMiCaiu_3OL-_Bz_8&index=1)

Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal. 

## How to Use

To use this reverse shell, two scripts need to be running

* **server.py** - runs on a public server and waits for clients to connect
* **client.py** - connects to a remote server and then wait for commands

***

### Server

To set up server script, simply run **server.py** using Python 3.4

`python3 server.py`

You will then enter an interactive prompt where you are able to view connected clients, select a specific client, and send commands to that client remotely.

To list all current connections:

`turtle> list`

To select a target from the list of clients:

`turtle> select 3`

***

### Client

In **client.py**, first change the IP address to that of the server and then run on target machine. If client does not have a compatible version of Python installed, you can create an executable by building from the source using **setup.py**.

`python setup.py build`
