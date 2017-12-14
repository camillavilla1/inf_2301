import socket


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



	def gen_msg(self, code, cont_len):
		self.msgcode = ' '
		if(code == 200):
			self.msgcode = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\nContent-length: '+ str(cont_len) + '\r\nConnection: Close\r\n\r\n'
		elif(code == 404):
			self.msgcode = 'HTTP/1.1 404 Not Found\r\nContent-type: text/html\r\nConnection: Close\r\n\r\n'
		print self.msgcode
		return self.msgcode

		

	def recieve(self, conn):
		"""Recieve connection"""
		#recieve data from client, split the data into a list
		data = conn.recv(1024)		
		liste = data.split()		

		#Check if GET- og POST-income
		if(liste[0] == 'GET'):
			self.getfunc(liste, conn)
		elif(liste[0]== 'POST'):
			self.postfunc(liste, conn)



	def getfunc(self, liste, conn):
		"""should be implemented to open the file at the path from the URL"""
		
		#incase no file is specified by the browser
		if (liste[1] == '/'):
			path = '/index.html'

		else:
			path = liste[1]

		try:
			#open file and read it	
			file_handler = open('.'+path, 'r')
			read_file = file_handler.read()
			respons_head = self.gen_msg(200, len(read_file))
		except IOError:
			read_file = 'Not found'
			respons_head = self.gen_msg(404, 0)


		respons = respons_head + read_file
		conn.send(respons)



	def postfunc(self, liste, conn):
		"""should be implemented to write the input data into the file given in the URL (path)"""
		
		file_reader = open(liste[1][1:], 'w')
		
		file_reader.write(liste[-1])
		cont_len = len(liste[-1])
		print "Length of body in POST: ", cont_len
		
		respons2 = self.gen_msg(404, 0) + liste[-1]
		conn.send(respons2)



	def run(self):
		self.socket.listen(5) #max # of quedued connections
		while 1:
			#conn - socket to client, addr - clients address
			conn, addr = self.socket.accept() 

			self.recieve(conn)
			print 'Got connection from: ', addr

			conn.close()



if __name__ == '__main__':
	server = Server()
	server.run()
