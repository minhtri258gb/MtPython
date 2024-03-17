
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
	,('MGR_MENU','Quản lý chi tiết',1,'/dynamic/list/?page=MGR_MENU')
	,('MGR_LIST','Quản lý danh sách',1,'/dynamic/list/?page=MGR_LIST')
	,('MGR_INFO','Quản lý chi tiết',1,'/dynamic/list/?page=MGR_INFO')
	,('MGR_TAB','Quản lý tab',1,'/dynamic/list/?page=MGR_TAB')
	,('MGR_CONTENT','Quản lý nội dung',1,'/dynamic/list/?page=MGR_CONTENT')
;
