
/*
	Pos:
		1: normal
		2: in table data (LIST)
	Type:
		GO / POPUP GO - param in URL
		LINK - url
*/
-- CONFIG
DROP TABLE 'action';

CREATE TABLE 'action' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'page_type' TEXT(64) NOT NULL
	,'page_id' INTEGER NOT NULL
	,'pos' INTEGER NOT NULL
	,'type' TEXT(64) NOT NULL
	,'method' TEXT(64)
	,'data' TEXT(512)
	,'seq' INTEGER
);

INSERT INTO 'action' ('page_id','page_type','code','name','pos','type','method','data','seq') VALUES
	-- LIST - MGR_MENU
	 (1,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_MENU',1)
	,(1,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_MENU&rowId={id}',1)
	-- LIST - MGR_LIST
	,(2,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST',1)
	,(2,'LIST','EDIT_INFO','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_LIST&rowId={id}',1)
	,(2,'LIST','EDIT_COL','Sửa cột',2,'GO',NULL,'type=LIST&code=MGR_LIST_COL&listId={id}',2)
	,(2,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=LIST&pageId={id}',3)
	-- LIST - MGR_LIST_FILTER
	,(3,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_FILTER',1)
	,(3,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_LIST_FILTER&rowId={id}',1)
	-- LIST - MGR_LIST_COL
	,(4,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_COL',1)
	,(4,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_LIST_COL&rowId={id}',1)
	-- LIST - MGR_INFO
	,(5,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO',1)
	,(5,'LIST','EDIT_INFO','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_INFO&rowId={id}',1)
	,(5,'LIST','EDIT_FIELD','Sửa trường',2,'GO',NULL,'type=LIST&code=MGR_INFO_FIELD&infoId={id}',2)
	,(5,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=INFO&pageId={id}',3)
	-- LIST - MGR_INFO_FIELD
	,(6,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO_FIELD',1)
	,(6,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_INFO_FIELD&rowId={id}',1)
	-- LIST - MGR_TAB
	,(7,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB',1)
	,(7,'LIST','EDIT','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_TAB&rowId={id}',1)
	,(7,'LIST','EDIT_TAB_PAGE','Sửa tab con',2,'GO',NULL,'type=LIST&code=MGR_TAB_PAGE&tabId={id}',2)
	-- LIST - MGR_TAB_PAGE
	,(8,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB_PAGE',1)
	,(8,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_TAB_PAGE&rowId={id}',1)
	-- LIST - MGR_ACTION
	,(9,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_ACTION',1)
	,(9,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_ACTION&rowId={id}',1)
	-- LIST - MGR_CONTENT
	,(10,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_CONTENT',1)
	,(10,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_CONTENT&rowId={id}',1)
	
;