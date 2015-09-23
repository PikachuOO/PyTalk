import select
import socket
import sys

from utils import User
from utils import create_socket, msg_parser, RECV_BUFFER

localhost    = "127.0.0.1"
default_port = 8080

class Server(object):
      
      def __init__(self, host=localhost, port=default_port):
          self.sever_socket = create_socket((host, port))
          self.connections  = [self.sever_socket]
          print "PyTalk server started on port " + str(port)

      def server_loop(self):
          status = 1;
          while status:
                try:
                    read_users, write_users, error_sockets =                   \
                                     select.select(self.connections, [], [], 0)
                    for user in read_users:
                        if user is self.sever_socket: # new client join
                           new_user, addr = self.sever_socket.accept()
                           new_user       = User(new_user, addr)
                           self.connections.append(new_user)
                           print "Client %s at %s now join!" % (new_user, addr)
                        else: # new message
                           msg = user.socket.recv(RECV_BUFFER)
                           if msg:
                              msg_parser(user, msg)
                           else: # no msg, user down, close connection
                              user.socket.close()
                              self.connections.remove(user)

                    for socket in error_sockets:
                        socket.close()
                        self.connections.remove(socket)

                except KeyboardInterrupt, SystemExit:
                       print "\nPyTalk Server Close..."
                       status = 0
          
          self.sever_socket.close()  
          
      def run(self):
          self.server_loop();


if __name__ == "__main__":
   server = Server(port = 8080 if sys.argv is not None else int(sys.argv[1]))
   server.run()