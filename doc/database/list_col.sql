
CREATE TABLE list_col (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,list_id INTEGER NOT NULL
	,seq INTEGER
);

INSERT INTO list_col (code,name,list_id,seq)
VALUES ('Code','Mã hành động',5,1), ('NAME','Tên hành động',5,2);

INSERT INTO list_col (id,code,name,list_id,seq) VALUES
	 (1,'CODE','Mã danh sách',1,1)
	,(2,'NAME','Tên danh sách',1,2)
	,(3,'CODE','Mã cột',2,1)
	,(4,'NAME','Tên cột',2,2)

;
