


INSERT INTO action (code,name,type,page_type,page_id,func_type,func_data,seq)
VALUES ('ADD','Thêm mới',1,'LIST',5,'LINK','info/?page=MGR_ACTION',NULL);

-- CONFIG
DROP TABLE ACTION;

CREATE TABLE "action" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,type INTEGER NOT NULL			-- 1: top, 2: inline
	,page_type TEXT(64) NOT NULL	-- LIST, INFO
	,page_id INTEGER NOT NULL
	,func_type TEXT(64) NOT NULL	-- LINK
	,func_data TEXT(256)			-- LINK: url
	,seq INTEGER)					-- Thứ tự sắp xếp
);

-- MGR_LIST List
INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('ADD','Thêm mới',1,'LIST',1,'LINK','info/?page=MGR_LIST',1)
	,('EDIT_INFO','Sửa thông tin',2,'LIST',1,'LINK','info/?page=MGR_LIST&id={id}',1)
	,('EDIT_COL','Sửa cột',2,'LIST',1,'LINK','list/?page=MGR_LIST_COL&listId={id}',2)
	,('EDIT_ACT','Sửa hành động',2,'LIST',1,'LINK','list/?page=MGR_ACTION&pageType=LIST&pageId={id}',3)
;
-- MGR_LIST Info
INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('SUBMIT','Lưu',1,'INFO',1,'SUBMIT',NULL,1)
	,('BACK','Quay lại',1,'INFO',1,'LINK','list/?page=MGR_LIST',2)
;
-- MGR_LIST_COL List
INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('BACK','Quay lại',1,'LIST',2,'LINK','list/?page=MGR_LIST',2)
;
-- MGR_LIST_COL Info
-- MGR_INFO List
-- MGR_INFO Info
-- MGR_ACTION List
INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('ADD','Thêm mới',1,'LIST',5,'LINK','info/?page=MGR_ACTION',1)
	,('EDIT','Chỉnh sửa',1,'LIST',5,'LINK','info/?page=MGR_ACTION&id={id}',2)
	,('BACK','Quay lại',1,'LIST',5,'LINK','list/?page=MGR_LIST',3)
;
-- MGR_ACTION Info
INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('BACK','Quay lại',1,'INFO',2,'LINK','info/?page=MGR_LIST',1)
;
-- MGR_MENU List
-- MGR_MENU Info