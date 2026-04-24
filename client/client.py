import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

HOST = "192.168.29.25"
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                chat_box.after(0,display_message,message)
        except:
            break
def display_message(msg):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state="disabled")
    chat_box.yview(tk.END)

def send_message():
    msg = input_field.get().strip()
    if msg:
        formatted = f"MESSAGE|{username}|{msg}"
        try:
            client.send(formatted.encode("utf-8"))
        except:
            messagebox.showerror("Error", "Connection lost")
        input_field.delete(0, tk.END)

def on_close():
    try:
        client.send(f"DISCONNECT|{username}|".encode("utf-8"))
        client.close()
    except:
        pass
    root.destroy()


root = tk.Tk()
root.title("LAN Chat")
username = simpledialog.askstring("Username","Enter your username:", parent=root)
if not username:
    exit()
chat_box = tk.Text(root, state="disabled", height = 20, width = 50)
chat_box.pack(padx = 10, pady = 5)

frame = tk.Frame(root)
frame.pack(padx = 10, pady = 5)

input_field = tk.Entry(frame, width = 50 )
input_field.pack(side=tk.LEFT)

send_button = tk.Button(frame, text = "Send", command = send_message)
send_button.pack(side = tk.RIGHT)

try:
    client.connect((HOST, PORT))
    client.send(f"CONNECT|{username}|".encode("utf-8"))
except:
    messagebox.showerror("Error", "Unable to connect to server")
    root.destroy()

thread = threading.Thread(target=receive_message, daemon=True)
thread.start()

root.bind("<Return>",lambda event: send_message())

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()