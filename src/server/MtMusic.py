import os
import sqlite3
from flask import request, jsonify, send_file, make_response
from pydub import AudioSegment
import MtConfig


class MtMusic:

  mt = None
  cloudId = -1

  def __init__(self, _mt):
    self.mt = _mt
    if MtConfig.cloud_db_music:
      self.cloudId = _mt.cloud.getWorkSheetId("music")
    else:
      self.db = MtMusicDB()

  def register(self):

    @self.mt.app.route("/music/getListMusic", methods=['POST'])
    def api_music_getListMusic():
      return self.api_getListMusic()

    @self.mt.app.route("/music/getMusic")
    def api_music_getMusic():
      return self.api_getMusic()

    @self.mt.app.route("/music/refresh", methods=['POST'])
    def api_music_refresh():
      return self.api_refresh()
    
    @self.mt.app.route("/music/add", methods=['POST'])
    def api_music_add():
      return self.api_add()

    @self.mt.app.route("/music/edit", methods=['POST'])
    def api_music_edit():
      return self.api_edit()
    
    @self.mt.app.route("/music/remove", methods=['DELETE'])
    def api_music_remove():
      return self.api_remove()
    
    @self.mt.app.route("/music/cut", methods=['POST'])
    def api_music_cut():
      return self.api_cut()

  def api_getListMusic(self):

    listMusic = []
    if MtConfig.cloud_db_music: # Get list from cloud sheet
      listMusic = self.mt.cloud.getAll(self.cloudId)
    else:                       # Get list from local database
      self.db.on()
      listMusic = self.db.getListMusic()
      self.db.off()

    # Filter
    listMusicFilter = []
    include = request.form.getlist("include[]")
    exclude = request.form.getlist("exclude[]")
    for music in listMusic:
      # no get miss
      if music.get('miss') == 1:
        continue
      tags = music.get('tags')
      if tags == None:
        tags = ''
      check = True
      # check include
      if include != None:
        for text in include:
          if text not in tags:
            check = False
            break
      # check exclude
      if check and exclude != None:
        for text in exclude:
          if text in tags:
            check = False
            break
      if check:
        listMusicFilter.append(music)
    
    # Sort
    def sortFunc(music):
      artists = music.get('artists')
      if len(artists) == 0:
        artists = ' '
      return (artists + str(music.get('name'))).upper()
    listMusicFilter.sort(key=sortFunc)

    # Return
    return jsonify(listMusicFilter), 200

  def api_getMusic(self):
    filename = request.args.get('filename')
    try:
      filepath = os.path.join(MtConfig.dir_music, filename + '.mp3')
      return send_file(filepath, 'audio/mp3')
    except FileNotFoundError as e:
      # Không tìm thấy file thì cập nhật là miss
      # self.db.on()
      # self.db.updateMissByFileName(filename, 1)
      # self.db.off()
      return jsonify("Không tìm thấy file nhạc: " + e.filename), 303
    except Exception as e:
      print(type(e), e)

  def api_refresh(self):
      # #TODO Authorize
    	# if !mt.util.authorize(req):
    	# 	return jsonify("Access denied"), 403

    	# Lấy tất cả từ thư mục
      listItems = os.listdir(MtConfig.dir_music)

      # Lấy các file mp3
      listFileMusic = []
      for item in listItems:
        if (item[-4:] == '.mp3'):
          listFileMusic.append(item[0:-4])

    	# Read database
      lstDBFileName = []
      if MtConfig.cloud_db_music: # Get list from cloud sheet
        lstDBFileName = self.mt.cloud.getCols(self.cloudId, 2) # filename
      else:                       # Get list from local database
        self.db.on()
        lstDBFileName = self.db.getAllFilename()
        self.db.off()

      # Danh sach file nhạc mới
      lstNewMusic = [{"filename":name} for name in listFileMusic if name not in lstDBFileName]
      if len(lstNewMusic) == 0:
        lstNewMusic.append({"filename":'empty'})
      
      return jsonify(lstNewMusic), 200

  def api_add(self):
    # #TODO Authorize
    # if !mt.util.authorize(req):
    # 	return jsonify("Access denied"), 403

    # Add to database
    filename = request.form.get('filename')

    if MtConfig.cloud_db_music: # Get list from cloud sheet
      lstValue, lstId = self.mt.cloud.findInCol(self.cloudId, 2, filename) # filename
      if len(lstValue) > 0:
        self.mt.cloud.setCell(self.cloudId, lstId[0]+1, 14, 'OKE')
      else:
        print("=========================== Không tìm thấy")
      pass
    else:
      self.db.on()
      musicDB = self.db.getMusicByFilename(filename)
      if musicDB != None:
        self.db.updateMissByFileName(filename, 0) # Nếu có thì cập nhật trở lại
      else:
        self.db.insertMusic(filename) # Thêm mới
      self.db.off()

    return jsonify("Success"), 200

  def api_edit(self):
    # #TODO Authorize
    # if !mt.util.authorize(req):
    # 	return jsonify("Access denied"), 403

    id = request.form.get('id')
    self.db.on()
    music = self.db.getMusicById(id)

    # If filename change, rename file on disk
    filepathOld = MtConfig.dir_music + music.get('filename') + '.mp3'
    filepathNew = MtConfig.dir_music + request.form.get('filename') + '.mp3'
    if filepathOld != filepathNew:
      os.rename(filepathOld, filepathNew)

    # Update data
    music.update({'filename': request.form.get('filename')})
    music.update({'name': request.form.get('name')})
    music.update({'artists': request.form.get('artists')})
    music.update({'duration': request.form.get('duration')})
    music.update({'tags': request.form.get('tags')})
    music.update({'decibel': request.form.get('decibel')})
    music.update({'rate': request.form.get('rate')})
    music.update({'trackbegin': request.form.get('trackbegin')})
    music.update({'trackend': request.form.get('trackend')})
    self.db.updateMusic(id, music)

    self.db.off()
    return jsonify("Success"), 200

  def api_remove(self):
    # #TODO Authorize
    # if !mt.util.authorize(req):
    # 	return jsonify("Access denied"), 403
      
    id = request.form.get('id')
    self.db.on()
    self.db.updateMissById(id, 1)
    self.db.off()
    return jsonify("Success"), 200
  
  def api_cut(self):
    # #TODO Authorize
    # if !mt.util.authorize(req):
    # 	return jsonify("Access denied"), 403

    # Get param
    id = request.form.get('id')
    trackbegin = request.form.get('trackbegin')
    trackend = request.form.get('trackend')
    if trackbegin == None or trackend == None:
      return jsonify("Thiếu thông tin track"), 300
    trackbegin = float(trackbegin)
    trackend = float(trackend)

    # Get from DB
    self.db.on()
    music = self.db.getMusicById(id)
    self.db.off()

    try:
      filepath = MtConfig.dir_music + music.get('filename') + '.mp3'
      musicFile = AudioSegment.from_mp3(filepath)

      trackFile = musicFile[trackbegin * 1000 : trackend * 1000]
      trackpath = MtConfig.tmp_path + 'track.mp3'
      if os.path.exists(trackpath):
        os.remove(trackpath)
      trackFile.export(trackpath, format='mp3')

      contentBin = None
      with open(trackpath, 'rb') as file:
        contentBin = file.read()

      os.remove(trackpath)

      res = make_response(contentBin)
      res.headers.set('Content-Type', 'audio/mp3')
      res.headers.set('Content-Disposition', 'attachment', filename='%s (track).mp3' % music.get('filename'))
      res.status = 200
      return res
    
    except Exception as e:
      print(type(e), e)
      return jsonify("Error"), 300


class MtMusicDB:

  dbPath = './res/database/music.sqlite'

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

  def cbk_dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  def getListMusic(self):
    self.conn.row_factory = MtMusicDB.cbk_dict_factory
    cursor = self.conn.execute("SELECT * FROM music WHERE miss = 0 ORDER BY artists, name")
    return cursor.fetchall()

  def getAllFilename(self):
    cursor = self.conn.execute("SELECT filename FROM music WHERE miss = 0")
    listFileName = []
    for row in cursor:
      listFileName.append(row[0])
    return listFileName
  
  def getMusicById(self, id):
    self.conn.row_factory = MtMusicDB.cbk_dict_factory
    cursor = self.conn.execute("SELECT * FROM music WHERE id = ?;", [id])
    return cursor.fetchone()

  def getMusicByFilename(self, filename):
    self.conn.row_factory = MtMusicDB.cbk_dict_factory
    cursor = self.conn.execute("SELECT * FROM music WHERE filename = ?;", [filename])
    return cursor.fetchone()

  def insertMusic(self, filename):
    name = filename
    artists = ""
    pos = filename.find(' - ')
    if pos > 0:
      artists = filename[:pos]
      name = filename[pos+3:]
    self.conn.execute('''
      INSERT INTO music(filename,artists,name,decibel,tags,miss)
      VAlUES(?,?,?,?,?,?)
    ''', [filename, artists, name, 100, 'new', 1])
    self.conn.commit()

  def updateMissByFileName(self, filename, miss):
    self.conn.execute("UPDATE music SET miss = ? WHERE filename = ?;", [miss, filename])
    self.conn.commit()

  def updateMissById(self, id, miss):
    self.conn.execute("UPDATE music SET miss = ? WHERE id = ?;", [miss, id])
    self.conn.commit()

  def updateMusic(self, id, data):
    self.conn.execute('''
      UPDATE music
      SET 
        filename = ?,
        name = ?,
        artists = ?,
        duration = ?,
        tags = ?,
        decibel = ?,
        rate = ?,
        trackbegin = ?,
        trackend = ?
      WHERE id = ?;
    ''', [
      data.get('filename'),
      data.get('name'),
      data.get('artists'),
      data.get('duration'),
      data.get('tags'),
      data.get('decibel'),
      data.get('rate'),
      data.get('trackbegin'),
      data.get('trackend'),
      id
    ])
    self.conn.commit()
