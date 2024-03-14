
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

INSERT INTO action (code,name,type,page_type,page_id,func_type,func_data,seq)
VALUES ('SUBMIT','Lưu',1,'INFO',1,'SUBMIT',NULL, NULL);

INSERT INTO "action" (code,name,"type",page_type,page_id,func_type,func_data,seq) VALUES
	 ('ADD','Thêm mới',1,'LIST',1,'LINK','info/?page=MGR_LIST',NULL)
	,('EDIT_INFO','Sửa thông tin',2,'LIST',1,'LINK','info/?page=MGR_LIST&record={code}',NULL)
	,('EDIT_COL','Sửa cột',2,'LIST',1,'LINK','list/?page=MGR_LIST_COL&listId={id}',NULL)
	,('EDIT_ACT','Sửa hành động',2,'LIST',1,'LINK','list/?page=MGR_ACTION&pageType=LIST&pageId={id}',NULL)
	,('BACK','Quay lại',1,'INFO',1,'LINK','list/?page=MGR_LIST',NULL)
	,('SUBMIT','Lưu',1,'INFO',1,'SUBMIT',NULL,NULL)
	,('BACK','Quay lại',1,'LIST',2,'LINK','list/?page=MGR_LIST',NULL)
	,('BACK','Quay lại',1,'LIST',5,'LINK','list/?page=MGR_LIST',NULL)
;
