# Comment marche le script ?

## Voici l'explication du fonctionnement du Scan réseau

#### Qu'est ce que le Scan-réseau ? Et bien c'est un script capable de faire un scan du réseau dans lequel il est lancé et de déterminer les adresse ip et mac associé à chaque machine
### Pour pouvoir executer le script, il va falloir suivre quelques étapes : 
-  Installer git
- Pull le repo git sur la machine depuis laquel on veut executer le script
- Executer le script sous forme de .py

#### Comment fonctionne l'outil ?
Le fonctionnement de l'outil est simple, il suffit d'executer le script pour pouvoir scanner notre réseau et ainsi avoir accès aux adresses : MAC, IP, découvrir des ports ouverts sur ces machines et enfin stocker un rapport, un compte-rendu des scans pour pouvoir consulter et sauvegarder le resultat du script directement sur noter machine dans le fichier Data.txt
Après avoir git pull et git le repo sur notre machine de cette manière :
```bash
git clone https://github.com/Chenishere/B2-reseau-2022-TP.git
git pull
cd B2-reseau-2022-TP
# Pour se deplacer dans le bon dossier puis :
cd TP5
# Maintenant nous sommes dans le bon dossier il ne manque plus qu'a exécuter le script : 
ynce@XchenHost TP5 % python3 Scan-Réseau.py | tee data.txt
WARNING: No IPv4 address found on en5 !
WARNING: No IPv4 address found on ap1 !
WARNING: more No IPv4 address found on awdl0 !
Rentrez votre nom :) : Chen
Bonjour Chen, voici un script permettant de scanner de réseau ⬇ 
⬇ Liste des appareils disponibles dans le réseau ⬇ :
Adresse IP          Adresse MAC
192.168.1.17        00:24:d4:7e:64:06
192.168.1.91        86:1c:ba:11:f8:97
192.168.1.108       00:1e:a6:d1:03:57
192.168.1.138       d4:61:9d:30:09:88
192.168.1.165       d2:48:45:a2:2c:c2
192.168.1.178       76:95:07:f2:f7:00
192.168.1.254       f4:ca:e5:58:55:65
```
- Ici, la commande "python3 Scan-Réseau.py | tee data.txt" permet d'executer le scan tout en sauvegardant son contenu dans le fichier data.txt

### Dernière étape, check si notre scan réseau a bien été enregistré :

- Dans le fichier Data.txt on retrouve ; 
```bash
Rentrez votre nom :) : Bonjour Chen, voici un script permettant de scanner de réseau ⬇ 
⬇ Liste des appareils disponibles dans le réseau ⬇ :
Adresse IP          Adresse MAC
192.168.1.17        00:24:d4:7e:64:06
192.168.1.91        86:1c:ba:11:f8:97
192.168.1.108       00:1e:a6:d1:03:57
192.168.1.138       d4:61:9d:30:09:88
192.168.1.165       d2:48:45:a2:2c:c2
192.168.1.178       76:95:07:f2:f7:00
192.168.1.254       f4:ca:e5:58:55:65
```
C'est bel est bien le contenenu du script que nous avons executé !

![Alt text](https://imageio.forbes.com/specials-images/imageserve/60427d207368a72e3811afd5/Happy-african-couple-shake-hand-of-insurer-buy-insurance-services/960x0.jpg?format=jpg&width=960)
