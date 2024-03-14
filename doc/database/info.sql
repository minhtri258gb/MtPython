

CREATE TABLE info (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	code TEXT(64) NOT NULL,
	name TEXT(256) NOT NULL
);

INSERT INTO info (id,code,name) VALUES
	 (1,'MGR_LIST','Chi tiết màn hình danh sách')
;