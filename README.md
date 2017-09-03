Environment:
Operating System- Windows
Programming language – Python 3.6
To run – Python 3.6 
Available at: https://www.python.org/downloads/
		(Or)
Anaconda Installer guide: https://docs.continuum.io/anaconda/install#
				(download python 3.6)
Note: Refer screen shots folder
Compiling and Running the application:
1.	Start the server
2.	Start the client 
a.	Give a name and register
b.	Server asks whether your presence should be shown to other users.
i.	If yes
1.	You will receive a list of users who are currently online
ii.	If no
1.	You won’t receive any list 
3.	Give the user name of the user name you want to connect
4.	Now, server connects both the users and server client2 that client1 is texting and ask to continue
5.	Message from one client is relayed to another client by server and prints the message in server with header.
6.	Both clients also receive messages with header, they are striped only the main message is displayed.
7.	At any point of time, any client types ‘bye’, the other client receives that his partner is logging off and if he replies ‘bye’ then connection is terminated and they both exits from the system.
8.	Same for all other users.



Extra implementations:
1.	Used multi-threading, every client is running in different threads and sending and receiving messages are also threaded to have a asynchronous communication.
2.	Online presence, if a client enables his online presence then will he gets a list of current online users. otherwise not.
Assumptions:
To exit from a conversation:
	Client has to type ‘bye’. 
	Or closing the client terminal will also do.
Limitations:
1.	Client must type ‘yes’ when asked to start texting with other clients. This is because every client is running in different threads and in order to establish a connection from one thread to another need to from break one. 

References:
https://docs.python.org/3/library/socket.html#example
https://www.tutorialspoint.com/http/http_messages.htm
https://www.youtube.com/playlist?list=PLQVvvaa0QuDe8XSftW-RAxdo6OmaeL85M
https://pythonprogramming.net/
