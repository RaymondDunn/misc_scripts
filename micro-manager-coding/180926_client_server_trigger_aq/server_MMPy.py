import socket
import json

# vars
port = 9999
buffer_size = 4096

#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host,
serversocket.bind(("localhost", port))

# listen for up to x connections
print("Listening for a connection...")
serversocket.listen(15)

while True:

    # accept connections from outside
    (clientsocket, client_address) = serversocket.accept()

    # in this case, we'll pretend this is a threaded server
    # ct = client_thread(clientsocket)
    # ct.run()

    try:
        print("connection from", client_address)

        data = clientsocket.recv(buffer_size)
        print("Received {}".format(data))

        if data:
            print("sending back to client")
            clientsocket.sendall(data)

    finally:

        # closing connection
        print("closing connection...")
        # close connection
        clientsocket.close()

