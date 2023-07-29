import os
import socket
from flask import jsonify, send_from_directory
from flask_swagger import swagger
import MtConfig

state = False

class MtCore:

  mt = None

  def __init__(self, mt):
    self.mt = mt

  def register(self):
    
    @self.mt.app.route('/')
    def api_home_page():
      return send_from_directory(MtConfig.statis_path, path="./home/index.html")

    @self.mt.app.route('/<appName>')
    @self.mt.app.route('/<appName>/')
    def api_app_page(appName):
      try:
        appName = appName.lower()
        if appName not in MtConfig.list_app:
          return "App not found"

        fullpath = MtConfig.statis_path + appName
        if (os.path.exists(fullpath) and os.path.isdir(fullpath)):
          return send_from_directory(MtConfig.statis_path, path=appName+"/index.html")
        
      except Exception as e:
        print(type(e), e)
        return "App not found"

    @self.mt.app.route("/authorize", methods=['POST'])
    def api_authorize():
      return jsonify(True), 200
    
    @self.mt.app.route("/docs")
    def api_doc_page():
      return jsonify(swagger(self.mt.app)), 200
    
    @self.mt.app.route('/common/getListApplication')
    def api_common_get_list_application():
      return jsonify(MtConfig.list_app), 200

    @self.mt.app.route('/common/getIPLocal')
    def api_common_get_ip_local():
      return jsonify(self.getHost()), 200

  def getHost(self):
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)