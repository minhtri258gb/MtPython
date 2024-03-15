
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
);

/*
struct:
	type: LIST: key,key,key,...
	type: PAIR: key:value|key:value|key:value
	type: JSON: {"key":"value","key":{...},"key":[{...},{...},...]}
	type: SQL: SELECT ... FROM ... WHERE ...
*/

INSERT INTO 'content' ('code','type','data') VALUES
	 ('PAGE_TYPE','LIST','LIST,INFO')
	,('FIELD_TYPE','LIST','TEXT,TEXTAREA,NUMBER,CHECKBOX,SELECTBOX')
	,('FUNC_TYPE','LIST','LINK,SUBMIT')
	,('PAGE','SQL','SELECT id, name FROM list WHERE 'LIST' = {page_type} UNION ALL SELECT id, name FROM info WHERE 'INFO' = {page_type}')
;

