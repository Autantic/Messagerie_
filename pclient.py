#*.* coding: utf-8 *.*

import sys
import socket
import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 65432

class Messagerie():
	def __init__(self, host, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((host, port))

		fen = tkinter.Tk()
		fen.withdraw()

		self.pseudo_nom = simpledialog.askstring("Utilisateur", "Non d'utilisateur", parent = fen)
		self.gui_done = False
		self.exec = True

		gui_thread = threading.Thread(target = self.send_message)
		rec_thread = threading.Thread(target = self.rec_message)
		gui_thread.start()
		rec_thread.start()


	def send_message(self):
		self.win = tkinter.Tk()
		self.win.configure(bg = "lightgray")

		self.chat_label = tkinter.Label(self.win, text = "Chat:", bg = "lightgray")
		self.chat_label.config(font = ("Arial", 12))
		self.chat_label.pack(padx = 20, pady = 5)

		self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
		self.text_area.pack(padx = 20, pady = 5)
		self.text_area.config(state = "disabled") 

		self.msg_label = tkinter.Label(self.win, text = "Message:", bg = "lightgray")
		self.chat_label.config(font = ("Arial", 12))
		self.chat_label.pack(padx = 20, pady = 5)

		self.input_area = tkinter.Text(self.win, height = 3)
		self.input_area.pack(padx = 20, pady = 5)

		self.send_button = tkinter.Button(self.win, text = "Send", command = self.write)
		self.send_button.config(font = ("Arial", 12))
		self.send_button.pack(padx = 20, pady = 5)

		self.gui_done = True

		self.win.protocol("WM_DELETE_WINDOW", self.stop)

		self.win.mainloop()

	def write(self):
		message = f"{self.pseudo_nom}: {self.input_area.get('1.0', 'end')}"
		self.client.send(message.encode("utf-8"))
		self.input_area.delete('1.0', 'end')


	def stop(self):
		self.exec = False
		self.win.destroy()
		self.client.close()
		exit(0)

	def rec_message(self):
		while self.exec:
			try:
				message = self.client.recv(1024)
				if message == "NICK":
					self.client.send(self.pseudo_nom.encode("utf-8"))
				else:
					if self.gui_done:
						self.text_area.config(state = "normal")
						self.text_area.insert("end", message)
						self.text_area.yview("end")
						self.text_area.config(state = "disabled")
			except:
				print("Error")
				self.client.close()
				break

client = Messagerie(HOST, PORT)
