
UPDATE 'info_field'
SET 'options' = 'content:1'
WHERE id = 7;

-- Config
DROP TABLE 'info_field';

CREATE TABLE 'info_field' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'info_id' INTEGER NOT NULL	-- Ref ID
	,'type' TEXT(64) NOT NULL		-- TEXT, TEXTAREA, NUMBER, CHECKBOX, SELECTBOX
	,'options' TEXT(512)			-- Tùy chỉnh cho loại trường
	,'seq' INTEGER				-- Thứ tự sắp xếp
);

/*
option: key:value|key:value|...
	TEXT
	TEXTAREA
	NUMBER
		min: giới hạn dưới
		max: giới hạn trên
		step: bước nhảy
	CHECKBOX
	SELECTBOX
		content: <id content>
*/

-- MGR_INFO
INSERT INTO 'info_field' ('code','name','info_id','type','options','seq') VALUES
	 ('CODE','Mã danh sách',1,'TEXT',NULL,1)
	,('NAME','Tên danh sách',1,'TEXT',NULL,2)
	,('QUERY','Truy vấn',1,'TEXTAREA',NULL,3)
;
-- MGR_ACTION
INSERT INTO 'info_field' ('code','name','info_id','type','options','seq') VALUES
	 ('CODE','Mã trường',2,'TEXT',NULL,1)
	,('NAME','Tên trường',2,'TEXT',NULL,2)
	,('TYPE','Loại trường',2,'SELECTBOX',NULL,3)
	,('PAGE_TYPE','Loại màn hình',2,'SELECTBOX',NULL,4)
	,('PAGE_ID','Màn hình',2,'SELECTBOX',NULL,5)
	,('FUNC_TYPE','Loại chức năng',2,'SELECTBOX',NULL,6)
	,('FUNC_DATA','Nội dung chức năng',2,'TEXTAREA',NULL,7)
	,('SEQ','Thứ tự',2,'NUMBER',NULL,8)
;