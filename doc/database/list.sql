
DROP TABLE 'list';

CREATE TABLE 'list' (
	 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,'code' TEXT(64) NOT NULL
	,'name' TEXT(256) NOT NULL
	,'table' TEXT(64)
	,'query' TEXT(1024) NOT NULL
	,'process' TEXT(256)
	,'hasBack' INTEGER DEFAULT 0 NOT NULL
	,'select' INTEGER DEFAULT 0 NOT NULL
);

INSERT INTO 'list' ('code','name','table','query','process','hasBack','select') VALUES
	 ('MGR_MENU','Quản lý menu','menu','SELECT id, code, name FROM menu',NULL,0,0)
	,('MGR_LIST','Quản lý danh sách','list','SELECT id, code, name, l.''table'' FROM list l',NULL,0,0)
	,('MGR_LIST_FILTER','Quản lý bộ lọc danh sách','list_filter','SELECT id, code, name FROM list_filter WHERE list_id = {listId} ORDER BY seq',NULL,1,0)
	,('MGR_LIST_COL','Quản lý cột danh sách','list_col','SELECT id, code, name FROM list_col WHERE list_id = {listId} ORDER BY seq',NULL,1,0)
	,('MGR_INFO','Quản lý chi tiết','info','SELECT id, code, name FROM info',NULL,0,0)
	,('MGR_INFO_FIELD','Quản lý trường chi tiết','info_field','SELECT id, code, name FROM info_field WHERE info_id = {infoId}',NULL,1,0)
	,('MGR_TAB','Quản lý Tab','tab','SELECT id, code, name FROM tab',NULL,0,0)
	,('MGR_TAB_PAGE','Quản lý Tab con','tab_page','SELECT id, code, name FROM tab_page',NULL,1,0)
	,('MGR_ACTION','Quản lý hành động','action','SELECT id, code, name FROM action WHERE page_type = {pageType} and page_id = {pageId}',NULL,1,0)
	,('MGR_CONTENT','Quản lý nội dung','content','SELECT id, code, type, data FROM content',NULL,0,0)
	,('GEN_LIST_COL','Tạo cột',NULL,'SELECT cid id, upper(name) name FROM PRAGMA_TABLE_INFO({listTable}) WHERE pk = 0','gen_list_col',1,2)
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

INSERT INTO 'list_col' ('list_id','code','name','seq') VALUES
	-- MGR_MENU
	 (1,'CODE','Mã menu',1)
	,(1,'NAME','Tên menu',2)
	-- MGR_LIST
	,(2,'CODE','Mã danh sách',1)
	,(2,'NAME','Tên danh sách',2)
	-- MGR_LIST_FILTER
	,(3.'CODE','Mã cột',1)
	,(3.'NAME','Tên cột',2)
	-- MGR_LIST_COL
	,(4,'CODE','Mã cột',1)
	,(4,'NAME','Tên cột',2)
	-- MGR_INFO
	,(5,'CODE','Mã thông tin',1)
	,(5,'NAME','Tên thông tin',2)
	-- MGR_INFO_FIELD
	,(6,'CODE','Mã trường thông tin',1)
	,(6,'NAME','Tên trường thông tin',2)
	-- MGR_TAB
	,(7,'CODE','Mã tab',1)
	,(7,'NAME','Tên tab',2)
	-- MGR_TAB_PAGE
	,(8,'CODE','Mã tab con',1)
	,(8,'NAME','Tên tab con',2)
	-- MGR_ACTION
	,(9,'CODE','Mã hành động',1)
	,(9,'NAME','Tên hành động',2)
	-- MGR_CONTENT
	,(10,'CODE','Mã nội dung',1)
	,(10,'TYPE','Cấu trúc',2)
	,(10,'DATA','Dữ liệu',3)
	-- MGR_CONTENT
	,(11,'NAME','Tên cột',3)
;
