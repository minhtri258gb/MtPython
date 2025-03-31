
# Database
## Setup
- Menu
	```sql
	DROP TABLE 'menu';

	CREATE TABLE 'menu' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
		,'parent' INTEGER
		,'link' TEXT(256)
	);

	INSERT INTO 'menu' ('code','name','parent','link') VALUES
		('MGR','Quản lý cấu hình',NULL,NULL)
		,('MGR_MENU','Quản lý menu',1,'/dynamic/page/?type=LIST&code=MGR_MENU')
		,('MGR_LIST','Quản lý danh sách',1,'/dynamic/page/?type=LIST&code=MGR_LIST')
		,('MGR_INFO','Quản lý chi tiết',1,'/dynamic/page/?type=LIST&code=MGR_INFO')
		,('MGR_TAB','Quản lý tab',1,'/dynamic/page/?type=LIST&code=MGR_TAB')
		,('MGR_CONTENT','Quản lý nội dung',1,'/dynamic/page/?type=LIST&code=MGR_CONTENT')
	;
	```
- List
	```sql
	DROP TABLE 'list';

	CREATE TABLE 'list' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
		,'database' TEXT(64)
		,'table' TEXT(64)
		,'query' TEXT(1024) NOT NULL
		,'process' TEXT(256)
		,'hasBack' INTEGER DEFAULT 0 NOT NULL
		,'select' INTEGER DEFAULT 0 NOT NULL
	);

	INSERT INTO 'list' ('code','name','database','table','query','process','hasBack','select') VALUES
		('MGR_MENU','Quản lý menu','dynamic','menu','SELECT id, code, name FROM menu',NULL,0,0)
		,('MGR_LIST','Quản lý danh sách','dynamic','list','SELECT id, code, name, l.''table'' FROM list l',NULL,0,0)
		,('MGR_LIST_FILTER','Quản lý bộ lọc danh sách','dynamic','list_filter','SELECT id, code, name FROM list_filter WHERE list_id = {listId} ORDER BY seq',NULL,1,0)
		,('MGR_LIST_COL','Quản lý cột danh sách','dynamic','list_col','SELECT id, code, name FROM list_col WHERE list_id = {listId} ORDER BY seq',NULL,1,0)
		,('MGR_INFO','Quản lý chi tiết','dynamic','info','SELECT id, code, name FROM info',NULL,0,0)
		,('MGR_INFO_FIELD','Quản lý trường chi tiết','dynamic','info_field','SELECT id, code, name FROM info_field WHERE info_id = {infoId}',NULL,1,0)
		,('MGR_TAB','Quản lý Tab','dynamic','tab','SELECT id, code, name FROM tab',NULL,0,0)
		,('MGR_TAB_PAGE','Quản lý Tab con','dynamic','tab_page','SELECT id, code, name FROM tab_page',NULL,1,0)
		,('MGR_ACTION','Quản lý hành động','dynamic','action','SELECT id, code, name FROM action WHERE page_type = {pageType} and page_id = {pageId}',NULL,1,0)
		,('MGR_CONTENT','Quản lý nội dung','dynamic','content','SELECT id, code, type, data FROM content',NULL,0,0)
		,('GEN_LIST_COL','Tạo cột',NULL,NULL,'SELECT cid id, upper(name) name FROM PRAGMA_TABLE_INFO({listTable}) WHERE pk = 0','gen_list_col',1,2)
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
	```
- Info
	```sql
	DROP TABLE 'info';

	CREATE TABLE 'info' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
		,'query' TEXT(1024) NOT NULL
		,'table' TEXT(64) NOT NULL
	);

	INSERT INTO info ('code','name','query','table') VALUES
		('MGR_MENU','Chi tiết menu','SELECT id, code, name, parent, link FROM menu WHERE id = {rowId}','menu')
		,('MGR_LIST','Chi tiết danh sách','SELECT id, code, name, query FROM list WHERE id = {rowId}','list')
		,('MGR_LIST_FILTER','Chi tiết bộ lọc danh sách','SELECT id, code, name, list_id, seq FROM list_filter WHERE id = {rowId}','list_filter')
		,('MGR_LIST_COL','Chi tiết cột danh sách','SELECT id, code, name, list_id, seq FROM list_col WHERE id = {rowId}','list_col')
		,('MGR_INFO','Chi tiết thông tin','SELECT id, code, name, query, i.''table'' FROM info i WHERE id = {rowId}','info')
		,('MGR_INFO_FIELD','Chi tiết trường thông tin','SELECT id, code, name, info_id, type, options, seq FROM info_field WHERE id = {rowId}','info_field')
		,('MGR_TAB','Chi tiết tab','SELECT id, code, name FROM tab WHERE id = {rowId}','tab')
		,('MGR_TAB_PAGE','Chi tiết tab con','SELECT id, code, name, tab_id FROM tab_page WHERE id = {rowId}','tab_page')
		,('MGR_ACTION','Chi tiết hành động','SELECT id, code, name, type, page_type, page_id, func_type, func_data, seq FROM action WHERE id = {rowId}','action')
		,('MGR_CONTENT','Chi tiết nội dung','SELECT id, code, type, data FROM content WHERE id = {rowId}','content')
	;

	-- ##############################################################

	DROP TABLE 'info_field';

	CREATE TABLE 'info_field' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
		,'info_id' INTEGER NOT NULL	-- Ref ID
		,'type' TEXT(64) NOT NULL	-- TEXT, TEXTAREA, NUMBER, CHECKBOX, SELECTBOX
		,'options' TEXT(512)		-- Tùy chỉnh cho loại trường
		,'default' TEXT(256)		-- Giá trị mặc định
		,'seq' INTEGER				-- Thứ tự sắp xếp
	);

	INSERT INTO 'info_field' ('info_id','code','name','type','options','default','seq') VALUES
		-- MGR_MENU
		(1,'CODE','Mã menu','TEXT',NULL,NULL,1)
		,(1,'NAME','Tên menu','TEXT',NULL,NULL,2)
		,(1,'PARENT','Menu cha','SELECTBOX','content:PARENT_MENU',NULL,3)
		,(1,'LINK','Đường dẫn','TEXT',NULL,NULL,4)
		-- MGR_LIST
		,(2,'CODE','Mã danh sách','TEXT',NULL,NULL,1)
		,(2,'NAME','Tên danh sách','TEXT',NULL,NULL,2)
		,(2,'TABLE','Tên bảng','TEXT',NULL,NULL,3)
		,(2,'QUERY','Truy vấn','TEXTAREA',NULL,NULL,4)
		,(2,'PROCESS','Hàm xử lý','TEXT',NULL,NULL,5)
		,(2,'HAS_BACK','Nút quay lại','CHECKBOX',NULL,NULL,6)
		,(2,'SELECT','Cho phép chọn dòng','NUMBER',NULL,NULL,7)
		-- MGR_LIST_FILTER
		,(3,'CODE','Mã danh sách','TEXT',NULL,NULL,1)
		,(3,'NAME','Tên danh sách','TEXT',NULL,NULL,2)
		,(3,'LIST_ID','Màn hình danh sách','SELECTBOX','content:LIST',NULL,3)
		,(3,'FIELD_TYPE','Loại trường','SELECTBOX','content:FIELD_TYPE',NULL,4)
		,(3,'FIELD_OPTIONS','Tùy chỉnh trường','TEXTAREA',NULL,NULL,5)
		,(3,'SEQ','Thứ tự','NUMBER',NULL,NULL,6)
		-- MGR_LIST_COL
		,(4,'CODE','Mã cột','TEXT',NULL,NULL,1)
		,(4,'NAME','Tên cột','TEXT',NULL,NULL,2)
		,(4,'LIST_ID','Danh sách','SELECTBOX','content:LIST',NULL,3)
		,(4,'SEQ','Thứ tự','NUMBER',NULL,NULL,4)
		-- MGR_INFO
		,(5,'CODE','Mã thông tin','TEXT',NULL,NULL,1)
		,(5,'NAME','Tên thông tin','TEXT',NULL,NULL,2)
		,(5,'QUERY','Truy vấn','TEXTAREA',NULL,NULL,3)
		,(5,'TABLE','Tên bảng','TEXT',NULL,NULL,4)
		-- MGR_INFO_FIELD
		,(6,'CODE','Mã trường','TEXT',NULL,NULL,1)
		,(6,'NAME','Tên trường','TEXT',NULL,NULL,2)
		,(6,'INFO_ID','Chi tiết','SELECTBOX','content:INFO',NULL,3)
		,(6,'TYPE','Loại trường','SELECTBOX','content:FIELD_TYPE',NULL,4)
		,(6,'OPTIONS','Tùy chỉnh trường','TEXTAREA',NULL,NULL,5)
		,(6,'SEQ','Thứ tự','NUMBER',NULL,NULL,6)
		-- MGR_TAB
		,(7,'CODE','Mã tab','TEXT',NULL,NULL,1)
		,(7,'NAME','Tên tab','TEXT',NULL,NULL,2)
		-- MGR_TAB_PAGE
		,(8,'CODE','Mã tab con','TEXT',NULL,NULL,1)
		,(8,'NAME','Tên tab con','TEXT',NULL,NULL,2)
		,(8,'TAB_ID','Tab','SELECTBOX','content:TAB',NULL,3)
		-- MGR_ACTION
		,(9,'CODE','Mã trường','TEXT',NULL,NULL,1)
		,(9,'NAME','Tên trường','TEXT',NULL,NULL,2)
		,(9,'TYPE','Loại trường','SELECTBOX','content:FIELD_TYPE',NULL,3)
		,(9,'PAGE_TYPE','Loại màn hình','SELECTBOX','content:PAGE_TYPE','{pageType}',4)
		,(9,'PAGE_ID','Màn hình','SELECTBOX','content:PAGE','{pageId}',5)
		,(9,'FUNC_TYPE','Loại chức năng','SELECTBOX','content:FUNC_TYPE',NULL,6)
		,(9,'FUNC_DATA','Nội dung chức năng','TEXTAREA',NULL,NULL,7)
		,(9,'SEQ','Thứ tự','NUMBER',NULL,NULL,8)
		-- MGR_CONTENT
		,(10,'CODE','Mã nội dung','TEXT',NULL,NULL,1)
		,(10,'TYPE','Cấu trúc','SELECTBOX','content:CONTENT_TYPE',NULL,2)
		,(10,'DATA','Dữ liệu','TEXTAREA',NULL,NULL,3)
	;
	```
- Tab
	```sql
	DROP TABLE 'tab';

	CREATE TABLE 'tab' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
	);

	INSERT INTO 'tab' ('code','name') VALUES
		('TEST','TEST Tab')
	;

	-- ##############################################################

	DROP TABLE 'tab_page';

	CREATE TABLE 'tab_page' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'name' TEXT(256) NOT NULL
		,'tab_id' INTEGER NOT NULL			-- ref tab_id
		,'page_type' TEXT(64) NOT NULL		-- LIST, INFO
		,'page_id' INTEGER NOT NULL
	);

	INSERT INTO 'tab_page' ('code','name','tab_id','page_type','page_id') VALUES
		('TEST1','Danh sách',1,'LIST',1)
		,('TEST2','Chi tiết 1',1,'INFO',1)
	;
	```
- Action
	```sql
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
		,(1,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_MENU&rowId={id}',1)
		-- LIST - MGR_LIST
		,(2,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST',1)
		,(2,'LIST','EDIT_INFO','Sửa thông tin',2,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST&rowId={id}',1)
		,(2,'LIST','EDIT_COL','Sửa cột',2,'GO',NULL,'type=LIST&code=MGR_LIST_COL&listId={id}&listTable={listTable}',2)
		,(2,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=LIST&pageId={id}',3)
		-- LIST - MGR_LIST_FILTER
		,(3,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_FILTER',1)
		,(3,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_FILTER&rowId={id}',1)
		-- LIST - MGR_LIST_COL
		,(4,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_COL',1)
		,(4,'LIST','GEN','Tạo tự động',1,'POPUP_GO',NULL,'type=LIST&code=GEN_LIST_COL',2)
		,(4,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_LIST_COL&rowId={id}',1)
		-- LIST - MGR_INFO
		,(5,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO',1)
		,(5,'LIST','EDIT_INFO','Sửa thông tin',2,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO&rowId={id}',1)
		,(5,'LIST','EDIT_FIELD','Sửa trường',2,'GO',NULL,'type=LIST&code=MGR_INFO_FIELD&infoId={id}',2)
		,(5,'LIST','EDIT_ACT','Sửa hành động',2,'GO',NULL,'type=LIST&code=MGR_ACTION&pageType=INFO&pageId={id}',3)
		-- LIST - MGR_INFO_FIELD
		,(6,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO_FIELD',1)
		,(6,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_INFO_FIELD&rowId={id}',1)
		-- LIST - MGR_TAB
		,(7,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB',1)
		,(7,'LIST','EDIT','Sửa thông tin',2,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB&rowId={id}',1)
		,(7,'LIST','EDIT_TAB_PAGE','Sửa tab con',2,'GO',NULL,'type=LIST&code=MGR_TAB_PAGE&tabId={id}',2)
		-- LIST - MGR_TAB_PAGE
		,(8,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB_PAGE',1)
		,(8,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_TAB_PAGE&rowId={id}',1)
		-- LIST - MGR_ACTION
		,(9,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_ACTION',1)
		,(9,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_ACTION&rowId={id}',1)
		-- LIST - MGR_CONTENT
		,(10,'LIST','ADD','Thêm mới',1,'POPUP_GO',NULL,'type=INFO&code=MGR_CONTENT',1)
		,(10,'LIST','EDIT','Chỉnh sửa',2,'POPUP_GO',NULL,'type=INFO&code=MGR_CONTENT&rowId={id}',1)
		
	;
	```
- Content
	``` sql

	UPDATE 'content'
	SET 'data' = 'LIST,INFO', 'type' = 'LIST'
	WHERE id = 1

	-- Config

	DROP TABLE 'content';

	CREATE TABLE 'content' (
		'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
		,'code' TEXT(64) NOT NULL
		,'type' TEXT(64) NOT NULL
		,'data' TEXT(1024) NOT NULL
		,'extra' TEXT(256)
	);

	/*
	struct:
		type: LIST: key,key,key,...
		type: PAIR: key:value|key:value|key:value
		type: JSON: {"key":"value","key":{...},"key":[{...},{...},...]}
		type: SQL: SELECT ... FROM ... WHERE ...
	*/

	INSERT INTO 'content' ('code','type','data','extra') VALUES
		('PAGE_TYPE','LIST','LIST,INFO',NULL)
		,('FIELD_TYPE','LIST','TEXT,TEXTAREA,NUMBER,CHECKBOX,SELECTBOX',NULL)
		,('FUNC_TYPE','LIST','GO,BACK,SAVE,POPUP_GO',NULL)
		,('CONTENT_TYPE','LIST','LIST,PAIR,JSON,SQL',NULL)
		,('PARENT_MENU','SQL','SELECT id key, name value FROM menu WHERE 1=1','id: and id!={id}')
		,('LIST','SQL','SELECT id key, name value FROM list',NULL)
		,('INFO','SQL','SELECT id key, name value FROM info',NULL)
		,('TAB','SQL','SELECT id key, name value FROM tab',NULL)
		,('PAGE','SQL','SELECT id key, name value FROM list WHERE ''LIST'' = {page_type} UNION ALL SELECT id key, name value FROM info WHERE ''INFO'' = {page_type}',NULL)
	;
	```
