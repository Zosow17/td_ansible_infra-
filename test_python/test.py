#!/usr/bin/env python3
# Indique l'outil à utiliser pour lancer ce script
# Importe l'objet permettant de faire une connection ssh avec netmiko
from netmiko import ConnectHandler
# Gestion des expression régulières
import re
# Dictionnaire avec paramètres pour se connecter à notre serveur web
serv_web = {
'device_type' : 'linux',
'ip' : '192.168.3.2',
'username' : 'utilisateur',
'password' : 'toor',
'port' : 22,
'verbose' : True
}
# Réalise la connection ssh avec le serveur Linux
connection = ConnectHandler(**serv_web)
# Envoi la commande ping pour tester si on peut joindre le 8.8.8.8 depuis le serveur web
test = connection.send_command('ping -c 4 -W 1 8.8.8.8')
# Affiche le résultat du test
print(">>> Serv_Web : Test de connectivité serveur Linux vers extérieur (dns google)")
print(test)
# Exemple de résultat :
# 4 packets transmitted, 4 received, 0% packet loss, time 3005ms
# Recherche en capturant les éléments entre parenthèse sous la forme
# (chiffres_répétés) lettre_répété lettre_répeté, ...
capture=re.search(r'(\d+) \w+ \w+, (\d+) \w+, (\d+)% \w+ \w+, time (\d+)ms',test)
# Les éléments sont stocké dans capture.group(1), capture.group(2) ...
# capture.group (1) correspond au paquets transmis et capture.groupe(2) au reçu
if capture.group(1)==capture.group(2):
    print("+++ Test réalisé avec succès")
else:
    print("xxx Problème de connectivité")
    exit(-1)