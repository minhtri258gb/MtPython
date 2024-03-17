import json

def main():
	try:
		str = """
			[
				{"id":1, "code":"A", "parent":null},
				{"id":2, "code":"B", "parent":1},
				{"id":3, "code":"C", "parent":1},
				{"id":4, "code":"D", "parent":1},
				{"id":5, "code":"E", "parent":3},
				{"id":6, "code":"F", "parent":3}
			]
		"""
		obj = json.loads(str) # Str to Obj
		print(obj)
		str = json.dumps(obj) # Obj -> Str
		print(str)

	except Exception as e:
		print(type(e), e)

if __name__ == '__main__':
	main()
