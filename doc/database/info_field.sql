
CREATE TABLE info_field (
	 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,info_id INTEGER NOT NULL	-- Ref ID
	,type TEXT(64) NOT NULL		-- TEXT, TEXTAREA, CHECKBOX, 
	,seq INTEGER				-- Thứ tự sắp xếp
);

INSERT INTO info_field (code,name,info_id,type,seq) VALUES
	 ('CODE','Mã danh sách',1,'TEXT',1)
	,('NAME','Tên danh sách',1,'TEXT',2)
	,('QUERY','Truy vấn',1,'AREA_TEXT',3)
;
