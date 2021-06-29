from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter 

test = True

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            msg_list.insert(tkinter.END,"Le serveur a crashé !!!!");
            
            break


def send(event=None):  
    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, "utf8"))

def exitc(event=None):
    
    scene.quit()



def close_window ():
    
    scene.destroy()

scene = tkinter.Tk()
scene.title("Application d'enchères")

messages_frame = tkinter.Frame(scene)
my_msg = tkinter.StringVar()  # pour les msg envoyéq.
my_msg.set("nom")
scrollbar = tkinter.Scrollbar(messages_frame)  # Pour parcourir les messages passés.
# La suite contiendra les messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(scene, textvariable=my_msg)
entry_field.bind("<Return>", send) #Return=la clé entrer du clavier #elle déclenche la méthode send
entry_field.pack()
send_button = tkinter.Button(scene, text="enchere", command=send)
send_button.pack()
button = tkinter.Button (scene, text = "Quit", command = close_window)
button.pack()


HOST = input('Entrer host: ')
if not HOST:
    HOST= '192.168.56.1'
PORT = input('Entrer port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)


ADDR = (HOST, PORT)
try:
    client_socket = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
    client_socket.connect(ADDR)
    test = True
except :
    print("le serveur est offline")
    test = False
if test :
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
