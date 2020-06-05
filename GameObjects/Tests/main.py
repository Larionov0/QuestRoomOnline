import unittest
import GameObjects.RoomObjects as ro


class RoomObjectTestCase(unittest.TestCase):
    def test_get_quest_rooms_table(self):
        lst = list(ro.QuestRoom.find_all_quest_rooms())
        self.assertEqual(lst, [])
