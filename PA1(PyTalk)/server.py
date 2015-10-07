import datetime
import select
import socket
import sys

from user  import User
from utils import RECV_BUFFER, NEED_USR_N_PASS, USR_PASS_ERROR,                \
                  CLIENT_IP_BLOCK, USR_PASS_KEY
from utils import TIME_OUT, BLOCK_TIME
from utils import create_socket
from utils import Utils

localhost    = socket.gethostbyname(socket.gethostname())
default_port = 8080

class Server(object):

      def __init__(self, host=localhost, port=default_port):
          self.server_socket  = create_socket((host, port))
          self.connections    = [self.server_socket]
          self.u              = Utils(self.connections, self.server_socket)
          self.usr_database   = self.u.load_usr_pass()
          self.u.usr_fail_login = {}
          self.login_count    = {}
          print "PyTalk server started at %s on port %s" % (localhost, str(port))

      def server_loop(self):
          status = 1;
          while status:
                try:
                    read_users, write_users, error_sockets =                   \
                                     select.select(self.u.connections, [], [], 0)
                    self.u.user_active_check()
                    for user in read_users:
                        if user is self.server_socket: # new client join
                           new_user, addr = self.server_socket.accept()
                           new_user       = User(new_user)
                           self.u.connections.append(new_user)
                           new_user.socket.send(NEED_USR_N_PASS)
                           self.login_count[new_user] = 0
                           print "Client %s at %s now join!" % (new_user, self.get_usr_ip(new_user))
                        else: # new message from client
                           msg = user.socket.recv(RECV_BUFFER)
                           if msg:
                              if USR_PASS_KEY in msg:
                                 if self.is_usr_login(user, msg):
                                    user.socket.send                           \
                                    ("Welcome %s to join PyTalk!\n" % user.name)
                                    self.u.broadcast(user,                     \
                                    "User: %s now joining PyTalk" % user.name)
                              else:
                                 self.u.update_user_active_time(user)
                                 self.u.msg_handler(user, msg)
                           else: # no msg, user down, close connection
                              self.u.remove_user(user)

                    for socket in error_sockets:
                        socket.close()
                        self.u.connections.remove(socket)

                except KeyboardInterrupt, SystemExit:
                       print "\nPyTalk Server Close..."
                       status = 0

          self.server_socket.close()

      def get_usr_ip(self, user):
          return user.socket.getsockname()[0]

      def is_usr_login(self, user, msg):
          if self.is_usr_pass_correct(user, msg):
             if self.u.is_usr_blocked(user):
                 self.u.block_fail_login(user)
                 return False
             else:
                 self.login_count[user] = 0
                 if self.u.usr_fail_login.get((user.name, user.ip)):
                    del self.u.usr_fail_login[(user.name, user.ip)]
                 user.active_time = datetime.datetime.now()
                 return True
          else:
             self.login_count[user] += 1
             if self.login_count[user] < 3:
                user.socket.send(USR_PASS_ERROR)
             else:
                user.socket.send(CLIENT_IP_BLOCK)
                username = self.get_username_from_msg(msg)
                self.u.usr_fail_login[(username, user.ip)] =                   \
                                                         datetime.datetime.now()
                self.u.remove_user(user)
                del self.login_count[user]
             return False

      def is_usr_pass_correct(self, user, msg):
          key, username, password = msg.split('#')
          if self.usr_database.get(username) != password:
             return False
          else:
             user.name = username
             return True

      def get_username_from_msg(self, msg):
          key, username, password = msg.split('#')
          return username

      def run(self):
          self.server_loop();

if __name__ == "__main__":
   server = Server(port = 8080 if len(sys.argv) < 2 else int(sys.argv[1]))
   server.run()