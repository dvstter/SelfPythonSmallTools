import socket
import struct
import math

class client:
	def init_client(self, address, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.connect((address.strip(), int(port)))
		except socket.error, e:
			print 'error:%s' % e 

	def main_loop(self):
		while True:
			cmd = raw_input('>')
			if cmd == 'quit':
				self.sock.send('quit')
				self.sock.close()
				break
			elif cmd == 'list':
				self.sock.send(cmd)
				result = self.sock.recv(1024)
				if result != '':
					print result,
			elif cmd[:5] == 'fetch':
				self.sock.send(cmd)
				self.get_file()
			else:
				print 'command did not recognised'

	def get_file(self):
		res = self.sock.recv(5)
		if res == 'error':
			print 'error occured...'
			return

		num_info = self.sock.recv(8)
		# recieve file size and file name size 
		file_size, filename_size = struct.unpack('2i', num_info)
		# recieve file name to create new file
		filename = self.sock.recv(filename_size)
		print 'fetching file %% destination:%s' % filename
		# open file to write 
		fid = open(filename, 'wb')
		for x in range(int(math.ceil(file_size/1024.0))):
			chunk = self.sock.recv(1024)
			fid.write(chunk)
		fid.close()
		print 'file transmitted over...'

if __name__ == '__main__':
	c = client()
#address = raw_input('ftp server ip address:')
#	port = raw_input('ftp server port number:')
	address = 'localhost'
	port = '8080'
	c.init_client(address=address, port=port)
	c.main_loop()
