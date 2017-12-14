import socket, sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

			
class Client(object):
	def __init__(self, ):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# Create a socket object
		
	
	def rsa_pub_key(self):
		"""Generate new RSA-key, send public key to server"""
		self.new_key = RSA.generate(2048)			#contain public- and private key
		
		self.public_key = self.new_key.publickey()		
		new_pubkey = open("pem.pem", 'w')			#make new pem-file for public key
		new_pubkey.write(self.public_key.exportKey("PEM"))	#write the public key to the file
		new_pubkey.close()
		
		open_pem = open("pem.pem", 'r')
		pub_key = open_pem.read()	
		open_pem.close()
		
		self.socket.send(pub_key)



	def get_aeskey(self):
		"""Get AES key from server. Decrypt it"""
		self.aeskey = self.socket.recv(4096)
		self.decr_aes = self.new_key.decrypt(self.aeskey)[:16]	#decrypt with pub/sec key
		self.iv = self.new_key.decrypt(self.aeskey)[16:]

		

	def new_text(self):
		"""Get text from the server and opens new text file for the message"""
		self.data = self.socket.recv(4096)

		new_txtfile = open("text_client.txt", 'w')
		new_txtfile.write(self.data)
		
		new_txtfile.close()

		
	
	def get_msg(self):
		"""Get message from server, decrypt message and put it in new document"""
		cipher = AES.new(self.decr_aes, AES.MODE_CFB, self.iv)
		
		dec_msg = cipher.decrypt(self.data)
	
		new_msg = open("text_client.txt", 'a')
		new_msg.write(dec_msg)


	
	def run(self, host="localhost", port=8080):
		host = sys.argv[1]
		port = int(sys.argv[2])
		self.socket.connect((host, port))
		
		self.rsa_pub_key()
		self.get_aeskey()
		self.new_text()
		self.get_msg()
		

				
if __name__ == '__main__':
	client = Client()
	print "Client running..."
	client.run()
	
