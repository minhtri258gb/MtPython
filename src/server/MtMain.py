import sys
import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from MtCloud import MtCloud
import MtConfig
from MtCore import MtCore

global mt

class Main:

	def __init__(self):

		# Load enviroment variable
		projectPath = os.path.abspath(os.getcwd())
		load_dotenv(os.path.join(projectPath, '.env'))

		# Process args
		for i, arg in enumerate(sys.argv):
			if i == 0: # Bỏ qua arg đầu tiên
				continue
			if arg == '-debug':
				MtConfig.debug = True

		# Init Cound DB
		# self.cloud = MtCloud()

		# Init API Server với static file folder
		isStaticServer = os.getenv('SERVER_STATIC')
		if isStaticServer == '1':
			staticPath = os.getenv('DIR_STATIC')
			self.app = Flask(__name__, static_url_path = '', static_folder=staticPath)
		else:
			self.app = Flask(__name__)


		# Fix lỗi CORS
		self.cors = CORS(self.app)
		self.app.config['CORS_HEADERS'] = 'Content-Type'

		# Hạn chế log trên console
		if not MtConfig.debug:
			self.log = logging.getLogger('werkzeug')
			self.log.setLevel(logging.ERROR)

		# List app
		self.listApp = {appName:None for appName in MtConfig.list_app}

		# Core app
		self.core = MtCore(self)
		self.core.register()

		# Addon app
		for appName in MtConfig.list_app:
			moduleName = 'Mt'+appName.capitalize() # Get module name
			if os.path.exists('./src/server/' + moduleName + '.py'):
				ObjModule = __import__(moduleName, globals(), locals(), [moduleName]) # Import module
				ObjClass = getattr(ObjModule, moduleName) # Get class of module
				app = ObjClass(self) # Create object from class
				self.listApp.update({appName: app}) # Update list
				app.register() # Register app

	def start(self):
		try:

			# Flask
			# def start_flask():

			mt.app.run(
				debug = MtConfig.debug,
				port = MtConfig.app_port,
				host = MtConfig.hostname,
				# ssl_context = ('./res/SSL/local.crt', './res/SSL/local.key')
			)
			# self.threadFlask = threading.Thread(target=start_flask, daemon=True)
			# self.threadFlask = Process(target=self.app.run, args=())
			# self.threadFlask.start()
			# self.threadFlask.join()
			# server.terminate()
			# server.join()
				
			# Tray Icon
			# def onClick(icon, item):
			#   global state
			#   if str(item) == "Checkable":
			#     state = not item.checked
			#   elif str(item) == 'Exit':
			#     self.tray.stop()
			# self.tray = Icon('test name',
			#   icon=Image.open("./res/logo.ico"),
			#   menu=Menu(
			#     MenuItem('Checkable', onClick, checked=lambda item: state),
			#     MenuItem("Exit", onClick)
			#   )
			# )

			# def start_tray():
			#   self.tray.run()
			# self.threadTray = threading.Thread(target=start_tray)

			# self.threadTray.start()

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('['+fname+':'+str(exc_tb.tb_lineno)+'] ',exc_type, e)


# Main
if __name__ == '__main__':
	mt = Main()
	mt.start()
