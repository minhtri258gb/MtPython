# cmd:
#  - pip install uvicorn (Run Server)
#  - pip install fastapi (REST API)
#  - pip install strawberry-graphql[fastapi] (GraphQL)
# link: http://localhost:8080

import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import strawberry
from strawberry.fastapi import GraphQLRouter

import mtConfig
import mtMusic

# Init
app = FastAPI()

# Strawberry GraphQL
@strawberry.type
class Query:
  @strawberry.field
  def hello(self) -> str:
    return "Hello World"
schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Core API
@app.get("/abc")
async def index():
  return {"message": "Hello World"}

# Music API
app.include_router(mtMusic.router_graphql, prefix="/music/graphql")

# Static file
app.mount("/", StaticFiles(directory=mtConfig.path_client, html=True, follow_symlink=True), name="static")

# Uvicorn
if __name__ == "__main__":
  uvicorn.run("main:app", host=mtConfig.http_hostname, port=mtConfig.http_port, reload=True)
