import sqlite3
from flask import request, jsonify

class MtDynamic:
	
	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtDynamicDB()

	def register(self):

		@self.mt.app.route("/dynamic/list/<code>", methods=['POST'])
		def api_dynamic_list(code):
			return self.api_list(code)
		
		@self.mt.app.route("/dynamic/info/<code>", methods=['POST'])
		def api_dynamic_info(code):
			return self.api_info(code)

	def api_list(self, code):

		#TODO Check authenticate

		self.db.on()
		headers, rows = self.db.getDynamicList(code)
		self.db.off()

		return jsonify({
			"headers": headers,
			"rows": rows
		}), 200

	def api_info(self, code):
		print(code)
		pass


class MtDynamicDB:

	h_db_path = './res/database/dynamic.sqlite'

	def __init__(self):
		self.conn = None

	def on(self):
		if self.conn != None:
			self.off()
		self.conn = sqlite3.connect(self.h_db_path)

	def off(self):
		if self.conn != None:
			self.conn.close()
			self.conn = None

	def cbk_dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
	
	def getDynamicList(self, code):
		
		self.conn.row_factory = MtDynamicDB.cbk_dict_factory

		# Header
		sql = """
			SELECT LOWER(lc.code) key, lc.name value
			FROM list l
			LEFT JOIN list_col lc ON lc.list_id = l.id
			WHERE l.code = ?
			ORDER BY lc.seq
		"""
		param = [code]
		headers = self.conn.execute(sql, param).fetchall()

		# Rows
		sql = """
			SELECT id, code, name
			FROM list
		"""
		param = []
		rows = self.conn.execute(sql, param).fetchall()

		# Return
		return headers, rows

