import socket
import os
import struct
import math

class file_info:
	def __init__(self, file_desc, location):
		self.file_desc = file_desc # file desc for ftp server
		self.location = location # the file's fully address
		self.basename = os.path.basename(self.location)
		self.size = os.path.getsize(self.location)
	def __str__(self):
		return self.file_desc

class server:
	def __init__(self):
		self.files = []
		self.count = 1
		self._init_server()

	def _init_server(self, maxconnection=10, folder=''):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('localhost', 8080))
		self.sock.listen(maxconnection)
		self._set_server()
		self.get_connection()

	def get_connection(self):
		self.connection, temp = self.sock.accept()
		self.client_addr = temp[0] # get client addr
		self.client_port = temp[1] # get client port 
		print 'get connection from %s:%i' % (self.client_addr, self.client_port)

	def release_connection(self):
		self.connection.close()
		print 'release connection from %s:%i' % (self.client_addr, self.client_port)
	
	def _visit_func(self, arg, dirname, names):
		for each in names:
			if os.path.isdir(os.path.abspath(dirname)+'/'+each):
				continue # jump over dirs 
			# construct new file info
			new_file = file_info('%d -- %s' % (self.count, each), os.path.abspath(dirname)+'/'+each)
			self.files += [new_file, ]
			self.count += 1

	def _set_server(self): # set info for this ftp server
		#print 'share file folder must be under this directory'
		#print 'must use relative address'
		#folder = raw_input('input share file folder:')
		folder = './ftp_share'
		while True:
			if os.path.isdir(folder):
				break
			print 'the file folder is not exists...'
			folder = raw_input('re-input share file folder:')
		self.folder = folder
		os.path.walk(self.folder, self._visit_func, None)

	############# end for private function ##########################

	def main_loop(self):
		while True:
			cmd = self.connection.recv(1024)
			if cmd == 'list':
				self.do_list()
			elif cmd[:5] == 'fetch':
				self.do_fetch(int(cmd.split(' ')[1]))
			elif cmd == 'quit':
				# clear data and re-connect
				self.release_connection()
				self.get_connection()
			else:
				pass # unrecognised command, leave it alone

	def close(self):
		try:
			self.connection.close()
			self.sock.close()
		except AttributeError:
			pass

	# command process function
	def do_list(self):
		print '%s:%i is listing files' % (self.client_addr, self.client_port)
		for each in self.files:
			self.connection.send('%s\n' % each)
	def do_fetch(self, file_id):
		file_id -= 1
		if file_id >= len(self.files):
			self.connection.send('error')
			return
		print '%s:%i is fetching file %% filename:%s' % (self.client_addr, self.client_port, self.files[file_id].basename)
		self.connection.send('ready')
		# open file, ready to transmit
		fid = open(self.files[file_id].location, 'rb')
		# get file info
		file_size = self.files[file_id].size
		base_name = self.files[file_id].basename
		# send file size and file name size
		self.connection.send(struct.pack('2i', file_size, len(base_name)))
		# send file name
		self.connection.send(base_name)
		for x in range(int(math.ceil(file_size/1024.0))):
			chunk = fid.read(1024) # read 1024 bytes
			self.connection.send(chunk)
		# send file
		
		print '%s:%i fetched file over %% filename:%s' % (self.client_addr, self.client_port, self.files[file_id].basename)
		fid.close()

if __name__ == '__main__':
	try:
		s = server()
		s.main_loop()	
	finally:
		s.close();

