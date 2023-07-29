import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class MtCloud:

  h_scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  h_credentials = None
  h_client = None

  m_workbook = None
  m_worksheets_name = []
  m_worksheets = []

  def __init__(self):
    self.h_credentials = ServiceAccountCredentials.from_json_keyfile_name("./res/important/google/mtcloud-392301-d88c7135144e.json", scopes=self.h_scope)
    self.h_client = gspread.authorize(self.h_credentials)
    self.m_workbook = self.h_client.open("Database")

  def getWorkSheetId(self, name):
    index = -1
    try:
      index = self.m_worksheets_name.index(name)
    except:
      worksheet = self.m_workbook.worksheet(name)
      self.m_worksheets_name.append(name)
      self.m_worksheets.append(worksheet)
      index = len(self.m_worksheets) - 1
    finally:
      return index

  def getAll(self, workSheetId):
    worksheet = self.m_worksheets[workSheetId]
    return worksheet.get_all_records()

  def getCols(self, workSheetId, colnum):
    worksheet = self.m_worksheets[workSheetId]
    lst = worksheet.col_values(colnum)
    if len(lst) > 0:
      lst.pop(0) # Bỏ tên cột
    return lst

  def findInCol(self, workSheetId, colnum, value, case_sensitive=True):
    worksheet = self.m_worksheets[workSheetId]
    regex_pattern = re.compile('^'+value+'$')
    lstCell = worksheet.findall(regex_pattern, None, colnum, case_sensitive)
    lstValue = [cell.value for cell in lstCell]
    lstId = [cell.row - 1 for cell in lstCell]
    return lstValue, lstId

  def set(self, workSheetId, range, value):
    worksheet = self.m_worksheets[workSheetId]
    worksheet.update(range, value)
  
  def setCell(self, workSheetId, rownum, colnum, value):
    worksheet = self.m_worksheets[workSheetId]
    worksheet.update_cell(rownum, colnum, value)
