import sqlite3
from flask import request, jsonify
import traceback
import MtSystem
import MtUtils

class MtDynamic:
	
	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtDynamicDB()

	def register(self):

		@self.mt.app.route("/api/dynamic/getPage", methods=['POST'])
		def _apigetPage():
			return self.apiGetPage()
		
		@self.mt.app.route("/api/dynamic/saveInfo", methods=['POST'])
		def _apiSaveInfo():
			return self.apiSaveInfo()

	def apiGetPage(self):
		args = request.get_json()
		self.db.on()
		self.db.returnType('LST_DIC')
		try:
			type = args['type']
			code = args['code']
			result = {}
			result['menus'] = self.db.getMenus()
			if type == 'LIST':
				res = self.getListPage(None, code, args)
				result.update(res)
			elif type == 'INFO':
				res = self.getInfoPage(None, code, args)
				result.update(res)
			elif type == 'TAB':
				res = self.getTabPage(None, code, args)
				result.update(res)
			result_code = 200
		except Exception as e:
			traceback.print_exc()
			result = str(e)
			result_code = 500
		self.db.off()
		return jsonify(result), result_code

	def apiSaveInfo(self):
		
		#TODO Check authenticate

		args = request.get_json()
		
		self.db.on()
		try:
			isUpdate = ('id' in args)
			result = {}
			idResult = self.db.saveInfo(args)
			if isUpdate:
				if idResult == -1:
					result_code = 201
					result['message'] = "Dữ liệu không có sự thay đổi"
				else:
					result_code = 200
					result['message'] = "Cập nhật thành công"
			else:
				result_code = 200
				result['message'] = "Lưu thành công"
				result['id'] = idResult
		except Exception as e:
			traceback.print_exc()
			result['message'] = str(e)
			result_code = 500
		self.db.off()

		return jsonify(result), result_code

	def getListPage(self, id, code, args):
		type = args['type']
		detail = self.db.getList(id, code)
		listId = detail['id']
		listQuery = detail['query']
		del detail['query'] # Remove for security
		# filters = self.db.getListFilter(listId) #TODO
		headers = self.db.getListCol(listId)
		rows = self.db.getListRow(listQuery, args)
		actions = self.db.getAction(type, listId)
		return {
			"detail": detail,
			# "filters": filters,
			"headers": headers,
			"rows": rows,
			"actions": actions,
		}

	def getInfoPage(self, id, code, args):
		type = args['type']
		detail = self.db.getInfo(id, code)
		infoId = detail['id']
		infoQuery = detail['query']
		del detail['query'] # Remove for security
		fields = self.db.getInfoField(infoId)
		form = {}
		if "id" in args:
			form = self.db.getInfoForm(infoQuery, args)
		actions = self.db.getAction(type, infoId)
		lstContentCode = [field['content'] for field in fields if 'content' in field] # Danh sách content
		lstContentCode = list(dict.fromkeys(lstContentCode)) # Remove duplicate
		contents, fields = self.db.getContent(lstContentCode, fields, form)
		return {
			'detail': detail,
			'fields': fields,
			'form': form,
			'actions': actions,
			'contents': contents,
		}

	def getTabPage(self, id, code, args):
		type = args['type']
		detail = self.db.getTab(id, code)
		print(detail)
		tabs = self.db.getTabPage(detail['id'])
		tabs[0] = self.loadFirstTab(tabs[0], args)
		return {
			'detail': detail,
			'tabs': tabs,
		}

	def loadFirstTab(self, tab, args):
		pageType = tab['pageType']
		pageId = tab['pageId']
		res = None
		if pageType == 'LIST':
			res = self.getListPage(pageId, None, args)
		elif pageType == 'INFO':
			res = self.getInfoPage(pageId, None, args)
		elif pageType == 'TAB':
			res = self.getTabPage(pageId, None, args)
		if res is not None:
			tab.update(res)
		return tab

class MtDynamicDB:

	h_db_path = './res/database/dynamic.sqlite'

	def __init__(self):
		self.conn = None
	
	def on(self):
		if self.conn != None:
			self.off()
		if sqlite3.threadsafety == 3:
			check_same_thread = False
		else:
			check_same_thread = True
		self.conn = sqlite3.connect(self.h_db_path, check_same_thread=check_same_thread)
	def off(self):
		if self.conn != None:
			self.conn.close()
			self.conn = None
	def query(self, sql, params):
		try:
			return self.conn.execute(sql, params).fetchall()
		except Exception as e:
			print("[ERROR] sql: ", sql)
			print("[ERROR] params: ", params)
			raise e
	def exec(self, sql, params):
		self.conn.execute(sql, params)
		self.conn.commit()
	def returnType(self, type):
		if type == 'LST_DIC':
			self.conn.row_factory = MtSystem.sql_dict_factory

	def getMenus(self):
		menus = self.query("""
			SELECT id, code, name, parent, link
			FROM menu
		""", [])
		return MtDynamicUtils.buildMenuTree(menus)

	def getList(self, id, code):
		sql = "SELECT id, code, name, query FROM list WHERE "
		if id is None:
			sql += "code = ?"
			params = [code]
		else:
			sql += "id = ?"
			params = [id]
		details = self.query(sql, params)
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		return details[0]
	def getListFilter(self, listId):
		return {} #TODO
	def getListCol(self, listId):
		return self.query("""
				SELECT LOWER(code) key, name value
				FROM list_col
				WHERE list_id = ?
				ORDER BY seq
			""", [listId])
	def getListRow(self, query, data):
		sql, params = MtUtils.fillVarSql(query, data)
		return self.query(sql, params)

	def getInfo(self, id, code):
		sql = "SELECT id, code, name, i.'table', query FROM info i WHERE "
		if id is None:
			sql += "code = ?"
			params = [code]
		else:
			sql += "id = ?"
			params = [id]
		details = self.query(sql, [code])
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		return details[0]
	def getInfoField(self, infoId):
		fields = self.query("""
			SELECT LOWER(code) code, name, type, options
			FROM info_field
			WHERE info_id = ?
			ORDER BY seq
		""", [infoId])
		return MtDynamicUtils.processFieldOptions(fields)
	def getInfoForm(self, query, data):
		sql, params = MtUtils.fillVarSql(query, data)
		forms = self.query(sql, params)
		if len(forms) > 0:
			return forms[0]
		return {}
	def saveInfo(self, args):
		
		self.conn.row_factory = MtSystem.sql_dict_factory

		tableName = args["_table_"]
		del args["_table_"]

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
			if column['notnull'] == 1 and colName not in args:
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
				lstKeyStr += ",'" + key + "'"
				lstValueStr += ",?"
				params.append(value)
			lstKeyStr = lstKeyStr[1:]
			lstValueStr = lstValueStr[1:]
				
			sql = """
				INSERT INTO '{0}' ({1})
				VALUES ({2});
			""".format(tableName, lstKeyStr, lstValueStr)
			self.exec(sql, params)

			# Get insert id
			sql = """
				SELECT seq
				FROM sqlite_sequence
				WHERE name = ?
			"""
			resNewId = self.query(sql, [tableName])

			return resNewId[0]['seq']
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
				return id
			else:
				return -1

	def getTab(self, id, code):
		sql = "SELECT id, code, name FROM tab WHERE "
		if id is None:
			sql += "code = ?"
			params = [code]
		else:
			sql += "id = ?"
			params = [id]
		details = self.query(sql, params)
		if len(details) == 0:
			raise Exception("Không tìm thấy trang")
		return details[0]
	def getTabPage(self, tabId):
		self.conn.row_factory = MtSystem.sql_dict_factory
		return self.query(
			""" SELECT code, name, page_type pageType, page_id pageId
				FROM tab_page
				WHERE tab_id = ?
			""" , [tabId])

	def getAction(self, pageType, pageId):
		return self.query("""
			SELECT code, name, type, func_type, func_data
			FROM action
			WHERE page_type = ?
				AND page_id = ?
			ORDER BY seq
		""", [pageType, pageId])

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
			SELECT code, c.'type', c.'data', extra
			FROM content c
			WHERE code IN ({0})
		""".format(lstIdStr[1:])
		lstContent = self.query(sql, params)

		# Process Extra
		for i, content in enumerate(lstContent):
			if 'extra' not in content:
				continue
			extra = MtUtils.process_struct_pair(content['extra'], 1)
			for key in extra:
				if key in form:
					lstContent[i]['data'] = content['data'] + extra[key]

		# Mark dynamic
		for i, content in enumerate(lstContent):
			lstContent[i]['dynamic'] = (content['data'].find("{") >= 0)

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
					data, params = MtUtils.fillVarSql(data, form)
					# data, params = MtUtils.fillVarSql(data, form, fields, result)
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
					data, params = MtUtils.fillVarSql(data, form)
					# data, params = MtUtils.fillVarSql(data, form, fields, result)
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

class MtDynamicUtils:
	def buildMenuTree(menus):
		# Insert child into parent
		lstRootId = []
		for i, menu in enumerate(menus):
			parentId = menu['parent']
			if parentId is None:
				lstRootId.append(i)
			else:
				# Find id
				parentStt = -1
				for j, menu2 in enumerate(menus):
					if menu2['id'] == parentId:
						parentStt = j
						break
				if parentStt >= 0:
					if 'child' not in menus[parentStt]:
						menus[parentStt]['child'] = []
					menus[parentStt]['child'].append(menu)
		# Select root menu
		return [menu for i, menu in enumerate(menus) if i in lstRootId]
	def processFieldOptions(fields):
		for i, field in enumerate(fields):
			options = field['options']
			del field['options']
			if options is not None:
				extraProp = MtUtils.process_struct_pair(options, 1)
				extraProp.update(field) # Đè field vào options tránh đè prop quan trọng
				fields[i] = extraProp # Cập nhật lại fields
		return fields
