import socket


def write_in_log(info):
    with open('server_info.log', 'a') as f:
        f.write(info + '\n')


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
server.bind(('', 10000))
server.listen(1)

client_sock, client_addr = server.accept()

write_in_log(f'Client {client_addr[0]} connected')

while True:
    break

client_sock.close()
