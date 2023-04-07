import telegram
from telegram import Update
from telegram.ext import CallbackContext


async def add_entry_callback(update: Update, context: CallbackContext):
    await update.message.reply_text("You wrote: {}".format(update.message.text))


class User:
    def __init__(self, user_id, name, surname, is_admin=False):
        self.user_id = user_id
        self.name = name
        self.surname = surname

    def get_user_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    async def start_callback(self, update: Update, context: CallbackContext):
        commands = telegram.BotCommand("start", "Start the bots")
        await telegram.Bot.set_my_commands(context.bot, [commands])