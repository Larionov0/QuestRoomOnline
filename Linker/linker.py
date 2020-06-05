from GameObjects.Exceptions import SingletoneException
from GameObjects.UserEnv import *
from GameObjects.RoomObjects import *
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class Linker:
    """
    Singletone
    """
    instance = None
    bot = None

    def __init__(self, use_this_out_of_class=True):
        if use_this_out_of_class:
            raise SingletoneException("Using out of Class (Singletone)")

    @staticmethod
    def get_instance():
        if Linker.instance is None:
            return Linker(use_this_out_of_class=False)
        else:
            return Linker.instance

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
        keyboard.add(KeyboardButton('Просмотр дотупных комнат'))
        keyboard.add(KeyboardButton('Мой профиль'))
        self.bot.reply_to(message, text='Вы находитесь в главном меню. Ваш выбор:', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.menu_choice)

    def menu_choice(self, message):
        self.bot.reply_to(message, f"Вы выбрали {message.text}")

    def answer_to_message(self, message, bot):
        if self.bot is None:
            self.bot = bot
        chat_id = message.chat.id
        player = Player.identify_player(chat_id)
        if player:
            self.main_menu(message)
        else:
            self.player_registration(message)
