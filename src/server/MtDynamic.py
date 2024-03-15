import sqlite3
from flask import request, jsonify
import traceback
import MtUtils

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

		@self.mt.app.route("/api/dynamic/info/save", methods=['POST'])
		def api_dynamic_info_save():
			return self.api_info_save()

	def api_list(self):

		#TODO Check authenticate

		args = request.get_json()

		self.db.on()
		try:
			result = self.db.getDynamicList(args)
			result_code = 200
		except Exception as e:
			traceback.print_exc()
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
			traceback.print_exc()
			result = str(e)
			result_code = 500
		self.db.off()

		return jsonify(result), result_code

	def api_info_save(self):
		
		#TODO Check authenticate

		args = request.get_json()
		
		self.db.on()
		try:
			result = self.db.getDynamicInfoSave(args)
			if result:
				result_code = 200
			else:
				result_code = 201
		except Exception as e:
			traceback.print_exc()
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
	
	def exec(self, sql, params):
		self.conn.execute(sql, params)
		self.conn.commit()
	
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
		query = detail['query']
		del detail['query'] # Bỏ query vì bảo mật

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
		sql = query
		params = []
		while True:
			posb = sql.find('{')
			if posb == -1:
				break
			pose = sql.find('}')
			if pose == -1:
				raise Exception("Cấu hình lỗi: Dấu { và } ko cùng số lượng: " + detail['query'])
			
			varName = sql[posb+1:pose]
			if len(varName) == 0:
				raise Exception("Cấu hình lỗi: Ko có tên biến giữa { và } : " + detail['query'])
			if not varName in args:
				raise Exception("Cấu hình lỗi: Ko tìm thấy biến trong yêu cầu:" + varName)
			sql = sql.replace("{"+varName+"}", "?")
			params.append(args[varName])
		rows = self.query(sql, params)

		# Actions
		sql = """
			SELECT code, name, type, func_type, func_data
			FROM action
			WHERE page_type = 'LIST'
				AND page_id = ?
			ORDER BY seq
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

		pageCode = args["page"]
		if "id" in args:
			id = args["id"]
		else:
			id = None

		lstContentCode = [] # Danh sách content

		# Detail
		sql = """
			SELECT id, code, name, i.'table', query
			FROM info i
			WHERE code = ?
		"""
		params = [pageCode]
		details = self.query(sql, params)
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		detail = details[0]
		infoId = detail['id']
		query = detail['query']
		del detail['query'] # Bỏ query vì bảo mật

		# Field
		sql = """
			SELECT LOWER(code) code, name, type, options
			FROM info_field
			WHERE info_id = ?
			ORDER BY seq
		"""
		params = [infoId]
		fields = self.query(sql, params)
		for i, field in enumerate(fields):
			# Process Options in field
			options = field['options']
			del field['options']
			if options is not None:
				options = MtUtils.process_struct_pair(options, 1)
				options.update(field) # Đè field vào options tránh đè prop quan trọng
				if 'content' in options: # Lưu danh sách content để load
					lstContentCode.append(options['content'])
				fields[i] = options # Cập nhật lại fields

		# Form
		if id is not None:
			sql, params = MtUtils.fillVarSql(query, args, None, None)
			# sql = query
			# params = []

			# while True:
			# 	posb = sql.find('{')
			# 	if posb == -1:
			# 		break
			# 	pose = sql.find('}')
			# 	if pose == -1:
			# 		raise Exception("Cấu hình lỗi: Dấu { và } ko cùng số lượng: " + detail['query'])
				
			# 	varName = sql[posb+1:pose]
			# 	if len(varName) == 0:
			# 		raise Exception("Cấu hình lỗi: Ko có tên biến giữa { và } : " + detail['query'])
			# 	if not varName in args:
			# 		raise Exception("Cấu hình lỗi: Ko tìm thấy biến trong yêu cầu: " + varName + " trong query: " + query)
			# 	sql = sql.replace("{"+varName+"}", "?")
			# 	params.append(args[varName])
			forms = self.query(sql, params)
			if len(forms) > 0:
				form = forms[0]
		else:
			form = {}

		# Actions
		sql = """
			SELECT code, name, type, func_type, func_data
			FROM action
			WHERE page_type = 'INFO'
				AND page_id = ?
		"""
		params = [infoId]
		actions = self.query(sql, params)

		# Content
		lstContentCode = list(dict.fromkeys(lstContentCode)) # Remove duplicate
		contents, fields = self.getContent(lstContentCode, fields, form)

		# Return
		return {
			"detail": detail,
			"fields": fields,
			"form": form,
			"actions": actions,
			"contents": contents
		}

	def getDynamicInfoSave(self, args):
		
		self.conn.row_factory = MtDynamicDB.cbk_dict_factory

		tableName = args["table"]
		del args["table"]

		# Kiểm tra tồn tại bảng và lấy các cột trong bảng
		sql = """
			SELECT name, t.'notnull'
			FROM pragma_table_info(?) t
			WHERE pk = 0
		"""
		params = [tableName]
		columns = self.query(sql, params)
		if len(columns) == 0:
			raise Exception("Cấu hình lỗi, bảng không tồn tại: " + tableName)

		# Kiểm tra các cột NOT NULL và giá trị truyền vào
		lstColStr = "id"
		for column in columns:
			colName = column['name']
			lstColStr += "," + colName
			if column['notnull'] == 1 and args[colName] is None:
				raise Exception("Cột "+colName+" trong bảng "+tableName+" không được truyền NULL")

		# Kiểm tra các cột của form có trong bảng không
		for key in args.keys():
			if lstColStr.find(key) == -1:
				raise Exception("Không tồn tại cột "+key+" trong bảng "+tableName)

		# Kiểm tra id
		if not 'id' in args: # Tạo mới

			lstKeyStr = ""
			lstValueStr = ""
			params = []
			for key, value in args.items():
				lstKeyStr += "," + key
				lstValueStr += ",?"
				params.append(value)
			lstKeyStr = lstKeyStr[1:]
			lstValueStr = lstValueStr[1:]
				
			sql = """
				INSERT INTO {0} ({1})
				VALUES ({2});
			""".format(tableName, lstKeyStr, lstValueStr)

			self.exec(sql, params)
			
		else: # Cập nhật

			id = args['id']

			# Lấy dữ liệu có sẵn
			sql = """
				SELECT * FROM {0}
				WHERE id = ?
			""".format(tableName)
			oldForms = self.query(sql, [id])
			oldForm = oldForms[0]

			# Tổng hợp SQL cập nhật
			setSql = ""
			params = []
			for key, value in args.items():
				if value != oldForm[key]:
					setSql += ",{0} = ?".format(key)
					params.append(value)
			if len(setSql) > 0:
				sql = """
					UPDATE {0}
					SET {1}
					WHERE id = ?
				""".format(tableName, setSql[1:])
				params.append(id)
				self.exec(sql, params)
				return True
			else:
				return False

	def getContent(self, lstContentCode, fields, form):

		# Get content info
		if len(lstContentCode) == 0:
			return {}, fields
		lstIdStr = ""
		params = []
		for contentCode in lstContentCode:
			lstIdStr += ",?"
			params.append(contentCode)
		sql = """
			SELECT code, c.'type', c.'data', dynamic
			FROM content c
			WHERE code IN ({0})
		""".format(lstIdStr[1:])
		lstContent = self.query(sql, params)

		# Find reference field value
		for content in lstContent:
			if content['dynamic'] == 0:
				continue
			# Find field use content
			lstFieldAffect = [i for i, f in enumerate(fields) if 'content' in f and f['content'] == content['code']]
			letVar = MtUtils.removeDuplicate(MtUtils.findVar(content['data']))
			for i, field in enumerate(fields):
				if field['code'] in letVar:
					if not 'affect' in fields[i]:
						fields[i]['affect'] = []
					lstAffectId = fields[i]['affect']
					lstAffectId.extend(lstFieldAffect)
					fields[i]['affect'] = MtUtils.removeDuplicate(lstAffectId)

		# Get content data static
		result = {}
		for content in lstContent:
			type = content['type']
			data = content['data']
			params = []
			if content['dynamic'] == 1: # Nhập biến vào chuỗi
				if type == 'SQL':
					data, params = MtUtils.fillVarSql(data, form, fields, result)
				else:
					data = MtUtils.fillVar(data, form, fields, result)
			if type == 'LIST':
				datas = MtUtils.process_struct_list(content['data'], 2)
			elif type == 'PAIR':
				datas = MtUtils.process_struct_pair(content['data'], 2)
			elif type == 'SQL':
				datas = self.query(data, params)
			result[content['code']] = datas

		# Get content data dynamic
		result = {}
		for content in lstContent:
			type = content['type']
			data = content['data']
			params = []
			if content['dynamic'] == 1: # Nhập biến vào chuỗi
				if type == 'SQL':
					data, params = MtUtils.fillVarSql(data, form, fields, result)
				else:
					data = MtUtils.fillVar(data, form, fields, result)
			if type == 'LIST':
				datas = MtUtils.process_struct_list(content['data'], 2)
			elif type == 'PAIR':
				datas = MtUtils.process_struct_pair(content['data'], 2)
			elif type == 'SQL':
				datas = self.query(data, params)
			result[content['code']] = datas

		# Return contents and update fields
		return result, fields
