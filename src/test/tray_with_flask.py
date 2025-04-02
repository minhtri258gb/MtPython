# pip install pystray flask pillow

import sys
import io
import threading
from flask import Flask
import pystray
from PIL import Image, ImageDraw

# Thiết lập encoding cho stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tạo ứng dụng Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

# Hàm tạo hình ảnh cho tray icon
def create_image():
	image = Image.new('RGB', (64, 64), 'white')
	dc = ImageDraw.Draw(image)
	dc.rectangle((16, 16, 48, 48), fill='blue')
	return image

# Hàm xử lý khi nhấn vào tray icon
def on_clicked(icon, item):
	print("asdasd")
	# print(u"Bạn đã nhấn vào tray icon!")

# Hàm chạy tray icon
def run_tray_icon():
	icon = pystray.Icon("test_icon", create_image(), "My Tray Icon", menu=pystray.Menu(
		pystray.MenuItem("Click Me", on_clicked)
	))
	icon.run()

# Chạy tray icon trong một luồng riêng biệt
tray_thread = threading.Thread(target=run_tray_icon)
tray_thread.daemon = True  # Đảm bảo luồng này sẽ kết thúc khi luồng chính kết thúc
tray_thread.start()

# Chạy ứng dụng Flask
if __name__ == '__main__':
	app.run(debug=True)
	