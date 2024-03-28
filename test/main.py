import os
import unicodedata

path = "D:/musics"
dir_list = os.listdir(path)

files = [unicodedata.normalize('NFC', f) for f in dir_list]

# File Write
mFile = open("./output.txt", 'w', encoding='utf-8')
for f in files:
	mFile.write(f + '\n')
mFile.close()
