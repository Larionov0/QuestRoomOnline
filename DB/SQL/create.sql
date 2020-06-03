USE QuestRoomOnline;

CREATE TABLE PLAYER (
    telegram_chat_id INTEGER PRIMARY KEY,
    username VARCHAR(30) CHECK(LENGTH(username) > 1),
    coins INTEGER
);
