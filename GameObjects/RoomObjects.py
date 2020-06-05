from .Exceptions import EmptyRoomException
from DB.db_manager import ISaveble, DatabaseManager, MySQLdb


class ObjectWithName:
    """Abstract class   """
    _name: str

    @property
    def name(self):
        return self._name


class ObjectWithID:
    """Abstract class   """
    _id: int

    @property
    def id(self):
        return self._id


class QuestRoom(ISaveble, ObjectWithName, ObjectWithID):
    def __init__(self, id_, name, count_of_players, complexity=1, description='', start_location_id=None, reward=None, players=None):
        self._id = id_
        self._name = name
        self._count_of_players = count_of_players
        self._complexity = complexity
        self._description = description
        self._reward = reward
        self._start_location_id = start_location_id
        if players is None:
            players = []
        self.__players = players

    @classmethod
    def get_by_id(cls, id_):
        db_manager = DatabaseManager.get_instance()
        row = db_manager.get_row('QuestRoom', id_, columns=['id', 'name', 'count_of_players', 'complexity', 'description'])
        return cls(*row)

    def add_player(self, player):
        if len(self.__players) < self._count_of_players:
            self.__players.append(player)

    @property
    def start_location(self):
        try:
            db_manager = DatabaseManager.get_instance()
            loc_id = db_manager.get_one_value_of_one_table('QuestRoom', 'start_location_id', self.id)
            return Location.get_by_id(loc_id)
        except MySQLdb._exceptions.OperationalError:
            return None

    @property
    def start_location_id(self):
        return self.start_location_id

    @property
    def count_of_players(self):
        return self._count_of_players

    @property
    def complexity(self):
        return self._complexity

    @property
    def description(self):
        return self._description

    @property
    def rooms(self):
        pass

    @property
    def count_of_players(self):
        return self._count_of_players

    def save(self):
        pass

    @classmethod
    def find_all_quest_rooms(cls):
        db_manager = DatabaseManager.get_instance()
        table = db_manager.get_table('QuestRoom', ['id', 'name', 'count_of_players', 'complexity', 'description'])
        for row in table:
            yield cls(*row)

    def get_rooms(self):
        return Room.get_rooms_by_quest_room(self)

    def __str__(self):
        return f"{self.id}. {self.name}  (complexity:{self.complexity}) {self._description[:20]}..."

    def __repr__(self):
        return "< " + self.__str__() + ">"


class Room(ISaveble, ObjectWithName, ObjectWithID):
    def __init__(self, id_, name, quest_room, locations=None, players=None):
        self._id = id_
        self._name = name
        self._quest_room = quest_room
        self._locations = locations
        if players is None:
            players = []
        self._players = players

    @classmethod
    def get_by_id(cls, id_):
        db_manager = DatabaseManager.get_instance()
        row = db_manager.get_row('Room', id_, columns=['name', 'quest_room_id'])
        quest_room = QuestRoom.get_by_id(row[1])
        return cls(id_, row[0], quest_room)

    def add_location(self, location):
        self._locations.append(location)

    def save(self):
        pass

    @property
    def quest_room(self):
        return self._quest_room

    @classmethod
    def get_rooms_by_quest_room(cls, quest_room):
        db_manager = DatabaseManager.get_instance()
        table = db_manager.get_table('Room', ['id', 'name'], f'quest_room_id = {quest_room.id}')
        for row in table:
            yield Room(row[0], row[1], quest_room)

    def get_locations(self):
        return Location.get_locations_by_room(self)

    def __str__(self):
        return f"{self._id} Room: {self._name} (in {self._quest_room.name})"

    def __repr__(self):
        return f"<{self.__str__()}>"


class IAccessible:
    """
    Интерфейс, который реализует обьекты, на которые
    могут ссылаться обьекты AccessLine.
    (Location, Thing)
    """

    def check_access_line(self, line):
        pass


class IShareAccessLine:
    """Interface"""

    def get_all_accessible_objects(self, player, signals):
        pass


class Location(ISaveble, IAccessible, IShareAccessLine, ObjectWithName, ObjectWithID):
    def __init__(self, id_, name, room, used_things=None, things_lines=None, adjacent_locations_lines=None, events=None):
        self._id = id_
        self._name = name
        self._used_things = used_things
        self._things_lines = things_lines
        self._adjacent_locations_lines = adjacent_locations_lines
        self._events = events
        self._room = room

    def add_adjacent_location(self, access_line_to, access_line_from, location):
        self._adjacent_locations_lines.append(access_line_to)
        access_line_to.to_ = location
        access_line_to.from_ = self

        location._adjacent_locations_lines.append(access_line_from)
        access_line_from.to_ = self
        access_line_from.from_ = location

        if location not in self._room:
            self._room.add_location(location)

    def base_add_location(self, location):
        line_to = AccessLine()
        line_from = AccessLine()
        self.add_adjacent_location(line_to, line_from, location)

    def add_event(self, event):
        self._events.append(event)

    def check_access_line(self, line):
        return line.to_ is self

    def get_all_accessible_objects(self, player, signals):
        for line in self._adjacent_locations_lines:
            if line.check_conditions(player, signals):
                yield line.to_

    def save(self):
        pass

    @classmethod
    def get_locations_by_room(cls, room):
        db_manager = DatabaseManager.get_instance()
        table = db_manager.get_table('Location', ['id', 'name'], f'room_id = {room.id}')
        for row in table:
            yield Location(row[0], row[1], room)

    def get_adjacent_locations(self):
        db_manager = DatabaseManager.get_instance()

        query = f"""
                        SELECT Location.id, Location.name, Location.room_id FROM
                        (
                        SELECT * FROM AccessLine
                        WHERE AccessLine.from_id = {self._id}
                        ) as temp
                        JOIN Location ON temp.to_id = Location.id
                """
        result = db_manager.execute(query, True)
        for row in result:
            if row[2] == self._room.id:
                room = self._room
            else:
                r = db_manager.get_row('Room', row[2])
                room = Room(r[0], r[1], self._room.quest_room)
            yield Location(row[0], row[1], room)

    @classmethod
    def get_by_id(cls, id_):
        db_manager = DatabaseManager.get_instance()
        row = db_manager.get_row('Location', id_, columns=['name', 'room_id'])
        room = Room.get_by_id(row[1])
        return cls(id_, row[0], room)

    def __str__(self):
        return f"({self._id}) {self._name} (in {self._room.name})"

    def __repr__(self):
        return f"<{self.__str__()}>"


class MiniLocation(Location):
    def save(self):
        pass


class AccessLine(ISaveble):
    def __init__(self, conditions=None, to_=None, from_=None):
        if conditions is None:
            self.conditions = {}
        self._to_ = to_
        self._from_ = from_

    def check_conditions(self, player, signals):
        for condition in self.conditions:
            try:
                if condition.check(player, signals):
                    return True
            except AttributeError:
                continue

        return False

    def save(self):
        pass
