import socket
import xml.etree.ElementTree as ET


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



	def gen_msg(self, code, cont, func):
		"""Generate message for the differente codes"""
		self.msgcode = ' '
		if(code == 200 and func == 'PUT' or func == 'DELETE'):
			self.msgcode = 'HTTP/1.1 200 OK\r\nContent-type: text/xml\r\nContent-length: 0\r\nConnection: Close\r\n\r\n'
			return self.msgcode	
		elif(code == 200):
			self.msgcode = 'HTTP/1.1 200 OK\r\nContent-type: text/xml\r\nContent-length: '+ str(len(cont)) + '\r\nConnection: Close\r\n\r\n'+cont
			return self.msgcode		
		elif(code == 404):
			self.msgcode = 'HTTP/1.1 404 Not Found\r\nContent-type: text/xml\r\nConnection: Close\r\n\r\n'
			return self.msgcode	

		

	def recieve(self, conn):
		"""Recieve connection"""
		#recieve data from client and split the data into a list
		data = conn.recv(1024)		
		liste = data.split()		

		#Check if GET, POST, PUT or DELETE
		if(liste[0] == 'GET'):
			self.getfunc(liste, conn)
		elif(liste[0] == 'POST'):
			self.postfunc(liste, conn)
		elif(liste[0] == 'PUT'):
			self.putfunc(liste, conn)
		elif(liste[0] == 'DELETE'):
			self.delfunc(liste, conn)



	def getfunc(self, liste, conn):
		"""should return all messages in the XML format"""
		
		#(incase no) file is specified by the browser 
		if (liste[1] == '/messages'):
			path = '/test.xml'

		else:
			path = liste[1]

		try:	
			#open file and read it
			file_handler = open('.'+path, 'r')
			read_file = file_handler.read()
			respons_head = self.gen_msg(200, read_file, 'GET')
		except IOError:
			read_file = 'Not found'
			respons_head = self.gen_msg(404, 0)


		respons = respons_head + read_file
		conn.send(respons)

		file_handler.close()


		
	def postfunc(self, liste, conn):
		"""should store the field message of the request as a new message, give it a unique id
		store the new message with the id into the XML file, and return the id back to the client."""
		post_tree = ET.parse('test.xml')
		post_root = post_tree.getroot()
		
		#for post_child in post_root:
		#	print post_child.tag, post_child.attrib


		#give unique id
		un_id = 0
		for node1 in post_root:
			for node2 in post_root:
				if node1.attrib['id'] > node2.attrib['id']: 
					un_id = int(node1.attrib['id'])
				else:
					un_id = int(node2.attrib['id'])
		
		un_id += 1
		
		#new message 
		new_msg = liste[-1]
		new_msg = new_msg.strip('value="')
			
		#make new child from subelement
		new_child = ET.SubElement(post_root, "message", id=str(un_id), value=str(new_msg))
		post_tree.write('./test.xml')

		response = "id="+'"'+ str(un_id) +'"'
		send = self.gen_msg(200, response, 'POST')
		conn.send(send)



	def putfunc(self, liste, conn):
		"""should update message with the given id to contain the given message"""
		put_tree = ET.parse('test.xml')
		put_root = put_tree.getroot()
		
		old_id= liste[-2]
		old_id = old_id.strip('id="')
		
		old_val = liste[-1]
		old_val = old_val.split('"')
		
		#update the given id's message
		for node in put_root:
			if (node.attrib['id'] == old_id):
				node.attrib['value'] = old_val[1]
			
		put_tree.write('./test.xml')
		
		send = self.gen_msg(200, 0, 'PUT')
		conn.send(send) 
		
		

	def delfunc(self, liste, conn):
		"""should delete the message with the given id field"""
		del_tree = ET.parse('test.xml')
		del_root = del_tree.getroot()
		
		id1 = liste[-1]
		id1 = id1.strip('id="')  
		
		#delete the given id's message
		for node2 in del_root:
			print node2.attrib['id']
			if(int(node2.attrib['id']) == int(id1)):
				del_root.remove(node2)
		
		del_tree.write('./test.xml')
		
		send = self.gen_msg(200, 0, 'DELETE')
		conn.send(send)
	
	
	
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
