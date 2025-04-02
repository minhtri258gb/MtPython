

import sqlite3
from flask import request, jsonify
import socket
import MtSystem

class MtNetwork:

	mt = None
	# dbPath = './res/database/api.sqlite'
	
	def __init__(self, _mt):
		self.mt = _mt
	
	def register(self):
		
		@self.mt.app.route("/network/check", methods=['GET'])
		def api_network_check():
			return self.api_check()
	
	def api_check(self):
		ip = '192.168.1.223'
		port = 9999

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result_connect = sock.connect_ex((ip, port))
		if result_connect == 0:
			res = "Port is open"
		else:
			res = "Port is not open"
		sock.close()

		return jsonify(res), 200
