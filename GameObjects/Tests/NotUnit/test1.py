import GameObjects.RoomObjects as ro
import DB.db_manager as dbm

qr = list(ro.QuestRoom.find_all_quest_rooms())[2]
print(list(qr.get_rooms()))
db = dbm.DatabaseManager.get_instance()
print(db.get_one_value_of_one_table('QuestRoom', 'name', 1))
