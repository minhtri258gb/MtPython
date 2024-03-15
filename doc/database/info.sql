
DROP TABLE info;

CREATE TABLE info (
	 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,query TEXT(1024) NOT NULL
);

INSERT INTO info ('code','name','query','table') VALUES
	 ('MGR_LIST','Chi tiết màn hình danh sách','SELECT id, code, name, query FROM list WHERE id = ?','list')
	,('MGR_ACTION','Chi tiết màn hình hành động','SELECT id, code, name, type, page_type, page_id, func_type, func_data, seq FROM action WHERE id = ?','action')
;

