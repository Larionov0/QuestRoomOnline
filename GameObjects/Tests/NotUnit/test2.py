import GameObjects.RoomObjects as ro
import DB.db_manager as dbm

qr = list(ro.QuestRoom.find_all_quest_rooms())[2]
room = list(qr.get_rooms())[1]
print(list(room.get_locations()))
