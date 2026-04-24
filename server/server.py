import socket
import threading

#server configurations
HOST = '0.0.0.0'
PORT = 12345

# data structure
clients = []
usernames = {}

def broadcast(message,sender_socket = None):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        clients.remove(client)

    username = usernames.get(client,"Unknown")

    if client in usernames:
        del usernames[client]

    try:
        client.close()
    except:
        pass

    broadcast(f"SYSTEM|{username} left the chat|")
    print(f"[DISCONNECT] {username}")


def handle_client(client):
    try:
        msg = client.recv(1024).decode('utf-8')
        msg_type, username, _ = msg.split("|")

        if msg_type != "CONNECT":
            client.close()
            return

        usernames[client] = username
        clients.append(client)

        print(f"[CONNECTED] {username}")

        broadcast(f"SYSTEM|{username} joined the chat|")

        while True:
            message = client.recv(1024).decode('utf-8')
            msg_type, username, content = message.split("|")

            if msg_type == "MESSAGE":
                formatted = f"{username}: {content}"
                print(f"[MESSAGE] {formatted}")
                broadcast(formatted)

            elif msg_type == "DISCONNECT":
                remove_client(client)
                break
    except:
        remove_client(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[STARTED] Server is running on {HOST}:{PORT})")

    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()