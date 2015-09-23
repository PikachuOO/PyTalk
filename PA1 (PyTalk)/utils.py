import socket

MAX_CLIENT_NUM = 30
TIME_OUT    = 0

def create_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(address)
    sock.listen(MAX_CLIENT_NUM)
    return sock

def msg_parser(msg):
    print "enter msg_parser"

class User(object):
      def __init__(self, socket, name="new_user"): 
          socket.setblocking(0)
          self.socket = socket 
          self.name   = name # why? whats this?

      def fileno(self): 
          return self.socket.fileno



