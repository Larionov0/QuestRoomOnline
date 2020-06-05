USE QuestRoomOnline;

CREATE TABLE QuestRoom (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40),
    count_of_players INTEGER,
    complexity INTEGER CHECK (complexity >= 1 and complexity <= 5),
    description VARCHAR(400),
    start_location_id INTEGER NULL
);

CREATE TABLE Room (
    id INTEGER PRIMARY KEY,
    name VARCHAR(60),
    quest_room_id INTEGER references QuestRoom(id)
);

CREATE TABLE Location (
    id INTEGER PRIMARY KEY,
    name VARCHAR(60),
    room_id INTEGER references Room(id)
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
    location_id INTEGER NULL references Location(id)
);

ALTER TABLE QuestRoom
ADD foreign key (start_location_id) references Location(id);
