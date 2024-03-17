import sqlite3
from flask import request, jsonify
import MtSystem

class MtManager:
	
	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtManagerDB()

	def register(self):

		@self.mt.app.route("/manager/search/<tableName>", methods=['POST'])
		def api_manager_search(tableName):
			return self.api_search(tableName)
		
		@self.mt.app.route("/manager/save/<tableName>", methods=['POST'])
		def api_manager_save(tableName):
			return self.api_save(tableName)

	def api_search(self, tableName):
		#TODO Check authenticate
		filter = {
			"page": request.form.get("page"),
			"rows": request.form.get("rows"),
			"sort": request.form.get("sort"),
			"order": request.form.get("order"),
			"text": request.form.get("text"),
		}
		self.db.on()
		rows, total = self.db.getList(tableName, filter)
		self.db.off()
		
		return jsonify({
			"rows": rows,
			"total": total
		}), 200

	def api_save(self, tableName):
		data = request.get_json()
		id = data.get('id')
		self.db.on()
		if id == None:
			self.db.insert(tableName, data)
		else:
			self.db.update(tableName, data)
		self.db.off()
		return "Success", 200


class MtManagerDB:
	
	dbPath = './res/database/manager.sqlite'

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

	def getList(self, table, filter):
		sql = "SELECT * FROM " + table + " WHERE 1=1"
		param = []

		# Filter
		text = filter.get('text')
		if text != None and len(text) > 0:
			sql += " and lower(name) LIKE ?"
			param.append('%'+text.lower()+'%')
		
		# Count
		sqlCount = "SELECT count(id) FROM (" + sql + ")"

		# Sort
		sort = filter.get('sort')
		order = filter.get('order')
		if sort != None:
			if order == None:
				order = 'asc'
			sql += " ORDER BY " + sort + " " + order
		else:
			sql += " ORDER BY id DESC"

		# Kpaging
		page = int(filter.get('page'))
		rows = int(filter.get('rows'))
		if page != None and rows != None:
			offset = (page - 1) * rows
			sql += " LIMIT " + str(rows) + " OFFSET " + str(offset)

		# Main Query
		self.conn.row_factory = MtSystem.sql_dict_factory
		rows = self.conn.execute(sql, param).fetchall()
		
		# Get total if kpaging
		total = len(rows)
		if page != None and rows != None:
			self.conn.row_factory = None
			total = self.conn.execute(sqlCount, param).fetchone()[0]

		return rows, total

	def insert(self, table, data):

		# Key list and value list
		keyStr = ""
		valueStr = ""
		for k,v in data.items():
			v = self.util_value2str(v)
			keyStr += k + ","
			valueStr += v + ","

		# Main SQl
		sql = "INSERT INTO " + table + " (" + keyStr[:-1] + ") "
		sql += "VALUES (" + valueStr[:-1] + ")"
		
		# Update
		self.conn.execute(sql)
		self.conn.commit()
	
	def update(self, table, data):
		
		# Main SQl
		sql = "UPDATE " + table + " SET "
		for k,v in data.items():
			if k == 'id':
				continue
			v = self.util_value2str(v)
			sql = sql + k + "=" + v + ","
		sql = sql[:-1] + " WHERE id=" + str(data.get('id'))

		# Update
		self.conn.execute(sql)
		self.conn.commit()

	def util_value2str(self, v):
		if v == None:
			return 'NULL'
		elif isinstance(v, int) or isinstance(v, float):
			return str(v)
		elif isinstance(v, str):
			return "'"+v+"'"

