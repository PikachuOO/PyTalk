import socket
import sys

RECV_BUFFER    = 4096
MAX_CLIENT_NUM = 30
TIME_OUT       = 0

def create_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make TCP connection reuseable
    sock.setblocking(0)
    sock.bind(address)
    sock.listen(MAX_CLIENT_NUM)
    return sock

def connect_server(address):
    sock_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock_connect.settimeout(2)
    sock_connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_connect.connect(address)
        print 'Connected to PyTalk Server. You can start sending messages :)'
        return sock_connect
    except:
        print "unable to connect server, leaving..."
        sys.exit



def msg_parser(user, msg):
    print "enter msg_parser"

class User(object):
      def __init__(self, socket, name="new_user"): 
          socket.setblocking(0)
          self.socket = socket 
          self.name   = name # why? whats this?

      def fileno(self): 
          return self.socket.fileno()



