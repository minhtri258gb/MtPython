from cryptography.fernet import Fernet

# Authorize
auth_token = "dump"
def auth_set(token):
	global auth_token
	auth_token = token
def auth_check(token):
	global auth_token
	return (token == auth_token)

# SQLite
def sql_dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

# Crypt
crypt = None
def crypt_loadKey():
	global crypt
	if crypt == None:
		with open('./res/cert/serect.key', 'rb') as serectKey:
			key = serectKey.read()
		crypt = Fernet(key)
def crypt_encode(data):
	global crypt
	return crypt.encrypt(data)
def crypt_decode(data):
	global crypt
	return crypt.decrypt(data)

# Console
def console_toogle(toogle):
	import win32gui, win32con, win32console
	hwnd = win32console.GetConsoleWindow()
	if toogle:
		win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
	else:
		win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
	pass
