# TP3 : On va router des trucs

## I. ARP

### 1. Echange ARP

🌞**Générer des requêtes ARP**
```
[ynce@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=64 time=0.338 ms
[ynce@localhost ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=0.524 ms

```
```
[ynce@localhost ~]$ ip neigh show | grep 10.3.1.12
10.3.1.11 dev enp0s3 lladdr 08:00:27:28:cf:36 REACHABLE
[ynce@localhost ~]$ ip neigh show | grep 10.3.1.11
10.3.1.12 dev enp0s3 lladdr 08:00:27:a8:a9:56 REACHABLE
```
- ' | grep '  permet d'isoler uniquement les elements que l'on veut pour avoir des recherches plus precises !

- L'adresse MAC de John est `08:00:27:28:cf:36`
```
#PC de John
[ynce@localhost ~]$ ip a | grep link/ether
    link/ether 08:00:27:28:cf:36 brd ff:ff:ff:ff:ff:ff
```

- L'adresse MAC de Marcel est `08:00:27:a8:a9:56`
```
#PC de Marcel
[ynce@localhost ~]$ ip a | grep link/ether
    link/ether 08:00:27:a8:a9:56 brd ff:ff:ff:ff:ff:ff
```

### 2. Analyse de trames

🌞**Analyse de trames**

```
[ynce@localhost ~]$ sudo ip neigh flush all
[ynce@localhost ~]$ sudo tcpdump -i enp0s3 -c 2 -w arp.pcap not port 22
dropped privs to tcpdump
tcpdump: listening on enp0s3, link-type EN10MB (Ethernet), snapshot length 262144 bytes
2 packets captured
```

🦈 **Capture réseau `tp3_arp.pcapng`** qui contient un ARP request et un ARP reply

## II. Routage

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

```
[ynce@localhost ~]$ sudo firewall-cmd --list-all
[sudo] password for ynce: 
public (active)
[...]
[ynce@localhost ~]$ sudo firewall-cmd --get-active-zone
public
  interfaces: enp0s3 enp0s8
[ynce@localhost ~]$ sudo firewall-cmd --add-masquerade --zone=public
success
[ynce@localhost ~]$ sudo firewall-cmd --add-masquerade --zone=public --permanent
success
```


🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

- PC de John
```
[ynce@localhost ~]$ sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3
[ynce@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.3.1.254
NETMASK=255.255.255.0
[ynce@localhost ~]$ sudo systemctl restart NetworkManager
[ynce@localhost ~]$ ip a | grep 10.3.1.254
    inet 10.3.1.254/24 brd 10.3.1.255 scope global noprefixroute enp0s3
```

- PC de Marcel
```
[ynce@localhost ~]$ sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3
[ynce@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.3.2.254
NETMASK=255.255.255.0
[ynce@localhost ~]$ sudo systemctl restart NetworkManager
[ynce@localhost ~]$ ip a | grep 10.3.2.254
    inet 10.3.2.254/24 brd 10.3.2.255 scope global noprefixroute enp0s3
```

### 2. Analyse de trames

🌞**Analyse des échanges ARP**

- vidage des tables ARP sur les 3 noeuds :
```
[ynce@localhost ~]$ sudo ip neigh flush all
```
- `ping` de John vers Marcel :
```
[ynce@localhost ~]$ ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=1.95 ms
```

| ordre | type trame  | IP source | MAC source                  | IP destination | MAC destination             |
|-------|-------------|-----------|-----------------------------|----------------|-----------------------------|
| 1     | Requête ARP | x         |`John` `08:00:27:28:cf:36`   | x              | Broadcast `FF:FF:FF:FF:FF`  |
| 2     | Réponse ARP | x         |`routeur` `08:00:27:d4:05:3e`| x              | `John` `08:00:27:28:cf:36`  |
| 1     | Requête ARP | x         |`routeur` `08:00:27:7a:0e:51`| x              | Broadcast `FF:FF:FF:FF:FF`  |
| 2     | Réponse ARP | x         |`Marcel` `08:00:27:a8:a9:56` | x              |`routeur` `08:00:27:7a:0e:51`|
| ?     | Ping        |`10.3.1.11`|`John` `08:00:27:28:cf:36`   |`10.3.2.12`     |`Marcel` `08:00:27:a8:a9:56` |
| ?     | Pong        |`10.3.2.12`|`Marcel` `08:00:27:a8:a9:56` |`10.3.1.11`     |`John` `08:00:27:28:cf:36`   |



🦈 **Capture réseau `tp3_routage_marcel.pcapng`**

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

- ajoutez une carte NAT en 3ème inteface sur le `router` pour qu'il ait un accès internet
```
[ynce@localhost ~]$ ip a | grep enp0s9
    inet 10.0.4.15/24 brd 10.0.4.255 scope global dynamic noprefixroute enp0s9
```
- ajoutez une route par défaut à `John` et `marcel` :

```
#Fonctionne sur PC John et Marcel
[ynce@localhost ~]$ cat /etc/sysconfig/network
GATEWAY=10.0.4.2
[ynce@localhost ~]$ sudo systemctl restart NetworkManager
[ynce@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=53.4 ms
```

- donnez leur aussi l'adresse d'un serveur DNS qu'ils peuvent utiliser :
```
#Manip sur PC John et Marcel
[ynce@localhost ~]$ sudo echo "DNS=1.1.1.1" >> /etc/sysconfig/network-scripts/ifcfg-enp0s3
[ynce@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 | grep DNS
DNS=1.1.1.1
[ynce@localhost ~]$ sudo systemctl restart NetworkManager

[ynce@localhost ~]$ dig gitlab.com | head -n 14 | tail -n 1
gitlab.com.             236     IN      A       172.65.251.78

[ynce@localhost ~]$ ping gitlab.com
PING gitlab.com (172.65.251.78) 56(84) bytes of data.
64 bytes from 172.65.251.78 (172.65.251.78): icmp_seq=1 ttl=61 time=36.6 ms
```

🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john` :
```
[ynce@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=160 ms
```

- capturez le ping depuis `John` avec `tcpdump` :

🦈 **Capture réseau `tp3_routage_internet.pcapng`**

- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source               | IP destination   | MAC destination          |     |
|-------|------------|--------------------|--------------------------|------------------|--------------------------|-----|
| 1     | ping       |`John` `10.3.1.11`  |`John` `08:00:27:28:cf:36`| `8.8.8.8`        |`08:00:27:d4:05:3e`       |     |
| 2     | pong       |`8.8.8.8`           |`08:00:27:d4:05:3e`       |`John` `10.3.1.11`|`John` `08:00:27:28:cf:36`| ... |

## III. DHCP


### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** 

- Installation du serveur sur `john` :
```
[ynce@localhost ~]$ sudo dnf install dhcp-server -y
```

- Création d'une machine `bob` + récupérer une IP en DHCP à l'aide de votre serveur :
```
[ynce@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 
NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=dhcp
ONBOOT=yes

[ynce@localhost ~]$ sudo systemctl restart NetworkManager
[ynce@localhost ~]$ ip a | grep dynamic
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s3
```

🌞**Améliorer la configuration du DHCP**

- ajoutez de la configuration à votre DHCP pour qu'il donne aux clients, en plus de leur IP :

**route par défaut**
```
[ynce@localhost ~]$ sudo cat /etc/dhcp/dhcpd.conf | grep routers
option routers 10.3.1.254;
```

**serveur DNS à utiliser**
```
[ynce@localhost ~]$ sudo cat /etc/dhcp/dhcpd.conf | grep domain
option domain-name-servers 1.1.1.1;
```


- récupérez de nouveau une IP en DHCP sur `marcel` pour tester :

**Vérification IP Marcel + ping gateway**
```
[ynce@localhost ~]$ ip a | grep dynamic
    inet 10.3.1.4/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8

[ynce@localhost ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.743 ms
```

**Vérif route par défaut Marcel**
```
[ynce@localhost ~]$ ip route
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.4 metric 101

[ynce@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=58.8 ms
```

**Vérif serveur DNS**
```
[ynce@localhost ~]$ dig gitlab.com | head -n 14 | tail -n 1
gitlab.com.             290     IN      A       172.65.251.78

[ynce@localhost ~]$ ping gitlab.com
PING gitlab.com (172.65.251.78) 56(84) bytes of data.
64 bytes from 172.65.251.78 (172.65.251.78): icmp_seq=1 ttl=61 time=37.5 ms
```

### 2. Analyse de trames

🌞**Analyse de trames**

```
#PC John
[ynce@localhost ~]$ sudo tcpdump -i enp0s3 -c 10 -w test.pcap not port 22
```
```
#PC bob
[ynce@localhost ~]$ sudo dhclient -r enp0s3
[ynce@localhost ~]$ sudo dhclient enp0s3
```

![alt text](https://sm.ign.com/t/ign_fr/news/l/live-actio/live-action-cowboy-bebop-series-headed-to-netflix_7ftq.1280.jpg)
