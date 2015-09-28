import socket
import sys
import os

RECV_BUFFER     = 4096
MAX_CLIENT_NUM  = 30
TIME_OUT        = 0
NEED_USR_N_PASS = '1'
USR_PASS_ERROR  = '2'
CLIENT_IP_BLOCK = '3'
USR_PASS_KEY    = "here_comes_usrname_password" 


def create_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make TCP connection reuseable
    sock.setblocking(0)
    sock.bind(address)
    sock.listen(MAX_CLIENT_NUM)
    return sock

def connect_server(address):
    sock_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_connect.connect(address)
        print 'Connected to PyTalk Server. You can start sending messages :)'
        return sock_connect
    except:
        print "unable to connect server, leaving..."
        sys.exit(1)

def msg_parser(user, msg):
    print "enter msg_parser"

def load_usr_pass():
    usr_pass_hash = {}
    file_obj = open("user_pass.txt", 'r')
    while True:
      line = file_obj.readline()
      if not line:
         break
      else:
         usrname, passwrd = line.split(' ')
         usr_pass_hash[usrname] = passwrd[:-1] # escape the '\n'
    file_obj.close()
    return usr_pass_hash




class User(object):
      def __init__(self, socket, name="new_user"): 
          socket.setblocking(0)
          self.socket = socket 
          self.name   = name # why? whats this?

      def fileno(self): 
          return self.socket.fileno()



