import sqlite3
from flask import request, jsonify

class MtDynamic:
	
	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtDynamicDB()

	def register(self):

		@self.mt.app.route("/api/dynamic/list", methods=['POST'])
		def api_dynamic_list():
			return self.api_list()
		
		@self.mt.app.route("/api/dynamic/info", methods=['POST'])
		def api_dynamic_info():
			return self.api_info()

	def api_list(self):

		#TODO Check authenticate

		args = request.get_json()

		self.db.on()
		try:
			result = self.db.getDynamicList(args)
			result_code = 200
		except Exception as e:
			result = str(e)
			result_code = 500
		self.db.off()

		return jsonify(result), result_code

	def api_info(self):
		
		#TODO Check authenticate

		args = request.get_json()
		
		self.db.on()
		try:
			result = self.db.getDynamicInfo(args)
			result_code = 200
		except Exception as e:
			result = str(e)
			result_code = 500
		self.db.off()

		return jsonify(result), result_code


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
	
	def query(self, sql, params):
		return self.conn.execute(sql, params).fetchall()
	
	def getDynamicList(self, args):
		
		self.conn.row_factory = MtDynamicDB.cbk_dict_factory

		pageCode = args["page"]

		# Detail List
		sql = """
			SELECT id, code, name, query FROM list WHERE code = ?
		"""
		params = [pageCode]
		details = self.query(sql, params)
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		detail = details[0]
		listId = detail['id']

		# Header
		sql = """
			SELECT LOWER(code) key, name value
			FROM list_col
			WHERE list_id = ?
			ORDER BY seq
		"""
		params = [listId]
		headers = self.query(sql, params)

		# Rows
		sql = detail['query']
		print(sql)
		# while True:
		# 	posb = sql.index('{')
		# 	print(posb)
		# 	if posb == -1:
		# 		break
		# 	pose = sql.index('}')
		# 	print(pose)
		# 	if pose == -1:
		# 		raise Exception("Cấu hình lỗi: Dấu { và } ko cùng số lượng: " + detail['query'])
		# 	print(posb, pose)
		# 	varName = sql.substring(posb+1, pose)
		# 	if len(varName) == 0:
		# 		raise Exception("Cấu hình lỗi: Ko có tên biến giữa { và } : " + detail['query'])
		# 	if args[varName] == null:
		# 		raise Exception("Cấu hình lỗi: Ko tìm thấy biến trong yêu cầu:" + varName)
		# 	sql = sql.replace("{"+varName+"}", args[varName])
		params = []
		rows = self.query(sql, params)

		# Actions
		sql = """
			SELECT code, name, type, func_type, func_data
			FROM action
			WHERE page_type = 'LIST'
				AND page_id = ?
		"""
		params = [listId]
		actions = self.query(sql, params)

		# Return
		return {
			"detail": detail,
			"headers": headers,
			"rows": rows,
			"actions": actions
		}

	def getDynamicInfo(self, args):
		
		self.conn.row_factory = MtDynamicDB.cbk_dict_factory

		# Detail Info
		sql = """
			SELECT id, code, name FROM info WHERE code = ?
		"""
		params = [pageCode]
		details = self.query(sql, params)
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		detail = details[0]
		infoId = detail['id']

		# TODO

		# Actions
		sql = """
			SELECT code, name, type, func_type, func_data
			FROM action
			WHERE page_type = 'INFO'
				AND page_id = ?
		"""
		params = [infoId]
		actions = self.query(sql, params)

		# Return
		return {
			"detail": detail,
			# "headers": headers,
			# "rows": rows,
			"actions": actions
		}

