import socket
import threading
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def brodcast(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while 1:
        try:
            msg = client.recv(1024)
            print(f"{msg.decode('utf-8')}")
            now = time.asctime().split(" ")[-2][0:5]
            msg = f"[{now}] {msg.decode('utf-8')}"

            brodcast(msg.encode("utf-8"))
        except Exception as ex:
            print(ex)
            index = clients.index(client)
            clients.pop(index)
            nicknames.pop(index)
            client.close()
            break


def receive():
    while 1:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client is {nickname.decode('utf-8')}")
        brodcast(
            f"{nickname.decode('utf-8')} has connected to the server!\n".encode("utf-8")
        )
        client.send("connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running...")
print()

receive()
