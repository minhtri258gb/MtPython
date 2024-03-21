import os
from dotenv import load_dotenv

load_dotenv()

STATIC_SERVER = os.getenv('STATIC_SERVER')
FILE_SERVER = os.getenv('FILE_SERVER')

print(STATIC_SERVER)
print(FILE_SERVER)
