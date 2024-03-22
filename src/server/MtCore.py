import os
import socket
import secrets
import base64
from flask import request, jsonify, send_from_directory
from flask_swagger import swagger
import MtConfig
import MtSystem

state = False

class MtCore:

	mt = None

	def __init__(self, mt):
		self.mt = mt

	def register(self):

		statis_path = os.getenv('DIR_STATIC')
		
		@self.mt.app.route('/')
		def api_home_page():
			return send_from_directory(statis_path, path="./home/index.html")

		@self.mt.app.route('/<appName>')
		@self.mt.app.route('/<appName>/')
		def api_app_page(appName):
			try:
				appName = appName.lower()
				if appName not in MtConfig.list_app:
					return "App not found"

				fullpath = statis_path + appName
				if (os.path.exists(fullpath) and os.path.isdir(fullpath)):
					return send_from_directory(statis_path, path=appName+"/index.html")
				
			except Exception as e:
				print(type(e), e)
				return "App not found"

		@self.mt.app.route("/authorize", methods=['POST'])
		def api_authorize():
			password = request.form.get('password')
			result = (password == '-1393153393')
			token = ""
			if result:
				token_bytes = secrets.token_bytes(25) # Gen key
				token_b64 = base64.b64encode(token_bytes) # To Base64
				token = token_b64.decode('ascii') # To String
				MtSystem.auth_set(token)
			return jsonify({"result": result, "token": token}), 200
		
		@self.mt.app.route("/docs")
		def api_doc_page():
			return jsonify(swagger(self.mt.app)), 200
		
		@self.mt.app.route('/common/getListApplication')
		def api_common_get_list_application():
			return jsonify(MtConfig.list_app), 200

		@self.mt.app.route('/common/getIPLocal')
		def api_common_get_ip_local():
			if not MtSystem.auth_check(request.args.get('token')):
				return "Access denied", 403
			return jsonify(self.getHost()), 200

	def getHost(self):
		hostname = socket.gethostname()
		return socket.gethostbyname(hostname)
	