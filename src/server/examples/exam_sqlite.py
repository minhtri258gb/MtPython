import sqlite3

def sql_dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def main():
	try:
		conn = sqlite3.connect('./res/database/music.sqlite')
		conn.row_factory = sql_dict_factory # MtSystem.sql_dict_factory
		cursor = conn.execute("SELECT id, tags FROM music")
		lst = cursor.fetchall()
		for music in lst:
			tags = music.get('tags')
			tags = tags.upper()
			conn.execute("UPDATE music SET tags = ? WHERE id = ?", [tags, music.get('id')])
		conn.commit()
		conn.close()
	except Exception as e:
		print(type(e), e)

if __name__ == '__main__':
	main()