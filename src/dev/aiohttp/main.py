# cmd: pip install aiohttp
# link: http://localhost:8080

# ko tự gửi file index.html khi đường dẫn ko có dấu / ở cuối

#===================
clientFolder = "D:/Projects/MtClient"
#===================

from aiohttp import web
from aiohttp_index import IndexMiddleware

async def hello(request):
  return web.Response(text="Hello, world")

app = web.Application()
app = web.Application(middlewares=[IndexMiddleware()])
app.add_routes([web.static('/', clientFolder, follow_symlinks=True)])
app.add_routes([web.get('/hello', hello)])

web.run_app(app)