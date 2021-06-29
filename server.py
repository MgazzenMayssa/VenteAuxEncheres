import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread , Timer
from datetime import datetime
import select,time,threading
enchéres = False #enchères
reference= "test"
Achetteur ="" 
debut_enchere= datetime.now()
prix = 0
global prixinit
participants =[]
fini = False
factures={}
#processus temps

class TestThreading(object):
    global debut_enchere
    global Achetteur
    global enchéres
    global participants
    global prix
    global prixinit
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global debut_enchere
        global Achetteur
        global enchéres
        global fini
        global participants
        while True:
            
            if ((datetime.now()-debut_enchere).seconds==20 and not fini):
                diffuserParticipant(bytes("ya monsieur l'enchere va se terminer dans 10 seconde !!!!" , "utf8"))
                fini = True
            if ((datetime.now()-debut_enchere).seconds>30): #enchere terminé
                bien = open("bien.txt","a")
                if (Achetteur!=""): #acheteur exist
                    diffuserParticipant(bytes("l'enchere est terminé ,%s gagnant." % Achetteur, "utf8"))
                    print("l'enchere est terminé ,%s gagnant." % Achetteur)
                    bien.write(strbien(reference,prixinit,prix,"Vendu",Achetteur+"\n"))
                    bien.close()
                    histo = open("histo.txt","a")
                    histo.write(strhisto(Achetteur,prix,"succes\n"))
                    histo.close()
                    #ajouter a factures
                    if (Achetteur not in list(factures.keys())):
                       fact = open("factures.txt","a")
                       fact.write(strfact(Achetteur,prix)+"\n")
                       fact.close()
                       factures[Achetteur]=prix
                    else : #achteur existe deja
                        factures[Achetteur]=factures[Achetteur]+prix
                        remplir()
                        
                    
                    enchéres = False
                    participants=[]
                    Achetteur=""
                    break
                
                else :  #pas d' acheteur . produit disponible
                    if enchéres:
                        diffuserParticipant(bytes("l'enchere est terminé sans gagnant", "utf8"))
                        print("l'enchere est terminé sans gagnant")
                        bien.write(strbien(reference,prixinit,prixinit,"Disponible","N/A\n"))
                        bien.close()
                        enchéres = False;
                        participants=[]
                        break
                    
                    
                enchéres = False;
                participants=[]
                break
                
            time.sleep(self.interval)   #endormir le client 

#proccessus menu
class menu(object):
    global debut_enchere
    global Achetteur
    global enchéres
    global reference
    global prix
    global prixinit
    global fini
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global debut_enchere
        global Achetteur
        global enchéres
        global fini
        global prix
        global prixinit
        global reference
        while True:
            # More statements comes here
            if not enchéres :
                print("1- nouvel enchere.")
                print("2-la liste des biens ")
                print("3-la facture d'un acheteur ")
                print("4-l'historique des propositions ")
                print("5- quitter")
                reponse = input()
                if (reponse =="1"):
                    reference = input("reference =")
                    prix = int(input("starting price = "))
                    prixinit= prix
                    enchéres = True
                    fini = False
                    histo = open("histo.txt","a")
                    histo.write("------------------\n")
                    histo.write("Produit "+reference+" :\n")
                    histo.close()
                    debut_enchere = datetime.now()
                    tr = TestThreading()
                    diffuser(bytes("un nouvel enchere a commencé : "+reference+str(prix), "utf8"))
                    diffuser(bytes("pour participer a la vente aux encheres tapez OKK ", "utf8"))
                    
                    print("en attente de connection...")
                elif (reponse=="2"):
                    bien = open("bien.txt","r")
                    l = bien.readlines()
                    for i in l :
                        print(i)
                    bien.close()
                elif (reponse=="3"):
                    ach =""
                    ach = input("donner le nom d'acheteur")
                    fact = open("factures.txt","r")
                    l = fact.readlines()
                    for i in l :
                        if i.split(" ")[0] == ach :
                            print(i)
                    fact.close()
                elif (reponse=="4"):
                    histo = open("histo.txt","r")
                    l = histo.readlines()
                    for i in l :
                        print(i)
                    histo.close()
                
                elif (reponse=="5"):
                      os._exit(0)
                else:
                    print("valeur erronéééééé !!! le numero doit etre entre 1 et 5")
                    
                
                
            time.sleep(self.interval)
            

def accepter_connexions():
    while True:
        try:
            client, client_address = SERVER.accept()
            client.send(bytes("veuillez entrer votre nom !","utf8"))
            addresses[client] = client_address
            Thread(target=gerer_client, args=(client,)).start()
        except:
            print("")
            break
def gerer_client(client):  
    nom = client.recv(1024).decode("utf8")
    global prix
    global Achetteur
    global debut_enchere
    global enchéres
    global fini
    if 1 :
        
        client.send(bytes('mar7bee %s! ' % nom, "utf8"))
        tr = TestThreading()
        if (enchéres):
            client.send(bytes('deja un enchere est en cours  :'+reference+"("+str(prix)+")\n", "utf8"))
            client.send(bytes("\n pour participer a la vente aux encheres tapez OKK ", "utf8"))
        else :
            client.send(bytes("pass d'enchere en cours, svp attendre un peu :) ", "utf8"))
           
        while True:
            
            clients[client] = nom
            msg = client.recv(1024)
            if enchéres:
                if msg == bytes("OKK", "utf8") and not joined(nom):
                    add(nom)
                    ms = "%s a rejoint l'enchere " % nom
                    diffuserParticipant(bytes(ms, "utf8"))
                    client.send(bytes(''+reference+", prix courant ("+str(prix)+") ,\n", "utf8"))
                    client.send(bytes("pour quitter taper Q ", "utf8"))
                    print(nom+" a rejoint l'enchere"); 
                   
                else :
                    if msg == bytes("OKK", "utf8") and joined(nom):
                        client.send(bytes("t'es deja dans l'enchere :p! ", "utf8"))
                if joined(nom):
                    try :
                        msgint=int(msg)
                        
                        if (msgint > prix): #prix valide
                            diffuserParticipant(msg,nom+" a proposé un noveau prix :")
                            
                            if (Achetteur!=""):
                                histo = open("histo.txt","a")
                                histo.write(strhisto(Achetteur,prix,"echec\n"))

                                histo.close()
                            
                            prix = msgint
                            Achetteur = nom
                            debut_enchere= datetime.now()
                            fini = False
                            print("dernier acheteur  : "+nom+"("+str(msgint)+"),"+debut_enchere.strftime("%H:%M:%S"))
                        else :
                            if msg != bytes("Q", "utf8"):
                                client.send(bytes("mauvaise offre!", "utf8"))
                    
                    except:
                        if (msg != bytes("Q", "utf8") and msg != bytes("OKK", "utf8")):
                            client.send(bytes("mauvaise entree !", "utf8"))
                
                if msg == bytes("Q", "utf8"):
                    if not joined(nom):
                        client.send(bytes("vous n'êtes pas dans une vente aux enchères !", "utf8"))
                    if Achetteur == nom and joined(nom):
                        client.send(bytes("vous ne pouvez pas quitter, vous êtes le dernier enchérisseur !", "utf8"))
                    if Achetteur != nom and joined(nom):
                        diffuserParticipant(bytes("%s a quitté l'enchere." % nom, "utf8"))
                        print(nom+"  a quitté l'enchere.")
                        client.send(bytes("pour participer a la vente aux encheres tapez OKK", "utf8"))
                        quit(nom)
                if not joined(nom) and msg != bytes("OKK", "utf8") and msg != bytes("Q", "utf8"):
                    client.send(bytes("vous n'êtes pas dans une vente aux enchères !", "utf8"))
            else :
                 client.send(bytes("Il n'y a pas d'enchère en cours, veuillez attendre une nouvelle enchère", "utf8"))
                
#diffuser un message a tous les client connectés
def diffuser(msg, prefix=""): 

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
#diffuser un message au clients participants
def diffuserParticipant(msg, prefix=""): 

    for sock in clients:
        if joined(clients[sock]):
            sock.send(bytes(prefix, "utf8")+msg)


#fonction qui retourne True si un client a rejoint la vente
def joined(nom):
    global participants
    for i in participants:
        if i==nom:
            return True
    return False
#fonction qui ajout un client a la liste des client joints
def add(nom):
    global participants
    participants.append(nom)

#l'inverse de add
def quit(nom):
    global participants
    participants.remove(nom)

#fonction pour lire les factures du fichier factures.txt et remplir le
#dictionnaire factures.
def remplirfactures():
    global factures
    fact = open("factures.txt","a")
    fact.close()
    fact = open("factures.txt","r")
    l = fact.readlines()
    fact.close()
    for i in l:
        nom = i.split(" ")[0]
        p = i.split(" ")[-1]
        if p[-1]=="\n":
            p = p[:-1]
        factures[nom]=int(p)

#fonction pour remplir le fichier factures apres mise a jour 
def remplir():
    global factures
    fact = open("factures.txt","a")
    fact.close()
    fact = open("factures.txt","w")
    for i in factures:
        fact.write(strfact(i,factures[i])+"\n")
    fact.close()

def strfact(a,b):
    ch = a
    for i in range (0,27-len(a)):
        ch=ch+" "
    ch = ch +str(b)
    return ch


def strbien(ref,p1,p2,t,bid):
    ch = ref
    for i in range (0,17-len(ref)):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    

        
    ch = ch+str(p1)
    for i in range (0,12-len(str(p1))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+str(p2)
    for i in range (0,15-len(str(p2))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+t
    for i in range (0,15-len(t)):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+bid
    return ch

def strhisto(bid,p,t):
    ch = Achetteur
    for i in range (0,20-len(bid)):
        ch=ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch + str(p)
    for i in range (0,12-len(str(p))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+t
    return ch


clients = {}
addresses = {}
HOST = '192.168.56.1'
PORT = 33000

ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
SERVER.bind(ADDR)

#SERVER.setblocking(0)
if __name__ == "__main__":
    while True :

        remplirfactures()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        m=menu()   
        
        SERVER.listen(10)
        ACCEPT_THREAD = Thread(target=accepter_connexions)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
