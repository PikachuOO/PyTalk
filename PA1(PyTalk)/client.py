import select
import socket
import sys

# from utils import User
from utils import connect_server
from utils import RECV_BUFFER, NEED_USR_N_PASS, USR_PASS_ERROR, \
                  CLIENT_IP_BLOCK, USR_PASS_KEY


def argv_reader(argv):
    if len(argv) < 3:
       print "Usage: python client.py hostname port"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])


class Client(object):      
      def __init__(self, host, port):
          self.server_connect = connect_server((host, port))
          self.socket_list    = [sys.stdin, self.server_connect]

      def prompt(self, msg_prefix="[Me]"):
          sys.stdout.write(msg_prefix + "> ")
          sys.stdout.flush()

      def client_loop(self):
          status = 1;

          # self.prompt()
          while status:
                try:
                       read_sockets, write_sockets, error_sockets =            \
                                     select.select(self.socket_list, [], [])

                       for socket in read_sockets:
                           if socket is self.server_connect: # msg from server
                              msg = socket.recv(RECV_BUFFER)
                              if not msg:
                                 print "Shxt...PyTalk Server Down :(\n"
                                 sys.exit(2)
                              else:
                                 if self.is_client_login(msg):
                                    sys.stdout.write(msg)
                                    self.prompt()      
                                 else:
                                    if msg == NEED_USR_N_PASS:
                                       self.login_prompt                       \
                                       ("Hi, Plz Enter Username and Password\n")
                                    elif msg == USR_PASS_ERROR:
                                       self.login_prompt                       \
                                       ("Username or Password wrong, try again.\n")
                                    elif msg == CLIENT_IP_BLOCK:
                                       sys.stdout.write                        \
                                       ("No more than 3 times error, block ~\n")
                                       status = 0

                           else: # msg from user to type in
                              msg = sys.stdin.readline()
                              if msg:
                                 self.server_connect.sendall(msg)
                              # self.prompt()                              

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving PyTalk..."
                       status = 0
          self.server_connect.close()        
      
      def is_client_login(self, msg):
          return not (msg == NEED_USR_N_PASS or                                \
                      msg == USR_PASS_ERROR  or                                \
                      msg == CLIENT_IP_BLOCK)
            
      def login_prompt(self, display_msg):
          sys.stdout.write(display_msg)
          self.prompt("Username:")
          username = raw_input()
          self.prompt("Password:")
          password = raw_input()
          self.server_connect.sendall(USR_PASS_KEY                             \
                                      + "#" + username                         \
                                      + "#" + password)


      def run(self):
          self.client_loop();

if __name__ == "__main__":
   host, port = argv_reader(sys.argv) 
   client     = Client(host, port)
   client.run()