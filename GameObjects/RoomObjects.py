from .Exceptions import EmptyRoomException
from DB.db_manager import ISaveble, DatabaseManager


class ObjectWithName:
    """Abstract class   """
    _name: str

    @property
    def name(self):
        return self._name


class QuestRoom(ISaveble, ObjectWithName):
    def __init__(self, name, count_of_players, rooms, reward, players=None):
        self._name = name
        self.__count_of_players = count_of_players
        self.__rooms = rooms
        self.__reward = reward
        if players is None:
            players = []
        self.__players = players

    def add_player(self, player):
        if len(self.__players) < self.__count_of_players:
            self.__players.append(player)

    @property
    def count_of_players(self):
        return self.__count_of_players

    def save(self):
        pass


class Room(ISaveble, ObjectWithName):
    def __init__(self, name, locations, players=None):
        if len(locations) == 0:
            raise EmptyRoomException()

        self._name = name
        self._locations = locations
        if players is None:
            players = []
        self._players = players

    def add_location(self, location):
        self._locations.append(location)

    def save(self):
        pass


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


class Location(ISaveble, IAccessible, IShareAccessLine, ObjectWithName):
    def __init__(self, name, used_things, things_lines, adjacent_locations_lines, events, room):
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


class MiniLocation(ISaveble, Location):
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
