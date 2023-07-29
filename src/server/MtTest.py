import MtConfig

def test_compare():

  # Get from cloud
  # import MtCloud
  # cloud = MtCloud.MtCloud()
  # sheetId = cloud.getWorkSheetId("music")
  # lstDataCloud = cloud.getAll(sheetId)
  # lstDataCloud = [
  #   {"id":0, "code":"abc1", "name":""},
  #   {"id":1, "code":"abc12", "name":""},
  #   {"id":2, "code":"abc2", "name":"ABC2"},
  #   {"id":3, "code":"abc3", "name":"ABC3"},
  #   {"id":4, "code":"abc4", "name":"ABC4"},
  #   {"id":5, "code":"abc5", "name":"ABC5"},
  #   {"id":6, "code":"abc6", "name":"ABC6"},
  #   {"id":7, "code":"abc7", "name":"ABC7"},
  #   {"id":8, "code":"abc8", "name":"ABC8"},
  #   {"id":9, "code":"abc9", "name":"ABC9"},
  # ]

  # Get from DB
  # import sqlite3
  # conn = sqlite3.connect('./res/database/music.sqlite')
  # def cbk_dict_factory(cursor, row):
  #   d = {}
  #   for idx, col in enumerate(cursor.description):
  #     d[col[0]] = row[idx]
  #   return d
  # conn.row_factory = cbk_dict_factory
  # cursor = conn.execute("SELECT * FROM music")
  # lstDataDB = cursor.fetchall()
  # conn.close()
  # lstDataDB = [
  #   {"id":-1, "code":"abc1", "name":None},
  #   {"id":1, "code":"abc1", "name":None},
  #   {"id":2, "code":"abc2", "name":"ABC2"},
  #   {"id":3, "code":"abc3", "name":"ABC3"},
  #   {"id":4, "code":"abc4", "name":"ABC4"},
  #   {"id":5, "code":"abc5", "name":"ABC5"},
  #   {"id":6, "code":"abc6s", "name":"ABC6"},
  #   {"id":7, "code":"abc7", "name":"ABC7"},
  #   {"id":8, "code":"abc8", "name":"ABC8"},
  #   {"id":9, "code":"abc9", "name":"ABC9"},
  # ]

  # # Compare
  # lstCompare = []
  # while len(lstDataCloud) > 0:
  #   dataCloud = lstDataCloud.pop()
  #   # Tìm 2 id giống nhau
  #   dataDB = next((d for d in lstDataDB if d.get("id") == dataCloud.get("id")), None)
  #   if dataDB != None: # Tìm thấy
  #     lstDataDB.remove(dataDB) # Xóa ở list DB
  #     # So sánh từng value
  #     for key, val1 in dataCloud.items():
  #       val2 = dataDB.get(key)
  #       if val1 == "": val1 = None
  #       if val2 == "": val2 = None
  #       if val1 != val2:
  #         lstCompare.append([dataCloud.get("id"), dataCloud, dataDB])
  #         break
  #   else: # Tìm không thấy
  #     lstCompare.append([dataCloud.get("id"), dataCloud, None]) # Chỉ bên cloud
  # # Nhập list chỉ bên DB
  # lstCompare.extend([d.get("id"), None, d] for d in lstDataDB)

  # sort
  # sorted(lstCompare, key=lambda x: x[0])

  # Save
  # import json
  # with open("./res/dump.json", 'w') as file:
  #   file.write(json.dumps(lstCompare))
  # print(lstCompare)

  # Read for test
  lstCompare = None
  import json
  with open('./res/dump.json') as json_file:
    lstCompare = json.load(json_file)
  print(lstCompare)



  pass

def main():
  try:
    test_compare()
  except Exception as e:
    print(type(e), e)

if __name__ == '__main__':
  main()
