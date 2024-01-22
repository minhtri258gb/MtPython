# cmd:
#  - pip install uvicorn
#  - pip install fastapi
# link: http://localhost

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

#===================
clientFolder = "D:/Projects/MtClient"
#===================

app = FastAPI()

@app.get("/abc")
async def index():
  return {"message": "Hello World"}

app.mount("/", StaticFiles(directory=clientFolder, html=True, follow_symlink=True), name="static")

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
