import os
from flask import Response, request, jsonify, send_file, make_response
import MtConfig

class MtFile:

	mt = None

	def __init__(self, _mt):
		self.mt = _mt

	def register(self):

		@self.mt.app.route("/file/list", methods=['GET'])
		def api_file_list():
			return self.api_list()

		@self.mt.app.route("/file/read", methods=['GET'])
		def api_file_read():
			return self.api_read()

		@self.mt.app.route("/file/write", methods=['POST'])
		def api_file_write():
			return self.api_write()

	def api_list(self):
		try:

			# Lấy params
			folderPath = request.args.get('folder')

			# Đọc danh sách fie từ folder
			listFile = os.listdir(folderPath)

			# Return
			return jsonify(listFile), 200
		except Exception as e:
			return "Có lỗi xử lý: "+str(e), 500

	def api_read(self):
		try:

			# Lấy params
			filePath = request.args.get('file')
			fileName = os.path.basename(filePath)

			# Đọc file
			with open(filePath, 'rb') as file:
				fileContent = file.read()

			# Return File Content
			return Response(
				fileContent,
				mimetype = 'application/octet-stream',
				headers = { 'Content-Disposition': 'attachment;filename='+fileName }
			)
		except Exception as e:
			return "Có lỗi xử lý: "+str(e), 500

	def api_write(self):
		try:

			# Lấy params
			if 'file' not in request.files:
				return "No file part", 400
			file = request.files['file']
			if file.filename == '':
				return "No selected file", 400
			folderPath = request.args.get('folder')
			# fileName = os.path.basename(filePath)

			# Lưu file vào thư mục
			filepath = os.path.join(folderPath, file.filename)
			file.save(filepath)

			return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
		except Exception as e:
			return "Có lỗi xử lý: "+str(e), 500


