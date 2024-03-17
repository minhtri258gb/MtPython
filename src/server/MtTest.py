import sqlite3
import json
import MtConfig
import MtSystem

class MtTest:
	mt = None
	def __init__(self, _mt):
		self.mt = _mt
	def register(self):
		pass

def main():
	try:
		menus = json.loads("""
			[
				{"id":1, "code":"A", "parent":null},
				{"id":2, "code":"B", "parent":1},
				{"id":3, "code":"C", "parent":1},
				{"id":4, "code":"D", "parent":1},
				{"id":5, "code":"E", "parent":3},
				{"id":6, "code":"F", "parent":3}
			]
		""")

		# Insert child into parent
		lstRootId = []
		for i, menu in enumerate(menus):
			parentId = menu['parent']
			if parentId is None:
				lstRootId.append(i)
			else:
				# Find id
				parentStt = -1
				for j, menu2 in enumerate(menus):
					if menu2['id'] == parentId:
						parentStt = j
						break
				if parentStt >= 0:
					if 'child' not in menus[parentStt]:
						menus[parentStt]['child'] = []
					menus[parentStt]['child'].append(menu)
		# Select root menu
		treeMenu = [menu for i, menu in enumerate(menus) if i in lstRootId]
		print(treeMenu)
		pass
	except Exception as e:
		print(type(e), e)

if __name__ == '__main__':
	main()
