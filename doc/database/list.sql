
DROP TABLE list;

CREATE TABLE list (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,query TEXT(1024) NOT NULL
);

INSERT INTO list (code,name,query)
VALUES ('NAME','Tên cột',"");

INSERT INTO list (id,code,name,query) VALUES
	 (1,'MGR_LIST','Quản lý danh sách','SELECT id, code, name FROM list')
	,(2,'MGR_LIST_COL','Quản lý cột danh sách','SELECT code, name FROM list_col WHERE list_id = <listId> ORDER BY seq;')
	,(3,'MGR_INFO','Quản lý chi tiết','SELECT id, code, name FROM info')
	,(4,'MGR_MENU','Quản lý menu','SELECT id, code, name FROM menu')
;

UPDATE list SET query = 'SELECT code, name FROM list_col WHERE list_id = <listId> ORDER BY seq;' WHERE id = 2
