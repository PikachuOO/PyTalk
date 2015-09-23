MAX_CLIENTS = 30
TIME

def create_socket(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(address, port)
    sock.listen(MAX_CLIENT_NUM)

