# cmd: pip install SQLAlchemy

from sqlalchemy import create_engine, text, select, MetaData, Table, Column, Integer, String, Float

engine = create_engine("sqlite+pysqlite:///res/database/music.sqlite", echo=True)

# conn = engine.connect()
# result = conn.execute(text("SELECT * FROM MUSIC"))
# print(result.all())

metadata = MetaData()
music_table = Table("music", metadata,
  Column("id", Integer, nullable=False, primary_key=True),
  Column("filename", String),
  Column("artists", String),
  Column("name", String, nullable=False),
  Column("duration", Float),
  Column("decibel", Integer, default=100),
  Column("tags", String, default='new'),
  Column("miss", Integer),
  Column("rate", Integer),
  Column("trackbegin", Float),
  Column("trackend", Float),
  sqlite_autoincrement=True
)

# Tạo bảng đã định nghĩa
# metadata.create_all(engine)

# Select
conn = engine.connect()
result = conn.execute(select(music_table))
print(result.fetchall())

# INSERT..RETURNING
# conn = engine.connect()
# result = conn.execute(
#   music_table.insert().
#   values(name='foo').
#   returning(music_table.c.col1, music_table.c.col2)
# )
# print(result.all())

# UPDATE..RETURNING
# conn = engine.connect()
# result = conn.execute(
#   music_table.update().
#   where(music_table.c.name=='foo').
#   values(name='bar').
#   returning(music_table.c.col1, music_table.c.col2)
# )
# print(result.all())

# DELETE..RETURNING
# conn = engine.connect()
# result = conn.execute(
#   music_table.delete().
#   where(music_table.c.name=='foo').
#   returning(music_table.c.col1, music_table.c.col2)
# )
# print(result.all())