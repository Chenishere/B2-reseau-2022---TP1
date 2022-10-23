import subprocess
from scapy.all import ARP, Ether, srp

# Voici l'entrée du script ou ont doit choisir un pseudo pour pouvoir executer le scan réseau

name = input("Rentrez votre nom :) : ")

# Si le champ "Name" est vide alors il y'a une erreur

if name == '':
    print("Erreur, veuillez selectionner un Nom :c")
    exit()
else:

# Sinon le script s'execute !

    Description_text = f"Bonjour {name}, voici un script permettant de scanner de réseau ⬇ "
Txt = Description_text
print(Txt)
process = subprocess.Popen(['echo', 'More output'],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr
(b'More output\n', b'')
# Le script Ici ⬇⬇⬇⬇

target_ip = "192.168.1.1/24"

# Création d'un packet arp
arp = ARP(pdst=target_ip)

ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

# Boucle pour accueillir une liste de client
clients = []

for sent, received in result:

    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# Afficher le client
print("⬇ Liste des appareils disponibles dans le réseau ⬇ :")
print("Adresse IP" + " "*10+"Adresse MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))


