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
# Maintenant nous sommes dans le bon dossier il ne manque plus qu'a exécuter le script 
python3 Scan-Réseau.py
```
