import os
from io import StringIO
import sqlite3
from flask import request, jsonify, send_file, make_response
# from pydub import AudioSegment
import MtConfig
import MtSystem


class MtMusic:

	mt = None
	# cloudId = -1
	dbPath = './res/database/music.sqlite'

	def __init__(self, _mt):
		self.mt = _mt
		# if MtConfig.cloud_db_music:
		# 	self.cloudId = _mt.cloud.getWorkSheetId("music")
		# else:
		# 	self.db = MtMusicDB()

	def register(self):

		@self.mt.app.route("/music/getListMusic", methods=['POST'])
		def api_music_getListMusic():
			return self.api_getListMusic()

		@self.mt.app.route("/music/getMusic", methods=['GET'])
		def api_music_getMusic():
			return self.api_getMusic()

		@self.mt.app.route("/music/refresh", methods=['POST'])
		def api_music_refresh():
			return self.api_refresh()

		@self.mt.app.route("/music/add", methods=['POST'])
		def api_music_add():
			return self.api_add()

		@self.mt.app.route("/music/addAll", methods=['POST'])
		def api_music_add_all():
			return self.api_add_all()

		@self.mt.app.route("/music/edit", methods=['POST'])
		def api_music_edit():
			return self.api_edit()

		@self.mt.app.route("/music/remove", methods=['DELETE'])
		def api_music_remove():
			return self.api_remove()

		# @self.mt.app.route("/music/cut", methods=['POST'])
		# def api_music_cut():
		# 	return self.api_cut()

		@self.mt.app.route("/music/listSync", methods=['POST'])
		def api_music_list_sync():
			return self.api_list_sync()

	def api_getListMusic(self):

		# Code lấy danh sách từ cloud
		# if MtConfig.cloud_db_music: # Get list from cloud sheet
			# listMusic = self.mt.cloud.getAll(self.cloudId)
		# else: # Get list from local database

		# Load from Database
		conn = sqlite3.connect(self.dbPath)
		conn.row_factory = MtSystem.sql_dict_factory

		sql = '''
			SELECT id, name, duration, rate, tags, decibel, trackbegin, trackend
			FROM music
			WHERE miss = 0
		'''

		# Filter include
		include = request.form.getlist("include[]")
		if include != None:
			for text in include:
				sql += " AND (','||tags||',') LIKE '%,"+text+",%'"

		# Filter exclude
		exclude = request.form.getlist("exclude[]")
		if exclude != None:
			for text in exclude:
				sql += " AND (','||tags||',') NOT LIKE '%,"+text+",%'"

		sql += " ORDER BY name"

		cursor = conn.execute(sql)
		listMusic = cursor.fetchall()
		conn.close()

		# Return
		return jsonify(listMusic), 200

	def api_getMusic(self):
		name = request.args.get('name')
		try:
			filepath = os.path.join(MtConfig.dir_music, name + '.mp3')
			return send_file(filepath, 'audio/mp3')
		except FileNotFoundError as e:
			# Không tìm thấy file thì cập nhật là miss
			conn = sqlite3.connect(self.dbPath)
			conn.execute("UPDATE music SET miss = 1 WHERE name = ?", [name])
			conn.commit()
			conn.close()
			return jsonify("Không tìm thấy file nhạc: " + e.name), 303
		except Exception as e:
			print(type(e), e)

	def api_refresh(self):
		try:

			# Authorize
			token = request.form.get('token')
			if not MtSystem.auth_check(token):
				return "Access denied", 403

			# Lấy tất cả từ thư mục
			listItems = os.listdir(MtConfig.dir_music)

			# Lấy các file mp3
			listFileMusic = []
			for item in listItems:
				if (item[-4:] == '.mp3'):
					listFileMusic.append(item[0:-4])

			# Read database from cloud
			# lstDBFileName = []
			# if MtConfig.cloud_db_music: # Get list from cloud sheet
			# 	lstDBFileName = self.mt.cloud.getCols(self.cloudId, 2) # name
			# else:                       # Get list from local database

			# Read database
			conn = sqlite3.connect(self.dbPath)
			cursor = conn.execute("SELECT name FROM music WHERE miss = 0")
			listFileName = []
			for row in cursor:
				listFileName.append(row[0])
			conn.close()

			# Danh sach file nhạc mới
			lstNewMusic = [{"name":name} for name in listFileMusic if name not in listFileName]
			if len(lstNewMusic) == 0:
				lstNewMusic.append({"name":'empty'})

			return jsonify(lstNewMusic), 200

		except Exception as e:
			return "Lỗi: "+str(e), 500

	def api_add(self):
		# Authorize
		if not MtSystem.auth_check(request.form.get('token')):
			return "Access denied", 403

		# Add to database
		name = request.form.get('name')

		# Cloud
		# if MtConfig.cloud_db_music: # Get list from cloud sheet
		# 	lstValue, lstId = self.mt.cloud.findInCol(self.cloudId, 2, name) # name
		# 	if len(lstValue) > 0:
		# 		self.mt.cloud.setCell(self.cloudId, lstId[0]+1, 14, 'OKE')
		# 	else:
		# 		print("=========================== Không tìm thấy")
		# 	pass
		# else:

		# From Database
		conn = sqlite3.connect(self.dbPath)
		conn.row_factory = MtSystem.sql_dict_factory
		cursor = conn.execute("SELECT * FROM music WHERE name = ?", [name])
		musicDB = cursor.fetchone()
		if musicDB != None: # Nếu có thì cập nhật trở lại
			conn.execute("UPDATE music SET miss = 0 WHERE name = ?", [name])
			conn.commit()
		else:
			conn.execute("INSERT INTO music(name) VAlUES(?)", [name])
			conn.commit()
		conn.close()

		return jsonify("Success"), 200

	def api_add_all(self):

		if not MtSystem.auth_check(request.form.get('token')):
			return "Access denied", 403

		# Add to database
		lstFileName = request.form.getlist('lstFileName[]')

		# Cloud
		# if MtConfig.cloud_db_music: # Get list from cloud sheet
		# 	lstValue, lstId = self.mt.cloud.findInCol(self.cloudId, 2, name) # name
		# 	if len(lstValue) > 0:
		# 		self.mt.cloud.setCell(self.cloudId, lstId[0]+1, 14, 'OKE')
		# 	else:
		# 		print("=========================== Không tìm thấy")
		# 	pass
		# else:

		# From Database
		conn = sqlite3.connect(self.dbPath)
		conn.row_factory = MtSystem.sql_dict_factory
		for name in lstFileName:
			cursor = conn.execute("SELECT id FROM music WHERE name = ?", [name])
			musicDB = cursor.fetchone()
			if musicDB != None: # Nếu có thì cập nhật trở lại
				conn.execute("UPDATE music SET miss = 0 WHERE name = ?", [name])
			else:
				conn.execute("INSERT INTO music(name) VAlUES(?)", [name])
		conn.commit()
		conn.close()

		return jsonify("Success"), 200

	def api_edit(self):

		# Authorize
		if not MtSystem.auth_check(request.form.get('token')):
			return "Access denied", 403

		id = request.form.get('id')
		conn = sqlite3.connect(self.dbPath)

		conn.row_factory = MtSystem.sql_dict_factory
		cursor = conn.execute("SELECT * FROM music WHERE id = ?", [id])
		music = cursor.fetchone()

		# If name change, rename file on disk
		filepathOld = MtConfig.dir_music + music.get('name') + '.mp3'
		filepathNew = MtConfig.dir_music + request.form.get('name') + '.mp3'
		if filepathOld != filepathNew:
			os.rename(filepathOld, filepathNew)

		# Process data
		tags = request.form.get('tags')
		if (isinstance(tags, str)):
			tags = tags.upper()

		trackbegin = request.form.get('trackbegin')
		trackend = request.form.get('trackend')
		if len(trackbegin) == 0:
			trackbegin = None
		if len(trackend) == 0:
			trackend = None

		# Update data
		music.update({'name': request.form.get('name')})
		music.update({'duration': request.form.get('duration')})
		music.update({'tags': tags})
		music.update({'decibel': request.form.get('decibel')})
		music.update({'rate': request.form.get('rate')})
		music.update({'trackbegin': trackbegin})
		music.update({'trackend': trackend})

		conn.execute('''
			UPDATE music
			SET name = ?,
				duration = ?,
				tags = ?,
				decibel = ?,
				rate = ?,
				trackbegin = ?,
				trackend = ?
			WHERE id = ?
		''', [
			music.get('name'),
			music.get('duration'),
			music.get('tags'),
			music.get('decibel'),
			music.get('rate'),
			music.get('trackbegin'),
			music.get('trackend'),
			id
		])
		conn.commit()
		conn.close()

		return jsonify("Success"), 200

	def api_remove(self):
		# Authorize
		if not MtSystem.auth_check(request.form.get('token')):
			return "Access denied", 403

		id = request.form.get('id')
		conn = sqlite3.connect(self.dbPath)
		conn.execute("UPDATE music SET miss = 1 WHERE id = ?", [id])
		conn.commit()
		conn.close()
		return jsonify("Success"), 200

	# def api_cut(self):
	# 	# Authorize
	# 	if not MtSystem.auth_check(request.form.get('token')):
	# 		return "Access denied", 403

	# 	# Get param
	# 	id = request.form.get('id')
	# 	trackbegin = request.form.get('trackbegin')
	# 	trackend = request.form.get('trackend')
	# 	if trackbegin == None or trackend == None:
	# 		return jsonify("Thiếu thông tin track"), 300
	# 	trackbegin = float(trackbegin)
	# 	trackend = float(trackend)

	# 	# Get from DB
	# 	conn = sqlite3.connect(self.dbPath)
	# 	conn.row_factory = MtSystem.sql_dict_factory
	# 	cursor = conn.execute("SELECT * FROM music WHERE id = ?", [id])
	# 	music = cursor.fetchone()
	# 	conn.close()

	# 	try:
	# 		filepath = MtConfig.dir_music + music.get('name') + '.mp3'
	# 		musicFile = AudioSegment.from_mp3(filepath)

	# 		trackFile = musicFile[trackbegin * 1000 : trackend * 1000]
	# 		trackpath = MtConfig.tmp_path + 'track.mp3'
	# 		if os.path.exists(trackpath):
	# 			os.remove(trackpath)
	# 		trackFile.export(trackpath, format='mp3')

	# 		contentBin = None
	# 		with open(trackpath, 'rb') as file:
	# 			contentBin = file.read()

	# 		os.remove(trackpath)

	# 		res = make_response(contentBin)
	# 		res.headers.set('Content-Type', 'audio/mp3')
	# 		res.headers.set('Content-Disposition', 'attachment', name='%s (track).mp3' % music.get('name'))
	# 		res.status = 200
	# 		return res

	# 	except Exception as e:
	# 		print(type(e), e)
	# 		return jsonify("Error"), 300

	def api_list_sync(self):
		try:
			# Lấy tất cả từ thư mục
			listItems = os.listdir(MtConfig.dir_music)

			# Lấy các file mp3
			listFileMusic = []
			for item in listItems:
				if (item[-4:] == '.mp3'):
					listFileMusic.append(item[0:-4])

			# Viết lên file stream
			content = StringIO()
			for name in listFileMusic:
				content.write(name + '\n')

			# Response
			res = make_response(content.getvalue())
			res.headers.set('Content-Type', 'text/plain')
			res.headers.set('Content-Disposition', 'attachment', name='listMusic.txt')
			res.status = 200
			return res

		except Exception as e:
			print(type(e), e)
			return jsonify("Error"), 300

