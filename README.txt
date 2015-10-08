# PyTalk
Computer Networks Programming Assignment 1: Socket Programming - Simple Chat App

Chia-Hao Hsu
UNI: ch3141

------------------------------- Description -----------------------------------

My chat server was separate in 4 files. 

user_pass.txt: has all the credentials to access the chat.

utils.py: class that deals with all the messages exchanged in the chat. 
             It defines a protocol that has a type, message, source and 
             destination.

user.py: class for every user of the chat.
         It defines a user that has a username, password, how many times the 
         user tried unsucessful to login, the date that that the user tried 
         to login, port number, ip number, blocked users and the user's last 
         heartbeat.

client.py: file with the Chat Client. It has functions for authentication, chat, 
           notifications, finding online users and to send heartbeat. It also 
           implements the peer-to-peer chat. 

server.py: file with the Message Center. It has functions for user authentication, 
           user message fowarding, timeout, blacklisting, presence broadcast, 
           offline messages and to send users address.

------------------------------- How to use it ---------------------------------

To run the program:
    1. Start the server with the port number that you want to user. 
        python Server.py port_number
    2. Start the client with the ip number provided by the server and the same 
       port number.
        python Client.py server_ip port_number

Implemented commands:

commands                        Functionality
whoelse                         Displays name of other connected users
wholast [number]                Displays name of those users 
                                connected within the last [number] minutes. Let 0 < number < 60|
broadcast message [message]     Broadcasts [message] to all connected users
broadcast user [user] [user]... Broadcasts [message] to the list of users
[user] message [message]
message [user] [message]        Private [message] to a [user]
logout                          Log out this user.

