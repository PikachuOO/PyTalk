import datetime
import md5
import socket
import sys
import os

def md5_encrypt(string):
    return md5.new(string).digest()

def set_minutes(minutes):
    return minutes * 60

RECV_BUFFER     = 4096
MAX_CLIENT_NUM  = 10
BLOCK_TIME      = set_minutes(1)
TIME_OUT        = set_minutes(30)
NEED_USR_N_PASS = md5_encrypt('1')
USR_PASS_ERROR  = md5_encrypt('2')
CLIENT_IP_BLOCK = md5_encrypt('3')
TIME_OUT_BLOCK  = md5_encrypt('4')
STILL_BLOCK     = md5_encrypt('5')
USR_REPEATED    = md5_encrypt('6')
USR_PASS_KEY    = "here_comes_usrname_password"
LOGOUT_STR      = "logout"

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

class NotNumberError(Exception):
    pass

class Utils(object):
    def __init__(self, connections, server_socket):
        self.connections     = connections
        self.server_socket   = server_socket
        self.usr_fail_login  = {}
        self.usr_logout_time = {}

    def msg_handler(self, user, msg):
        msg  = msg.lower()[:-1]
        args = msg.split()
        if args:
           if args[0] == "whoelse":
              usr_list = ["Current Online Users:\n"]
              for usr in self.connections:
                  if usr != user and usr != self.server_socket:
                     usr_list.append(usr.name)
                     usr_list.append('\n')
              user.socket.send(''.join(usr_list))
           elif args[0] == "wholast":
                try:
                    last_usr_list = ["last Online Uses:\n"]
                    for usrname in self.usr_logout_time.keys():
                        if not args[1].isdigit():
                            raise NotNumberError()
                        last_time = set_minutes(float(args[1]))
                        if usrname != user.name and                            \
                           self.is_usr_last(usrname, last_time):
                            last_usr_list.append(usrname)
                            last_usr_list.append('\n')
                    user.socket.send(''.join(last_usr_list))
                except IndexError:
                    self.send_err_msg(user, "plz indicate last time")
                except NotNumberError:
                    self.send_err_msg(user, "plz input number for wholast")
           elif args[0] == "broadcast":
                try:
                    if args[1] == "message":
                        if args[2:]:
                            message = ' '.join(args[2:])
                            self.broadcast(user, user.name + " says: " + message)
                            self.send_msg(user)
                        else:
                            self.send_err_msg(user,                            \
                                             "message required for broadcast")
                    elif args[1] == "user":
                        msg_idx = self.find_messgae_idx(args)
                        if msg_idx < 3:
                            self.send_err_msg(user,                            \
                                             "plz assign user to broadcast")
                        else:
                            usrnames    = args[2:msg_idx]
                            connections = self.get_usr_connections(usrnames)
                            try:
                                if connections:
                                    message = ' '.join(args[msg_idx + 1:])
                                    self.broadcast                             \
                                            (user,                             \
                                             user.name + " says: " + message,  \
                                             connections)
                                    self.send_msg(user)
                                else:
                                    self.send_err_msg(user,                    \
                                        "plz assign correct users to broadcast")
                            except IndexError:
                                self.send_err_msg                              \
                                     (user, "message required for broadcast")
                    else:
                        self.send_err_msg                                      \
                             (user, "Invalid Arguments for broadcast")
                except IndexError:
                    self.send_err_msg(user, "broadcast needs args")

           elif args[0] == "message":
                try:
                    usr = self.get_single_usr_connection(args[1])
                    if usr is None:
                        self.send_err_msg(user, "can't find the specific user")
                    else:
                        message = ' '.join(args[2:])
                        self.send_msg(usr, user.name + "says: " + message)
                        self.send_msg(user)
                except IndexError:
                    self.send_err_msg(user, "can't find user or message")
           elif args[0] == "logout":
              self.broadcast(user, user.name + " is leaving PyTalk...")
              self.remove_user(user)
           else:
              self.send_err_msg(user, "Invalid Input Command")

    def is_usr_last(self, username, last_time):
        return self.time_pass_util_now(self.usr_logout_time[username])         \
                                                                    <= last_time

    def find_messgae_idx(self, args):
        msg_idx = -1
        for i in xrange(len(args)):
            if args[i] == "message":
               msg_idx = i
               break
        return msg_idx

    def send_err_msg(self, user, message, err_prefix="Error: "):
        user.socket.send(err_prefix + message + '\n')

    def send_msg(self, user, message=""):
        user.socket.send('\n' + message + '\n')

    def get_single_usr_connection(self, usrname):
        for usr in self.connections:
            if usr != self.server_socket and usr.name == usrname:
               return usr
        return None

    def get_usr_connections(self, usrnames):
        connections = []
        for usrname in usrnames:
            for usr in self.connections:
                if usr != self.server_socket and usr.name == usrname:
                   connections.append(usr)
        return connections

    def load_usr_pass(self):
        usr_pass_hash = {}
        file_obj = open("user_pass.txt", 'r')
        while True:
          line = file_obj.readline()
          if not line:
             break
          else:
             usrname, passwrd = line.split(' ')
             if passwrd[-1] == '\n':
                usr_pass_hash[usrname] = passwrd[:-1] # escape the '\n'
             else:
                usr_pass_hash[usrname] = passwrd
        file_obj.close()
        return usr_pass_hash

    def update_user_active_time(self, user):
        user.active_time = datetime.datetime.now()

    def user_active_check(self):
        for user in self.connections:
            if user != self.server_socket and self.is_user_inactive(user):
                self.kick_out_user(user, TIME_OUT_BLOCK)

    def is_user_inactive(self, user):
        return self.time_pass_util_now(user.active_time) > TIME_OUT

    def is_usr_blocked(self, user, username):
        block_time = self.usr_fail_login.get((username, user.ip))
        return block_time and self.time_pass_util_now(block_time) <= BLOCK_TIME

    def time_pass_util_now(self, time):
        return (datetime.datetime.now() - time).total_seconds()

    def block_fail_login(self, user):
        self.kick_out_user(user, STILL_BLOCK)

    def is_usr_repeated(self, username):
        for usr in self.connections:
            if usr != self.server_socket and usr.name == username:
                return True
        return False

    def delete_repeated_usr(self, user):
        self.kick_out_user(user, USR_REPEATED)

    def kick_out_user(self, user, err_code):
        user.socket.send(err_code)
        self.remove_user(user)

    def remove_user(self, user):
        user.socket.close()
        if user in self.connections:
           self.connections.remove(user)
           if user.name != "new_user":
              self.usr_logout_time[user.name] = datetime.datetime.now()

    def broadcast(self, user, message, connections=[]):
        if not connections:
            connections = self.connections
        for usr in connections:
            if usr != self.server_socket and usr != user:
                try:
                   self.send_msg(usr, message)
                except:
                   self.remove_user(usr)
