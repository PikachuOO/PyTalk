import select
import socket
import sys

# from utils import User
from utils import connect_server, msg_parser, RECV_BUFFER

def argv_reader(argv):
    if len(argv) < 3:
       print "Usage: python client.py hostname port"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])



class Client(object):      
      def __init__(self, host, port):
          self.server_connect = connect_server((host, port))
          self.socket_list = [sys.stdin, self.server_connect]

      def client_loop(self):
          status = 1;

          self.prompt()
          while status:
                try:
                       read_sockets, write_sockets, error_sockets =             \
                                     select.select(self.socket_list, [], [])

                       for socket in read_sockets:
                           if socket is self.server_connect: # msg from server
                              msg = socket.recv(RECV_BUFFER)
                              if not msg:
                                 print "Shxt...PyTalk Server Down :("
                                 sys.exit(2)
                              else:
                                 sys.stdout.write(msg)
                                 self.prompt()      
                           else:
                              msg = sys.stdin.readline()
                              self.server_connect.sendall(msg)
                              self.prompt()                              

                except KeyboardInterrupt, SystemExit:
                       print "\nPyTalk User Leaving..."
                       status = 0
      
      def prompt(self, msg_prefix="[Me]"):
          sys.stdout.write(msg_prefix + "> ")
          sys.stdout.flush()

      def run(self):
          self.client_loop();

if __name__ == "__main__":
   host, port = argv_reader(sys.argv) 
   client     = Client(host, port)
   client.run()