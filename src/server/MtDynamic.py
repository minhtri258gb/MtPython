import os
import sqlite3
import flask
import traceback
import MtSystem
import MtUtils

class MtDynamic:

	mt = None

	def __init__(self, _mt):
		self.mt = _mt
		self.db = MtDynamicDB()
	
	def register(self):

		@self.mt.app.route("/dynamic/page", methods=['GET'])
		def _viewPage():
			return self.viewPage()

		@self.mt.app.route("/api/dynamic/getPage", methods=['POST'])
		def _apigetPage():
			return self.apiGetPage()
		
		@self.mt.app.route("/api/dynamic/saveInfo", methods=['POST'])
		def _apiSaveInfo():
			return self.apiSaveInfo()
	
	def viewPage(self):
		staticPath = os.getenv('DIR_STATIC')
		return flask.send_from_directory(staticPath, path="dynamic/index.html")
	
	def apiGetPage(self):
		args = flask.request.get_json()
		self.db.on()
		self.db.returnType('LST_DIC')
		try:
			type = args.get('type')
			id = args.get('id')
			code = args.get('code')
			result = {}

			if 'loadMenu' in args:
				result['menus'] = self.db.getMenus()
			
			if type == 'LIST':
				res = self.getListPage(id, code, args)
			elif type == 'INFO':
				res = self.getInfoPage(id, code, args)
			elif type == 'TAB':
				res = self.getTabPage(id, code, args)
			else:
				raise Exception("Loại trang không hợp lệ!")
			result.update(res)
			result_code = 200
		except Exception as e:
			traceback.print_exc()
			errMsg = str(e)#.encode(encoding='UTF-8')
			result = { 'message': errMsg }
			result_code = 500
		self.db.off()
		return flask.jsonify(result), result_code
	
	def getListPage(self, id, code, args):
		# Page
		page = self.db.getList(id, code)
		if id is None:
			id = page['id']
		listQuery = page['query']
		del page['query'] # Remove for security
		# filters = self.db.getListFilter(listId) #TODO
		# Headers
		headers = self.db.getListCol(id)
		headers.insert(0, { "key": "stt", "value": "STT" })
		# Rows
		rows = self.db.getListRow(listQuery, args)
		# if 'process' in page:
		# 	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", page['process'])
		# 	pass
		for i, row in enumerate(rows):
			row['stt'] = i+1
		# Actions
		actionsRaw = self.db.getAction('LIST', id)
		actions = []
		actionsRow = []
		for action in actionsRaw:
			pos = action.get('pos')
			del action['pos']
			if pos == 2:
				actionsRow.append(action)
			else:
				actions.append(action)
		# Update headers
		if len(actions) > 0:
			headers.append({ "key": "overflow", "empty": True })
		# Result
		return {
			"page": page,
			# "filters": filters,
			"headers": headers,
			"rows": rows,
			"actions": actions,
			"actionsRow": actionsRow,
		}
	
	def getInfoPage(self, id, code, args):
		page = self.db.getInfo(id, code)
		if id is None:
			id = page['id']
		infoQuery = page['query']
		del page['query'] # Remove for security
		fields = self.db.getInfoField(id)
		form = {}
		if "rowId" in args:
			form = self.db.getInfoForm(infoQuery, args)
		# ACTIONS
		actions = self.db.getAction('INFO', id)
		# CONTENTS
		# Lấy danh sách content code có dùng
		lstContentCode = [field['content'] for field in fields if 'content' in field] # Lấy contentCode từ fields
		lstContentCode = list(dict.fromkeys(lstContentCode)) # Remove duplicate
		contents = self.db.getContent(lstContentCode)
		packData = args
		packData.update(form)
		contentsData, fields = self.loadContentData(contents, packData, fields)
		return {
			'page': page,
			'fields': fields,
			'form': form,
			'actions': actions,
			'contents': contentsData,
		}
	
	def getTabPage(self, id, code, args):
		page = self.db.getTab(id, code)
		if id is None:
			id = page['id']
		tabs = self.db.getTabPage(id)
		tabs[0] = self.loadFirstTab(tabs[0], args)
		return {
			'page': page,
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
			tab['isLoaded'] = True
		return tab
	
	def loadContentData(self, contents, form, fields):
		
		# Process Extra
		for i, content in enumerate(contents):
			if 'extra' not in content:
				continue
			extra = MtUtils.process_struct_pair(content['extra'], 1)
			for key in extra:
				if key in form:
					contents[i]['data'] = content['data'] + extra[key]

		# Mark dynamic
		for i, content in enumerate(contents):
			contents[i]['dynamic'] = (content['data'].find("{") >= 0)

		# Find reference field value
		for content in contents:
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
		for content in contents:
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
				datas = self.db.query(data, params)
			result[content['code']] = datas

		# Get content data dynamic
		result = {}
		for content in contents:
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
				datas = self.db.query(data, params)
			result[content['code']] = datas

		# Return contents and update fields
		return result, fields
	
	def apiSaveInfo(self):
		
		#TODO Check authenticate

		args = flask.request.get_json()
		
		self.db.on()
		self.db.returnType('LST_DIC')
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

		return flask.jsonify(result), result_code


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
		sql = "SELECT id, code, name, query, process, hasBack, l.'select' FROM list l WHERE "
		if id is None:
			sql += "code = ?"
			params = [code]
		else:
			sql += "id = ?"
			params = [id]
		pages = self.query(sql, params)
		if len(pages) == 0:
			raise Exception("Không tìm thấy trang")
		return pages[0]
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
		pages = self.query(sql, params)
		if len(pages) == 0:
			raise Exception("Không tìm thấy trang")
		return pages[0]
	def getInfoField(self, infoId):
		fields = self.query("""
				SELECT LOWER(code) code, name, type, options, f.'default'
				FROM info_field f
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
		pages = self.query(sql, params)
		if len(pages) == 0:
			raise Exception("Không tìm thấy trang")
		return pages[0]
	def getTabPage(self, tabId):
		return self.query("""
				SELECT id, code, name, page_type pageType, page_id pageId
				FROM tab_page
				WHERE tab_id = ?
			""" , [tabId])

	def getAction(self, pageType, pageId):
		return self.query("""
			SELECT code, name, pos, type, data
			FROM action
			WHERE page_type = ?
				AND page_id = ?
			ORDER BY seq
		""", [pageType, pageId])

	def getContent(self, strLstContentCode):
		if len(strLstContentCode) == 0:
			return []
		lstIdStr = ""
		params = []
		for contentCode in strLstContentCode:
			lstIdStr += ",?"
			params.append(contentCode)
		sql = """
				SELECT code, c.'type', c.'data', extra
				FROM content c
				WHERE code IN ({0})
			""".format(lstIdStr[1:])
		return self.query(sql, params)

	# def getContent2(self, lstContentCode, fields, form):


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
