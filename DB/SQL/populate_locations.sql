insert into Location(id, name, room_id)
values (1, 'At the helm', 1);

insert into Location(id, name, room_id)
values (2, 'At the first-aid kit', 1);

insert into Location(id, name, room_id)
values (3, 'Near the sofa', 2);

insert into Location(id, name, room_id)
values (4, 'Under the sofa', 2);

insert into Location(id, name, room_id)
values (5, 'Near the window', 2);

insert into Location(id, name, room_id)
values (6, 'On the toilet', 3);

insert into Location(id, name, room_id)
values (7, 'Under the baseboard', 4);

UPDATE QuestRoom
SET start_location_id = 1
WHERE id = 3;