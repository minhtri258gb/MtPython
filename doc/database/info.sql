
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
	,(2,'QUERY','Truy vấn','TEXTAREA',NULL,NULL,3)
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