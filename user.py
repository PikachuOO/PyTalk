import datetime

class User(object):
      def __init__(self, socket, name="new_user"):
          socket.setblocking(0)
          self.socket      = socket
          self.name        = name
          self.ip          = socket.getsockname()[0]
          self.active_time = datetime.datetime.now()

      def fileno(self):
          return self.socket.fileno()

