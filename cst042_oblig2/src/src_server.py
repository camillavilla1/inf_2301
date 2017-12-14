import socket, sys
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

HOST = 'localhost'
PORT = 8080


class Server(object):
	def __init__(self):
		# Create a new socket using the given address family, 
		# socket type and protocol number
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Set the value of the given socket option
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		#Bind the socket to address
		self.socket.bind((HOST, PORT))
		
	
	
	def rsa_encryption(self, conn):
		"""Recieve public (rsa)key"""
		rec_key = conn.recv(2048)
		self.pubkey = RSA.importKey(rec_key, None)
	
		
	
	def key_aes(self, conn):
		"""Generate symmetric AES key"""
		ran_key = Random.new()
		self.aes_key = ran_key.read(16)
		self.iv = Random.new().read(16)
		
		enc_key = self.pubkey.encrypt(self.aes_key + self.iv, 20)
		conn.send(enc_key[0])



	def send_msg(self, conn):
		"""Read the textfile, encrypt the message and sendt to client"""
		file_text = sys.argv[1]
		txtfile = open(file_text, 'r').read()
				
		cipher = AES.new(self.aes_key, AES.MODE_CFB, self.iv)
	
		msg = cipher.encrypt(txtfile)
		
		conn.send(msg)
	

		
	def run(self):
		self.socket.listen(5) #max # of quedued connections
		while 1:
			#conn - socket to client, addr - clients address
			conn, addr = self.socket.accept() 
			
			self.rsa_encryption(conn)
			self.key_aes(conn)
			self.send_msg(conn)
			
			
			#conn.send('Thank you for connecting\n')	#cannot open message if this is implemented
			print 'Got connection from: ', addr

			conn.close()
		
		
				
if __name__ == '__main__':
	server = Server()
	print "Server running..."
	server.run()
	
