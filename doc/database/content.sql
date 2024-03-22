
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
