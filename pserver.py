# *-* encoding: utf-8 *-*

import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65432

"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
	server.bind((HOST, PORT))
	server.listen()
"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
pseudo_noms = []

#--- Diffuse le message de chaque client 
def diffusion(message: str):
	for client in clients:
		client.send(message)


#--- Recoit les messages provenant d'un client
def reception():
	client, addr = server.accept()
	with client:
		print(f"Connecté avec: {addr}")
		while True:
			pseudo_nom = client.recv(1024)
			if not pseudo_nom:
				break
			client.send(pseudo_nom)

			pseudo_noms.append(pseudo_nom)
			clients.append(client)

			print(f"Le nom du client est {pseudo_nom}\n")
			diffusion(f"{pseudo_nom} est connecte au serveur.".encode("utf-8"))

			thread = threading.Thread(target = traitement, args = (client,))
			thread.start()

#--- Traitement
def traitement(client):
	while True:
		try:
			message = client.recv(1024)
			print(f"{pseudo_noms[clients.index(client)]} ...:> {message}")
			print("\n")
			diffusion(mesage)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()

			pseudo_nom = pseudo_noms[index]
			pseudo_noms.remove(pseudo_nom)
			break

if __name__ == "__main__":
	print("Serveur lancé...\n")

	reception()