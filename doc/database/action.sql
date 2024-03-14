
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
);

INSERT INTO action (code,name,type,page_type,page_id,func_type,func_data)
VALUES ('EDIT_COL','Sửa cột',2,'LIST',1,'LINK','list/?page=MGR_LIST_COL&record={code}');

INSERT INTO action (id,code,name,type,page_type,page_id,func_type,func_data) VALUES
	 (1,'ADD','Thêm mới',1,'LIST',1,'LINK','info/?page=MGR_LIST')
	,(2,'EDIT_INFO','Sửa thông tin',2,'LIST',1,'LINK','info/?page=MGR_LIST&record={code}')
	,(3,'EDIT_COL','Sửa cột',2,'LIST',1,'LINK','list/?page=MGR_LIST_COL&listId={id}')
	,(4,'BACK','Quay lại',1,'INFO',1,'LINK','list/?page=MGR_LIST')
;
