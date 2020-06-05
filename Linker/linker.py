from GameObjects.Exceptions import SingletoneException
from GameObjects.UserEnv import *
from GameObjects.RoomObjects import *
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class Linker:
    """
    Singletone
    """
    instance = None
    bot = None

    def __init__(self, use_this_out_of_class=True):
        if use_this_out_of_class:
            raise SingletoneException("Using out of Class (Singletone)")

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            return cls(use_this_out_of_class=False)
        else:
            return cls.instance


class TextLinker(Linker):
    def answer_to_message(self, message, bot):
        if self.bot is None:
            self.bot = bot
        chat_id = message.chat.id
        player = Player.identify_player(chat_id)
        if player:
            self.main_menu(message)
        else:
            self.player_registration(message)

    def player_registration(self, message):
        chat_id = message.chat.id
        player = Player(chat_id)
        player.create()
        self.bot.reply_to(message, "Зарегистрируйтес, пжлст.\n Введите свой username")
        self.bot.register_next_step_handler(message, self.answer_to_registation_input)

    def answer_to_registation_input(self, message):
        chat_id = message.chat.id
        username = message.text
        if 1 < len(username) <= 30:
            player = Player.identify_player(chat_id)
            player.username = username
            player.save()
            self.bot.reply_to(message, "Вы успешно зарегестрированы!")
            self.main_menu(message)
        else:
            self.bot.send_message('Некорректное имя! Попробуйте еще раз')
            self.bot.register_next_step_handler(message, self.answer_to_registation_input)

    def main_menu(self, message):
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton('Available quest-rooms👁'))
        keyboard.add(KeyboardButton('My profile😃'))
        self.bot.reply_to(message, text='You are in main menu. Your choice:', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.main_menu_choice)

    def main_menu_choice(self, message):
        choice = message.text
        if choice == 'Available quest-rooms👁':
            self.quest_rooms_watching(message)
        # self.bot.reply_to(message, f"Вы выбрали {message.text}")

    def quest_rooms_watching(self, message):
        quest_rooms = QuestRoom.find_all_quest_rooms()
        # keyboard = ReplyKeyboardMarkup()
        # for quest_room in quest_rooms:
        #     keyboard.add(KeyboardButton(str(quest_room)))
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Back to main menu", callback_data=f'quest_rooms_choosing:back'))
        for quest_room in quest_rooms:
            keyboard.add(InlineKeyboardButton(str(quest_room), callback_data=f'quest_rooms_choosing:{quest_room.id}'))
        self.bot.reply_to(message, 'Please choose quest-room', reply_markup=keyboard)


class CallbackLinker(Linker):
    def answer_to_call(self, call, bot):
        if self.bot is None:
            self.bot = bot
        self.bot.answer_callback_query(call.id)

        pseudo_url = call.data.split(':')

        if pseudo_url[0] == 'quest_rooms_choosing':
            self.quest_rooms_choosing(call, pseudo_url[1])
        elif pseudo_url[0] == 'moving_to':
            self.move_to_location(call, int(pseudo_url[1]))

    def quest_rooms_choosing(self, call, choice):
        if choice == 'back':
            if TextLinker.bot is None:
                TextLinker.bot = self.bot
            TextLinker.get_instance().main_menu(call.message)
        else:
            self.start_in_quest_room(call, int(choice))

    def start_in_quest_room(self, call, quest_room_id):
        quest_room = QuestRoom.get_by_id(quest_room_id)
        start_loc = quest_room.start_location
        if start_loc is None:
            self.bot.send_message(call.message.chat.id, 'Location not yet finalized☹ Coming soon')
            if TextLinker.bot is None:
                TextLinker.bot = self.bot
            TextLinker.get_instance().quest_rooms_watching(call.message)
        else:
            player = Player.identify_player(call.message.chat.id)
            player.set_location(start_loc)
            self.on_location_menu(call)

    def move_to_location(self, call, loc_id):
        player = Player.identify_player(call.message.chat.id)
        loc = Location.get_by_id(int(loc_id))
        player_loc = Location.get_by_id(player.get_location_id)
        if player_loc.id in [l.id for l in loc.get_adjacent_locations()]:
            player.set_location(loc)
            self.on_location_menu(call)

    def on_location_menu(self, call):
        player = Player.identify_player(call.message.chat.id)
        my_loc = Location.get_by_id(player.get_location_id)
        nearby = my_loc.get_adjacent_locations()
        keyboard = InlineKeyboardMarkup()
        for loc in nearby:
            keyboard.add(InlineKeyboardButton(f'{loc}', callback_data=f"moving_to:{loc.id}"))
        msg = f"Your location🤔:\n{my_loc}\n\nAvailable locations: "
        self.bot.send_message(player.telegram_chat_id, msg, reply_markup=keyboard)
