
DROP TABLE 'list';

CREATE TABLE 'list' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'query' TEXT(1024) NOT NULL
	,'hasBack' INTEGER DEFAULT 0 NOT NULL
);

INSERT INTO 'list' ('code','name','query','hasBack') VALUES
	 ('MGR_MENU','Quản lý menu','SELECT id, code, name FROM menu',0)
	,('MGR_LIST','Quản lý danh sách','SELECT id, code, name FROM list',0)
	,('MGR_LIST_FILTER','Quản lý bộ lọc danh sách','SELECT id, code, name FROM list_filter WHERE list_id = {listId} ORDER BY seq',1)
	,('MGR_LIST_COL','Quản lý cột danh sách','SELECT id, code, name FROM list_col WHERE list_id = {listId} ORDER BY seq',1)
	,('MGR_INFO','Quản lý chi tiết','SELECT id, code, name FROM info',0)
	,('MGR_INFO_FIELD','Quản lý trường chi tiết',"SELECT id, code, name FROM info_field WHERE info_id = {infoId}",1)
	,('MGR_TAB','Quản lý Tab','SELECT id, code, name FROM tab',0)
	,('MGR_TAB_PAGE','Quản lý Tab con','SELECT id, code, name FROM tab_page',1)
	,('MGR_ACTION','Quản lý hành động','SELECT id, code, name FROM action WHERE page_type = {pageType} and page_id = {pageId}',1)
	,('MGR_CONTENT','Quản lý nội dung','SELECT id, code, type, data FROM content',0)
;

-- ##############################################################

DROP TABLE 'list_filter';

CREATE TABLE 'list_filter' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'list_id' INTEGER NOT NULL			-- Ref ID
	,'field_type' TEXT(64) NOT NULL		-- TEXT, TEXTAREA, NUMBER, CHECKBOX, SELECTBOX
	,'field_options' TEXT(512)			-- Tùy chỉnh cho loại trường
	,'seq' INTEGER						-- Thứ tự sắp xếp
);

INSERT INTO 'list_filter' ('code','name','list_id','field_type','field_options','seq') VALUES
	-- MGR_LIST
	 ('CODE','Mã danh sách',2,'TEXT',NULL,1)
	,('NAME','Tên danh sách',2,'TEXT',NULL,2)
;

-- ##############################################################

DROP TABLE 'list_col';

CREATE TABLE 'list_col' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'list_id' INTEGER NOT NULL
	,'seq' INTEGER
);

INSERT INTO 'list_col' ('code','name','list_id','seq') VALUES
	-- MGR_MENU
	 ('CODE','Mã menu',1,1)
	,('NAME','Tên menu',1,2)
	-- MGR_LIST
	,('CODE','Mã danh sách',2,1)
	,('NAME','Tên danh sách',2,2)
	-- MGR_LIST_FILTER
	,('CODE','Mã cột',3,1)
	,('NAME','Tên cột',3,2)
	-- MGR_LIST_COL
	,('CODE','Mã cột',4,1)
	,('NAME','Tên cột',4,2)
	-- MGR_INFO
	,('CODE','Mã thông tin',5,1)
	,('NAME','Tên thông tin',5,2)
	-- MGR_INFO_FIELD
	,('CODE','Mã trường thông tin',6,1)
	,('NAME','Tên trường thông tin',6,2)
	-- MGR_TAB
	,('CODE','Mã tab',7,1)
	,('NAME','Tên tab',7,2)
	-- MGR_TAB_PAGE
	,('CODE','Mã tab con',8,1)
	,('NAME','Tên tab con',8,2)
	-- MGR_ACTION
	,('CODE','Mã hành động',9,1)
	,('NAME','Tên hành động',9,2)
	-- MGR_CONTENT
	,('CODE','Mã nội dung',10,1)
	,('TYPE','Cấu trúc',10,2)
	,('DATA','Dữ liệu',10,3)
;
