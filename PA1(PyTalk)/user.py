class User(object):
      def __init__(self, socket, name="new_user"): 
          socket.setblocking(0)
          self.socket = socket 
          self.name   = name # why? whats this?

      def fileno(self): 
          return self.socket.fileno()



