USE QuestRoomOnline;

SHOW tables;

SELECT * FROM PLAYER;

CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON QuestRoomOnline . * TO 'test_user'@'localhost';
