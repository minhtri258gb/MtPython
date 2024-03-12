import sqlite3
from flask import request, jsonify

class MtDynamic:
	
	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtDynamicDB()

	def register(self):

		@self.mt.app.route("/dynamic/list/<name>", methods=['GET'])
		def api_dynamic_list(name):
			return self.api_list(name)
		
		@self.mt.app.route("/dynamic/info/<name>", methods=['GET'])
		def api_dynamic_info(name):
			return self.api_info(name)

	def api_list(self, name):
		print(name)
		pass

	def api_info(self, name):
		print(name)
		pass


class MtDynamicDB:

	h_db_path = './res/database/dynamic.sqlite'

	def __init__(self):
		self.conn = None

	def on(self):
		if self.conn != None:
			self.off()
		self.conn = sqlite3.connect(self.dbPath)

	def off(self):
		if self.conn != None:
			self.conn.close()
			self.conn = None

	def cbk_dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
