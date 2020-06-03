import telebot
from Linker.linker import Linker

bot = telebot.TeleBot(token="1244457932:AAEq93X5pDntEDivxdOuJg9fxRBrL_rZbzw")


class BotManager:
    def run(self):
        pass

    @staticmethod
    @bot.message_handler(commands=['start'])
    def on_start(message):
        Linker.get_instance().answer_to_message(message, bot)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def on_message(message):
        Linker.get_instance().answer_to_message(message, bot)


def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)
print("Starting...")
bot.polling(none_stop=True)
