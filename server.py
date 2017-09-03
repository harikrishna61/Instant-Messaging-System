# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:21:28 2017

@author: harikrishna,bathala
"""

# -*- coding: utf-8 -*-
import socket
import sys
import _thread
import threading
import datetime

""" host name is retrieved using gethostbyname and  a socket object is created
"""
host=socket.gethostname()
port=8000
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""host is binded to port to 8000 to listen all incoming requests
"""
try:
    s.bind((host,port))
except socket.error as msg:
    print("bind failed"+str(msg))
    sys.exit()
"""started listening to requests ,upto 10 
"""
s.listen(10)


"""lsts are created to store sockets,all users,active users(who are communicating with some one)
#online users list to store which users are currently nad like to show their presence to others
"""
client_sockets_list=[]
user_name_list=[]
active_user_list=[]
online_user_list=[]
"""whenever this server wants to send a message this function is called 
    it adds http header,time samp,length of the message added as a header to the message
"""
def sending_message_with_header(s,msg):
    head="PUT HTTP/1.1\n"
    timestamp=str(datetime.datetime.now())+"\n"
    length="Content-Length-"+str(len(msg))+"\n"
    message=head+timestamp+length+msg
    s.send(message.encode('utf-8'))
"""
whenever server receives a message this function is called to strip the header of the message
"""
def strip_messsage_header(msg):
   return msg.split("\n",3)[3]

"""
this function receies message from destnation client and send the same message to source client 
"""
def send_message(to_sock,conn,sender,receiver):
    while True :
        re_chat=client_sockets_list[to_sock].recv(4096)
        
        
        """if any user type bye,means that they are ending the conversation
        #'clent is logging off' message is forwarded to their partner
        #once both users typed bye the they will exited from send  and receive message thread
        """
        if strip_messsage_header(re_chat.decode('utf-8'))=='bye' :
            bye_msg="client is logging off"
            print(bye_msg)
            sending_message_with_header(conn,bye_msg)
            """conn.sendall(bye_msg.encode('utf-8'))
            their user name,socket are removed from user name and active userlist as they are exiting
            """
            active_user_list.remove(sender)
            user_name_list.remove(sender)
            online_user_list.remove(sender)
            break
        
        #message are forwarded to sourceclient  
        
        elif re_chat :
            print(sender+" says :"+re_chat.decode('utf-8'))
            #conn.sendall(re_chat)
            sending_message_with_header(conn,strip_messsage_header(re_chat.decode('utf-8')))
        else :
            break
    _thread.exit()
#this function receies message from source client and send the same message to destination client         
def recv_message(to_sock,conn,sender,receiver):
    while True:
        cl1_msg=conn.recv(4096)   
        
        """if any user type bye,means that they are ending the conversation
        #'clent is logging off' message is forwarded to their partner
        #once both users typed bye the they will exited from send  and receive message thread
        """
        if strip_messsage_header(cl1_msg.decode('utf-8'))=='bye' :
            bye_msg1="client is logging off"
            print(bye_msg1) 
            #their user name,socket are removed from user name and active userlist as they are exiting
            sending_message_with_header(client_sockets_list[to_sock],bye_msg1)
            active_user_list.remove(receiver)
            user_name_list.remove(receiver)
            online_user_list.remove(receiver)  
            break
        #message are forwarded to destination client     
        elif cl1_msg :
            print(receiver+" says :"+cl1_msg.decode('utf-8')) 
            sending_message_with_header(client_sockets_list[to_sock],strip_messsage_header(cl1_msg.decode('utf-8')))
        else :
            break
    _thread.exit()       
    
#here the clients messages and responses from their destination users are being relayed by the server both forward and backward   
def thread_for_client(conn,current_user):  
   #welcome_msg='Thank you,enter user name of the client you want to connect.Active users at he moment is'
    while True:
        mg= conn.recv(4096)
        reply=mg.decode('utf-8')
    
        """if the destination user is active(comunicating with some one) or 
            they are no such user,user busy  is sent to the client 
           if the destination user is current user itself then user is busy message is sent
        """
        if strip_messsage_header(reply) in active_user_list or strip_messsage_header(reply)==current_user  :
            print("Client says :"+strip_messsage_header(reply))
            user_busy_txt="user is  busy "
            sending_message_with_header(conn,user_busy_txt)
            continue
        if strip_messsage_header(reply) == "yes":
            sys.exit()
        if strip_messsage_header(reply) not in user_name_list :
            print("Client says :"+strip_messsage_header(reply))
            user_busy_txt="user is  invalid"
            sending_message_with_header(conn,user_busy_txt)
            continue
        else :
            break
    """if the user is not active and registerd a connection is made b/w the two users    
        now,the destination user is added to active user  as he started to communicating and
        his socket object is also retrieved for communicating
    """
    to_sock=user_name_list.index(strip_messsage_header(reply))
    active_user_list.append(strip_messsage_header(reply))
    from_sock=client_sockets_list.index(conn)
    active_user_list.append(user_name_list[from_sock])
    #telling the destination user that ,'this user' is texting you
    first_txt=user_name_list[from_sock]+" is texting you.Type 'yes' to connect."
    sending_message_with_header(client_sockets_list[to_sock],first_txt)
    print("Client says :"+first_txt)
    """a seperate thread is created to handle send and receive messages to client,
    #passing source client,destination clien's user name and socket object
    """
    recv_thread = threading.Thread(target = recv_message, args = (to_sock,conn,strip_messsage_header(reply),user_name_list[from_sock],))
    send_thread = threading.Thread(target = send_message, args = (to_sock,conn,strip_messsage_header(reply),user_name_list[from_sock],))
    recv_thread.start()
    send_thread.start()
    #waits for both threads to complete their exection
    send_thread.join()
    recv_thread.join()    
    client_sockets_list.remove(conn)
    del client_sockets_list[to_sock]
    
# accepting users and registering each user by a user name.making sure that 2 user gets same name.  
def regestering_users():    
    while True:
        print("server socket is in listening mode")
        connection, addr = s.accept()
        while True:
            get_user_name="select an user name "
            sending_message_with_header(connection,get_user_name)
            user_name=connection.recv(1024)
            if strip_messsage_header(user_name.decode('utf-8')) not in user_name_list :
                    user_name_list.append(strip_messsage_header(user_name.decode('utf-8')))
                    ack_name=strip_messsage_header(user_name.decode('utf-8'))
                    sending_message_with_header(connection,ack_name)
                    break
            else:
                user_exits="user already exists"
                sending_message_with_header(connection,user_exits)
            
        print("connected to :"+str(addr[0]))
        client_sockets_list.append(connection)
        """asking users whether they to know other users about presnence.
        #if yes they will receive the list of current online users,
        #other wise no and their presence is kept secret
        """
        while True:
            view_online="Do you want your presence to be known by other users(yes/no)"
            sending_message_with_header(connection,view_online)
            reply_online_view=connection.recv(1024)
            if strip_messsage_header(reply_online_view.decode('utf-8')) == 'yes' :
                online_user_list.append(strip_messsage_header(user_name.decode('utf-8')))
                users='-'.join(online_user_list)
                sending_message_with_header(connection,users)
                break
            if strip_messsage_header(reply_online_view.decode('utf-8')) =='no' :
                no_online_presence="thank you,your online presence will be kept secret."
                sending_message_with_header(connection,no_online_presence)
                break
        #asking the user to whom he wants to connect    
        welcome_msg='Thank you,enter user name of the client you want to connect'
        sending_message_with_header(connection,welcome_msg)
        """creating a seperate thread for every user 
        passing the socket object and user name of user to thread_for_client function to make connection
        with the client the user desires        
        """
        start_thread = threading.Thread(target = thread_for_client, args = (connection,strip_messsage_header(user_name.decode('utf-8')),))
        start_thread.start()
    start_thread.join()   
    connection.close() 
#once the server started to listening to requests ,registering users function is called to register users        
regestering_users()        

s.close()
