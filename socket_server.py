import socket

x= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

h_name="45.32.155.246" #socket.gethostname()
print("elindult itt: ", h_name)

port= 2222

x.bind((h_name, port))
print("kész")

while 1:
    print("hallgatás...")
    x.listen(1) #ennyi csatlakozást vár maximum

    connection,address= x.accept()
    print(address)
 
    while 1:
        e_message = connection.recv(1024)
        if not e_message:
            print("kapcsolat bontva")
            break
        d_message = e_message.decode()
        print(d_message)
        msg = input()
        connection.send(msg.encode())