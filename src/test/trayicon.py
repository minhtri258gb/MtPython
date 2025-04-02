# pip install pystray

import pystray
from PIL import Image, ImageDraw

# Tạo một hình ảnh đơn giản cho biểu tượng
def create_image():
	image = Image.new('RGB', (64, 64), 'white')
	dc = ImageDraw.Draw(image)
	dc.rectangle((16, 16, 48, 48), fill='blue')
	return image

# Hàm xử lý khi nhấn vào biểu tượng
def on_clicked(icon, item):
	print("TrayIcon Click!")

# Tạo biểu tượng
icon = pystray.Icon("test_icon", create_image(), "My Tray Icon", menu=pystray.Menu(
	pystray.MenuItem("Click Me", on_clicked)
))

# Chạy biểu tượng
icon.run()

print("ANY")
