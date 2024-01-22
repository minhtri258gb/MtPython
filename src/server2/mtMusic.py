# cmd: install SQLAlchemy (Database)
# link: http://localhost:8080/music
# link: http://localhost:8080/music/graphql


# SqlAlchemy
from sqlalchemy import create_engine, select, MetaData, Table, Column, Integer, String, Float

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

engine = create_engine("sqlite+pysqlite:///res/database/music.sqlite", echo=True)


# Strawberry
import typing
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Music:
  id: int
  filename: str
  artists: str
  name: str
  duration: float
  decibel: int
  tags: str
  miss: int
  rate: int
  trackbegin: float
  trackend: float

def searchMusic(): # id=None
  conn = engine.connect()

  sql = select(music_table)
  if (id != None):
    sql.where(music_table.c.id == id)

  result = conn.execute()
  lstTmp = result.fetchall()

  lstRes = []
  for music in lstTmp:
    lstRes.append(Music(
      id          = music[0],
      filename    = music[1],
      artists     = music[2],
      name        = music[3],
      duration    = music[4],
      decibel     = music[5],
      tags        = music[6],
      miss        = music[7],
      rate        = music[8],
      trackbegin  = music[9],
      trackend    = music[10]
    ))

  return lstRes

@strawberry.type
class Query:
  # musics: typing.List[Music] = strawberry.field(resolver=searchMusic)
  @strawberry.field
  def getById(self) -> Music:
    conn = engine.connect()
    sql = select(music_table)
  #   # if (id != None):
  #   #   sql = sql.where(music_table.c.id == id)
    result = conn.execute(sql)
    lstTmp = result.fetchall()
    lstRes = []
    for music in lstTmp:
      lstRes.append(Music(
        id          = music[0],
        filename    = music[1],
        artists     = music[2],
        name        = music[3],
        duration    = music[4],
        decibel     = music[5],
        tags        = music[6],
        miss        = music[7],
        rate        = music[8],
        trackbegin  = music[9],
        trackend    = music[10]
      ))
    return lstRes

schema = strawberry.Schema(Query)
router_graphql = GraphQLRouter(schema)
