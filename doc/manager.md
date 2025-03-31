
# Database
## Startup
- Manager
	```sql
	INSERT INTO 'list' ('code','name','table','query','process','hasBack','select')
	VALUES ('MGR_ANIME','Danh sách Anime','anime','SELECT * FROM anime',NULL,0,1)

	SELECT id FROM list WHERE code = 'MGR_ANIME'
	
	INSERT INTO 'list_col' ('list_id','code','name','seq') VALUES
		 (12,'NAME','Tên',1)
		,(12,'STORY','Story',2)
		,(12,'ART','Art',3)
		,(12,'SOUND','Sound',4)
		,(12,'FANTASY','Fantasy',5)
		,(12,'SAD','Sad',6)
		,(12,'JOKE','Joke',7)
		,(12,'BRAND','Brand',8)
		,(12,'REVIEW','Review',9)
		,(12,'END','End',10)
		,(12,'CHARACTER','Character',11)
		,(12,'UPDATE','Update',12)
	```
