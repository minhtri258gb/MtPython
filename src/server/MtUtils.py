import re


def process_struct_list(data, style): # Process struct LIST
	result = []
	if data is None or len(data) == 0:
		return result
	lstKey = data.split(',')
	if style == 1:
		result = lstKey
	if style == 2:
		for key in lstKey:
			result.append({"key": key, "value": key})
	return result
def process_struct_pair(data, style): # Process struct PAIR
	if style == 1:
		result = {}
	elif style == 2:
		result = []
	if data is None or len(data) == 0:
		return result
	lstPair = data.split('|')
	for pair in lstPair:
		pos = pair.find(':')
		if pos <= 0:
			raise Exception('Lỗi cấu trúc PAIR: ' + data)
		key = pair[0:pos]
		value = pair[pos+1:]
		if len(key) == 0 or len(value) == 0:
			raise Exception('Lỗi cấu trúc PAIR: ' + data)
		if style == 1:
			result[key] = value
		elif style == 2:
			result.append({"key": key, "value": value})
	return result

def findVar(str): # Find list variable in string
	lstVar = re.findall("\{[a-zA-Z_]+\}", str) # Tìm các biến {name}
	return [var[1:-1] for var in lstVar] # Bỏ dấu {} ở dầu và cuối
def fillVar(str, data):
	lstVar = findVar(str)
	for var in lstVar:
		if not var in data:
			raise Exception("[MtUtils - fillVar] Ko tìm thấy biến trong data: "+var)
		str.replace("{"+var+"}", data[var])
	return str
def fillVarSql(str, data):
	lstVar = findVar(str) # Tìm các biến {name}
	str = re.sub("\{[a-zA-Z_]+\}", "?", str) # Thay các biến thành ?
	params = []
	for var in lstVar:
		if not var in data:
			raise Exception("[MtUtils - fillVarSql] Cấu hình lỗi, biến ko tìm thấy trong form: "+var)
		params.append(data[var])
	return str, params



# ############# Xử lý lại
# def fillVar(data, form, fields, contents):
# 	lst = findVar(data)
# 	for var in lst:
# 		if not var in form:
# 			value = self.getDefaultField(fields, var, contents)
# 			# raise Exception("Cấu hình lỗi, biến ko tìm thấy trong form: "+var)
# 		else:
# 			value = form[var]
# 		data.replace("{"+var+"}", data[var])
# 	return data

# def fillVarSql(data, form, fields, contents):
# 	lst = findVar(data) # Tìm các biến {name}
# 	data = re.sub("\{[a-zA-Z_]+\}", "?", data) # Thay các biến thành ?
# 	params = []
# 	for var in lst:
# 		if not var in form:
# 			value = getDefaultField(fields, var, contents)
# 			# raise Exception("Cấu hình lỗi, biến ko tìm thấy trong form: "+var)
# 		else:
# 			value = form[var]
# 		params.append(value)
# 	return data, params

# def getDefaultField(fields, var, contents):
# 	for field in fields:
# 		if field['code'] == var:
# 			type = field['type']
# 			if type == "TEXT" or type == "TEXTAREA":
# 				return ""
# 			elif type == "NUMBER":
# 				return 0
# 			elif type == 'SELECTBOX':
# 				return contents[field['content']][0]['key']
# 	return None
# ############# Xử lý lại



def removeDuplicate(lst):
	return list(dict.fromkeys(lst))






