

-- CONFIG
DROP TABLE 'action';

CREATE TABLE 'action' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'type' INTEGER NOT NULL			-- 1: top, 2: inline
	,'page_type' TEXT(64) NOT NULL		-- LIST, INFO
	,'page_id' INTEGER NOT NULL
	,'func_type' TEXT(64) NOT NULL		-- LINK
	,'func_method' TEXT(64)				-- LINK: url
	,'func_data' TEXT(512)				-- LINK: url
	,'seq' INTEGER						-- Thứ tự sắp xếp
);

INSERT INTO 'action' ('page_id','page_type','code','name','type','func_type','func_method','func_data','seq') VALUES
	-- LIST - MGR_MENU
	 (1,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_MENU',1)
	,(1,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_MENU&id={id}',1)
	-- LIST - MGR_LIST
	,(2,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_LIST',1)
	,(2,'LIST','EDIT_INFO','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_LIST&id={id}',1)
	,(2,'LIST','EDIT_COL','Sửa cột',2,'GO',NULL,'type=LIST&code=MGR_LIST_COL&listId={id}',2)
	,(2,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=LIST&pageId={id}',3)
	-- LIST - MGR_LIST_FILTER
	,(3,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_LIST_FILTER',1)
	,(3,'LIST','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	,(3,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_LIST_FILTER&id={id}',1)
	-- LIST - MGR_LIST_COL
	,(4,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_LIST_COL',1)
	,(4,'LIST','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	,(4,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_LIST_COL&id={id}',1)
	-- LIST - MGR_INFO
	,(5,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_INFO',1)
	,(5,'LIST','EDIT_INFO','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_INFO&id={id}',1)
	,(5,'LIST','EDIT_FIELD','Sửa trường',2,'GO',NULL,'type=LIST&code=MGR_INFO_FIELD&infoId={id}',2)
	,(5,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=INFO&pageId={id}',3)
	-- LIST - MGR_INFO_FIELD
	,(6,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_INFO_FIELD',1)
	,(6,'LIST','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	,(6,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_INFO_FIELD&id={id}',1)
	-- LIST - MGR_TAB
	,(7,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_TAB',1)
	,(7,'LIST','EDIT','Sửa thông tin',2,'GO',NULL,'type=INFO&code=MGR_TAB&id={id}',1)
	,(7,'LIST','EDIT_TAB_PAGE','Sửa tab con',2,'GO',NULL,'type=LIST&code=MGR_TAB_PAGE&tabId={id}',2)
	-- LIST - MGR_TAB_PAGE
	,(8,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_TAB_PAGE',1)
	,(8,'LIST','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	,(8,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_TAB_PAGE&id={id}',1)
	-- LIST - MGR_ACTION
	,(9,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_ACTION',1)
	,(9,'LIST','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	,(9,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_ACTION&id={id}',1)
	-- LIST - MGR_CONTENT
	,(10,'LIST','ADD','Thêm mới',1,'GO',NULL,'type=INFO&code=MGR_CONTENT',1)
	,(10,'LIST','EDIT','Chỉnh sửa',2,'GO',NULL,'type=INFO&code=MGR_CONTENT&id={id}',1)
	
	-- INFO - MGR_MENU
	,(1,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(1,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_LIST
	,(2,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(2,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_LIST_FILTER
	,(3,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(3,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_LIST_COL
	,(4,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(4,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_INFO
	,(5,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(5,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_INFO_FIELD
	,(6,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(6,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_TAB
	,(7,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(7,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_TAB_PAGE
	,(8,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(8,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_ACTION
	,(9,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(9,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
	-- INFO - MGR_CONTENT
	,(10,'INFO','SAVE','Lưu',1,'SAVE',NULL,NULL,1)
	,(10,'INFO','BACK','Quay lại',1,'BACK',NULL,NULL,2)
;