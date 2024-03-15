
DROP TABLE list;

CREATE TABLE list (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
	,code TEXT(64) NOT NULL
	,name TEXT(256) NOT NULL
	,query TEXT(1024) NOT NULL
);

INSERT INTO list (code,name,query)
VALUES ('MGR_INFO_FIELD','Quản lý trường chi tiết',"SELECT id, code, name FROM info_field WHERE info_id = {infoId}");

INSERT INTO list (code,name,query) VALUES
	 ('MGR_LIST','Quản lý danh sách','SELECT id, code, name FROM list')
	,('MGR_LIST_COL','Quản lý cột danh sách','SELECT id, code, name FROM list_col WHERE list_id = <listId> ORDER BY seq')
	,('MGR_INFO','Quản lý chi tiết','SELECT id, code, name FROM info')
	,('MGR_INFO_FIELD','Quản lý trường chi tiết',"SELECT id, code, name FROM info_field WHERE info_id = {infoId}")
	,('MGR_ACTION','Quản lý hành động','SELECT id, code, name FROM action WHERE page_type = ''{pageType}'' and page_id = {pageId};')
	,('MGR_MENU','Quản lý menu','SELECT id, code, name FROM menu')
	,('MGR_CONTENT','Quản lý nội dung','SELECT id, code, type, dynamic FROM content')
;

UPDATE list SET query = 'SELECT id, code, name FROM action WHERE page_type = ''{pageType}'' and page_id = {pageId}' WHERE id = 5
