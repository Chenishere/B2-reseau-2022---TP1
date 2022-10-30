# TP4 : TCP, UDP et services réseau

Dans ce TP on va explorer un peu les protocoles TCP et UDP. On va aussi mettre en place des services qui font appel à ces protocoles.

# 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. 1Go RAM c'est large large. Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Les firewalls de vos VMs doivent **toujours** être actifs (et donc correctement configurés).

➜ **Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

# I. First steps

Faites-vous un petit top 5 des applications que vous utilisez sur votre PC souvent, des applications qui utilisent le réseau : un site que vous visitez souvent, un jeu en ligne, Spotify, j'sais po moi, n'importe.

```
1 - Spotify
2 - Discord
3 - Chrome
4 - Twitch
5 - Youtube
```

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

- avec Wireshark, on va faire les chirurgiens réseau
- déterminez, pour chaque application :
  - IP et port du serveur auquel vous vous connectez
  - le port local que vous ouvrez pour vous connecter

```
1 - Spotify : ↓
IP + port serveur => 35.186.224.40:443 /  port local : 49570
2 - Discord : ↓
IP + port serveur => 162.159.136.234:443 / port local : 40472
3 - Chrome : ↓
IP + port serveur => 66.22.199.20:443 /  port local : 62624
4 - Twitch : ↓
IP + port serveur => 52.223.198.2:443 /  port local : 52113
5 - Youtube : ↓
IP + port serveur => 91.68.245.15:443 /  port local : 53363
```

🌞 **Demandez l'avis à votre OS**

- votre OS est responsable de l'ouverture des ports, et de placer un programme en "écoute" sur un port
- il est aussi responsable de l'ouverture d'un port quand une application demande à se connecter à distance vers un serveur
- bref il voit tout quoi
- utilisez la commande adaptée à votre OS pour repérer, dans la liste de toutes les connexions réseau établies, la connexion que vous voyez dans Wireshark, pour chacune des 5 applications

```
ynce@XchenHost:~$ ss -tpn | grep spotify                                    
ESTAB 0      0       10.33.17.218:49570 35.186.224.40:443    users:(("spotify",pid=20078,fd=32)) 
[...]
ynce@XchenHost:~$ ss -tpn | grep Discord
ESTAB 0      0       10.33.17.218:42690 162.159.136.234:443  users:(("Discord",pid=20618,fd=34))
[...]
ynce@XchenHost:~$ ss -tpn | grep prospect
ESTAB 0      0       10.33.17.218:56436   52.97.212.82:443  users:(("chrome",pid=21202,fd=26))
#Twitch
ynce@XchenHost:~$ ss -tpn | grep chrome
ESTAB 73     0       10.33.17.218:58370  216.58.213.74:443  users:(("chrome",pid=19424,fd=66))
#Youtube
ynce@XchenHost:~$ ss -tpn | grep chrome
ESTAB      0      0       10.33.17.218:38506 142.250.74.246:443  users:(("chrome",pid=19424,fd=53))
```

**Il faudra ajouter des options adaptées aux commandes pour y voir clair. Pour rappel, vous cherchez des connexions TCP ou UDP.**

```
# MacOS
$ netstat

# GNU/Linux
$ ss

# Windows
$ netstat
```

🦈🦈🦈🦈🦈 **Bah ouais, captures Wireshark à l'appui évidemment.** Une capture pour chaque application, qui met bien en évidence le trafic en question.

# II. Mise en place

Allumez une VM Linux pour la suite.

## 1. SSH

Connectez-vous en SSH à votre VM.

🌞 **Examinez le trafic dans Wireshark**

- donnez un sens aux infos devant vos yeux, capturez un peu de trafic, et coupez la capture, sélectionnez une trame random et regardez dedans, vous laissez pas brainfuck par Wireshark n_n
- **déterminez si SSH utilise TCP ou UDP**
  - pareil réfléchissez-y deux minutes, logique qu'on utilise pas UDP non ?
- **repérez le *3-Way Handshake* à l'établissement de la connexion**
  - c'est le `SYN` `SYNACK` `ACK`
- **repérez le FIN FINACK à la fin d'une connexion**
- entre le *3-way handshake* et l'échange `FIN`, c'est juste une bouillie de caca chiffré, dans un tunnel TCP

🌞 **Demandez aux OS**

- repérez, avec un commande adaptée, la connexion SSH depuis votre machine
- ET repérez la connexion SSH depuis votre VM

```
# MacOS
$ netstat

# GNU/Linux
$ ss

# Windows
$ netstat
```

🦈 **Je veux une capture clean avec le 3-way handshake, un peu de trafic au milieu et une fin de connexion**

## 2. NFS

Allumez une deuxième VM Linux pour cette partie.

Vous allez installer un serveur NFS. Un serveur NFS c'est juste un programme qui écoute sur un port (comme toujours en fait, oèoèoè) et qui propose aux clients d'accéder à des dossiers à travers le réseau.

Une de vos VMs portera donc le serveur NFS, et l'autre utilisera un dossier à travers le réseau.

🌞 **Mettez en place un petit serveur NFS sur l'une des deux VMs**

- j'vais pas ré-écrire la roue, google it, ou [go ici](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=nfs&f=1)
- partagez un dossier que vous avez créé au préalable dans `/srv`
- vérifiez que vous accédez à ce dossier avec l'autre machine : [le client NFS](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=nfs&f=2)

> Si besoin, comme d'hab, je peux aider à la compréhension, n'hésitez pas à m'appeler.

🌞 **Wireshark it !**

- une fois que c'est en place, utilisez `tcpdump` pour capturer du trafic NFS
- déterminez le port utilisé par le serveur

🌞 **Demandez aux OS**

- repérez, avec un commande adaptée, la connexion NFS sur le client et sur le serveur

```
# GNU/Linux
$ ss
```

🦈 **Et vous me remettez une capture de trafic NFS** la plus complète possible. J'ai pas dit que je voulais le plus de trames possible, mais juste, ce qu'il faut pour avoir un max d'infos sur le trafic

## 3. DNS

🌞 Utilisez une commande pour effectuer une requête DNS depuis une des VMs

- capturez le trafic avec un `tcpdump`
- déterminez le port et l'IP du serveur DNS auquel vous vous connectez
