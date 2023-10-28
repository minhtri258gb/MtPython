import sqlite3
from flask import request, jsonify

class MtCalendar:
	
	mt = None
	dbMgrPath = './res/database/manager.sqlite'

	def __init__(self, _mt):
		self.mt = _mt

	def register(self):
		@self.mt.app.route("/calendar/get")
		def api_calendar_get():
			return self.api_get()

	def api_get(self):
		sql = "SELECT * FROM date_event WHERE 1=1"
		param = []
		conn = sqlite3.connect(self.dbMgrPath)
		conn.row_factory = MtCalendar.cbk_dict_factory
		rows = conn.execute(sql, param).fetchall()
		conn.close()
		return jsonify(rows), 200
	
	def cbk_dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
