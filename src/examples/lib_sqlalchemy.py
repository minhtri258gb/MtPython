from sqlalchemy import create_engine, select, text

engine = create_engine('sqlite:///res/database/music.sqlite', echo = True)

sql = select(text("* from music")).where(text("music.id = :id"))

conn = engine.connect()
result = conn.execute(sql, {"id": 200}).fetchall()

print(result)