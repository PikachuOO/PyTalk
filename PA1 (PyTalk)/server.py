import select
import socket
import sys

from utils import User
from utils import create_socket, msg_parser

READ_BUFF = 4096

class Server(object):
      def __init__(host="127.0.0.1", port=8080):
          self.sever_socket = create_socket(host, port)
          self.connections  = [self.sever_socket]

      def sever_loop():
          status = 1;
          while status:
                try:
                    read_users, write_users, error_sockets =                   \
                                     select.select(self.connections, [], [], 0)
                    for user in read_users:
                        if user is self.sever_socket: # new client join
                           new_user, addr = self.sever_socket.accept()
                           self.connections.append(new_user)
                           print "Client %s at %s now join!" % (new_user, addr)
                        else: # new message
                           msg = user.socket.recv(READ_BUFF)
                           if msg:
                              msg_parser(user, msg)
                           else: # no msg, user down, close connection
                              user.socket.close()
                              self.connections.remove(user)

                    for socket in error_sockets:
                        socket.close()
                        self.connections.remove(socket)

                except KeyboardInterrupt, SystemExit:
                       print "Server Close..."
                       status = 0
          
          self.sever_socket.close()  
          
      def run(self):
          self.sever_loop();


if __name__ == "__main__":
   server = Server(port=sys.argv[1])
   server.run()