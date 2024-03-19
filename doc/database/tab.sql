
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
