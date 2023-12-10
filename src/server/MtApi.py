import sqlite3
from flask import request, jsonify
import MtUtils

class MtApi:

	mt = None
	dbPath = './res/database/api.sqlite'
	
	def __init__(self, _mt):
		self.mt = _mt
	
	def register(self):
		
		@self.mt.app.route("/api/search", methods=['GET'])
		def api_api_search():
			return self.api_search()
	
	def api_search(self):

		# Query
		conn = sqlite3.connect(self.dbPath)
		conn.row_factory = MtUtils.cbk_dict_factory
		cursor = conn.execute("SELECT * FROM api")
		listAPI = cursor.fetchall()
		conn.close()

		# Return
		return jsonify(listAPI), 200
	