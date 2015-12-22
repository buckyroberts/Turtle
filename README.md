# Python Reverse Shell

This is a multi-client, multi-threaded reverse shell written in Python. There is still a lot of work to do.

[YouTube Tutorial Series](https://www.youtube.com/watch?v=1ObzpG_W_0o&list=PL6gx4Cwl9DGCbpkBEMiCaiu_3OL-_Bz_8&index=1)

## How to Use

To use this reverse shell, two scripts need to be running

* **server.py** - runs on a public server and waits for clients to connect
* **client.py** - connects to a remote server and then wait for commands

***

### Server

To set up server script, simply run server.py using Python 3.4

`python3 server.py`

You will then enter an interactive prompt where you are able to view connected clients, select a specific client, and send commands to that client remotely.

To list all current connections:

`turtle> list`

To select a target from the list of clients:

`turtle> select 3`
