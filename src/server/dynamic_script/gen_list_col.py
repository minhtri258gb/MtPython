import re

rows = [
	{'id': 1, 'name': 'ID', 'dataType': 'INTEGER'},
	{'id': 2, 'name': 'STR1', 'dataType': 'TEXT(64)'},
	{'id': 3, 'name': 'STR2', 'dataType': 'TEXT(256)'},
	{'id': 4, 'name': 'STR3', 'dataType': 'TEXT(512)'},
	{'id': 5, 'name': 'STR4', 'dataType': 'TEXT(1024)'},
	{'id': 6, 'name': 'STR5', 'dataType': 'TEXT(2048)'},
]

for i, row in enumerate(rows):
	dataType = row.get('dataType')
	if dataType == "INTEGER":
		rows[i]['type'] = 'NUMBER'
	elif dataType.startswith("TEXT"):
		pos = re.search("\([0-9]+\)", dataType)
		length = int(dataType[pos.start()+1:pos.end()-1])
		if length > 500:
			rows[i]['type'] = 'TEXTAREA'
		else:
			rows[i]['type'] = 'TEXT'

print(rows)
