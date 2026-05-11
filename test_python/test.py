#!/usr/bin/env python3
from netmiko import ConnectHandler
import re

serv_web = {
    'device_type' : 'linux',
    'ip' : '192.168.3.2',
    'username' : 'utilisateur',
    'password' : 'toor',
    'port' : 22,
    'verbose' : False # Mis à False pour un affichage plus propre, mets True pour débugger
}

# 1. Connexion
connection = ConnectHandler(**serv_web)

# 2. Test de connectivité (PING)
print(">>> Serv_Web : Test de connectivité vers 8.8.8.8")
test_ping = connection.send_command('ping -c 4 -W 1 8.8.8.8')
print(test_ping)

capture_ping = re.search(r'(\d+) \w+ \w+, (\d+) \w+, (\d+)% \w+ \w+, time (\d+)ms', test_ping)

if capture_ping and capture_ping.group(1) == capture_ping.group(2):
    print("+++ Ping réalisé avec succès")
else:
    print("xxx Problème de connectivité IP")
    connection.disconnect()
    exit(-1)

# 3. Test de résolution DNS (NSLOOKUP)
print("\n>>> Serv_Web : Test de résolution DNS (www.google.fr)")
test_dns = connection.send_command('nslookup -timeout=1 www.google.fr')
print(test_dns)

# On cherche "Server:" suivi d'espaces/tabs et de l'IP
capture_dns = re.search(r'Server:\s+(\d+\.\d+\.\d+\.\d+)', test_dns)

if capture_dns:
    dns_ip = capture_dns.group(1)
    print(f"+++ Résolution DNS fonctionnelle via le serveur : {dns_ip}")
else:
    print("xxx Erreur : Impossible de résoudre le nom de domaine")
    connection.disconnect()
    exit(-2)
    
# --- Nouveau Test : Serveur Web Local ---

print("\n>>> Serv_Web : Test du serveur Web en local (wget)")
# On tente de télécharger l'index
test_web = connection.send_command('wget --timeout 1 -t 1 127.0.0.1')
print(test_web)

# On vérifie si la réponse contient "index.html" sauvegardé ou "200 OK"
if "index.html" in test_web or "200 OK" in test_web:
    print("+++ Serveur Web local fonctionnel (index.html accessible)")
else:
    print("xxx Erreur : Le serveur Web ne répond pas en local")
    connection.disconnect()
    exit(-3)
# 4. Fermeture propre
connection.disconnect()
print("\n--- Tous les tests sont validés ---")