from DB.db_manager import ISaveble, DatabaseManager


class Player(ISaveble):
    def __init__(self, telegram_chat_id, username=None, coins=0):
        self.telegram_chat_id = telegram_chat_id
        self.username = username
        self.coins = coins

    def create(self):
        DatabaseManager.get_instance().insert_row(
            'Player', {
                'telegram_chat_id': self.telegram_chat_id,
                'username': self.username,
                'coins': self.coins
            }
        )

    def save(self):
        DatabaseManager.get_instance().update_row(self.get_dict(), 'Player', self.telegram_chat_id, 'telegram_chat_id')

    def get_dict(self):
        return {
            'telegram_chat_id': self.telegram_chat_id,
            'username': self.username,
            'coins': self.coins
        }

    @classmethod
    def identify_player(cls, telegram_chat_id):
        player_data = DatabaseManager.get_instance().get_row('Player', telegram_chat_id, primary_str='telegram_chat_id')
        if player_data is None:
            return None
        else:
            return cls(*player_data)
