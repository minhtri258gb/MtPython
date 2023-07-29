import sqlite3
from flask import request, jsonify

class MtCalendar:
    
  mt = None

  def __init__(self, _mt):
    self.mt = _mt
    self.db = MtCalendarDB()

  def register(self):

    @self.mt.app.route("/calendar/get")
    def api_calendar_get():
      return self.api_get()

    pass

  def api_get(self):
    # self.db.on()
    # lst = self.db.getList(tableName, filter)
    # self.db.off()
    pass

class MtCalendarDB:
  pass