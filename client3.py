# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:21:28 2017

@author: harikrishna,bathala
"""

# -*- coding: utf-8 -*-

import socket
import sys
import threading
import _thread
import datetime
#socket oblest is ceated to connect to server
try:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("failed to connect " + str(msg))
    sys.exit();
print("socket created")
# host name is retrieved using gethostbyname 
host_name=socket.gethostname()
print("IP address of host is "+host_name)
port=8000
#connected to the port 8000 which server is listeninig for requests
s.connect((host_name,port))
print("socket connected to "+host_name)
def sending_message_with_header(s,msg):
    head="PUT HTTP/1.1\n"
    timestamp=str(datetime.datetime.now())+"\n"
    length="Content-Length-"+str(len(msg))+"\n"
    message=head+timestamp+length+msg
    s.send(message.encode('utf-8'))
def strip_messsage_header(msg):
    return msg.split("\n",3)[3]
"""getting auser nmae and sending it to client to register if it unique ,
#otherwise getting the name again
"""
while True:
    r=s.recv(1024)
    print("Server says: ")
    print(strip_messsage_header(r.decode('utf-8')))
    my_name=input("me: ")
    sending_message_with_header(s,my_name)
    final_name=s.recv(1024)
    if  strip_messsage_header(final_name.decode('utf-8'))!= 'user already exists':
            print("my name is ")
            print(strip_messsage_header(final_name.decode('utf-8')))
            break
    else :
        continue
"""message are sent asynchronously to destination client
#exits from the thread if user type 'bye' as his message    
"""        
def send_message(s):
    while True :
        text=input("me: ")        
        sending_message_with_header(s,text)
        if text=='bye' :
            _thread.exit()
"""message are receive asynchronously to destination client
#exits from the thread if it receives 'client is logging off' message as his partner would have typed 'bye'
"""            
def recv_message(s):
    while True:
        re=s.recv(4096)
        print("\nclient :"+strip_messsage_header(re.decode('utf-8')))
        if strip_messsage_header(re.decode('utf'))=='client is logging off' :
            _thread.exit()
"""asks client to whether their presence to public or private for other users
#if public so,then they will get a list of users who are public right now
#else  their presence is kept private and asked to the give user name of the user they want to client
#after that 2 differnt threads are create to handle send and receicve messages by the client to their destinaion client 
"""
def connect_to_users():
    while True :
        online_presence=s.recv(1024)
        print("Server :"+strip_messsage_header(online_presence.decode('utf-8')))
        reply_online_presence=input("me: ")
        sending_message_with_header(s,reply_online_presence)
        if reply_online_presence =='yes'   :
            user_list=s.recv(1024)
            users=strip_messsage_header(user_list.decode('utf-8'))
            print("online users :")
            print(users.replace(my_name,''))
            break
        if reply_online_presence =='no' :
            ack_presence=s.recv(1024)
            print("Server :")
            print(strip_messsage_header(ack_presence.decode('utf-8')))
            break
    greet_msg=s.recv(1024)
    print("Server :")
    print(strip_messsage_header(greet_msg.decode('utf-8'))) 
    #threads call send_message and recv_message by passing the socket oblect s to communcate 
    send_thread = threading.Thread(target = send_message, args = (s,))
    recv_thread = threading.Thread(target = recv_message, args = (s,))
    send_thread.start()
    recv_thread.start()
    #waits for both threads to complete their exection 
    send_thread.join()
    recv_thread.join()
    #waits for both threads to complete their exection 
#once the user registers in server ,connecct to users is called to connect to other users 
connect_to_users()
#connection is closed after exiting from connect_to_user funcrion    
s.close
