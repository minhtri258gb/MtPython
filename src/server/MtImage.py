# from PIL import Image
# from io import BytesIO

class MtImage:
	
	mt = None
	dbPath = './res/database/manager.sqlite'
	
	def __init__(self, _mt):
		self.mt = _mt
		# self.db = MtManagerDB()
	
	def register(self):
		
		# @self.mt.app.route("/manager/search/<tableName>", methods=['POST'])
		# def api_manager_search(tableName):
		# 	return self.api_search(tableName)
		
		# @self.mt.app.route("/manager/save/<tableName>", methods=['POST'])
		# def api_manager_save(tableName):
		# 	return self.api_save(tableName)
		
		pass
	
	# def covPNG2JPG(self): # convert png to jpg
	# 	ima = Image.open("img.png")
	# 	with BytesIO() as f:
	# 		ima.save(f, format='JPEG')
	# 		f.seek(0)
	# 		ima_jpg = Image.open(f)

