USE QuestRoomOnline;

CREATE TABLE QuestRoom (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40),
    count_of_players INTEGER,
    complexity INTEGER CHECK (complexity >= 1 and complexity <= 5)
);

CREATE TABLE Room (
    id INTEGER PRIMARY KEY,
    name VARCHAR(60),
    quest_room_id INTEGER references QuestRoom(id)
);

CREATE TABLE Location (
    id INTEGER PRIMARY KEY,
    name VARCHAR(60)
);

CREATE TABLE AccessLine (
    id INTEGER PRIMARY KEY,
    from_id INTEGER REFERENCES Location(id),
    to_id INTEGER REFERENCES Location(id)
);


CREATE TABLE PLAYER (
    telegram_chat_id INTEGER PRIMARY KEY,
    username VARCHAR(30) CHECK(LENGTH(username) > 1),
    coins INTEGER,
    quest_room_id INTEGER NULL references QuestRoom(id),
    room_id INTEGER NULL references Room(id),
    location INTEGER NULL references Location(id)
);
