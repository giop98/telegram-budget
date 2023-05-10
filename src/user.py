import telegram
import datetime
import os
import json
from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def report_button(update: Update, context: CallbackContext):
    """Parses the CallbackQuery and returns the report"""
    query = update.callback_query
    await query.answer()
    answer = int(query.data)
    if answer == 1:
        await query.message.reply_text("Report for the last month")
    elif answer == 3:
        await query.message.reply_text("Report for the last 3 months")
    elif answer == 6:
        await query.message.reply_text("Report for the last 6 months")
    elif answer == 12:
        await query.message.reply_text("Report for the last year")
    else:
        await query.message.reply_text("Invalid command")
        return


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
        # Check if the user_id is the same as the config.json
        if str(update.effective_user.id) == str(self.user_id):
            await update.message.reply_text("Hello {} {}!".format(self.name, self.surname))
            commands = [
                telegram.BotCommand("start", "Start the bot"),
                telegram.BotCommand("report", "Get a report")
            ]
            await telegram.Bot.set_my_commands(self=context.bot, commands=commands)

    async def add_entry_callback(self, update: Update, context: CallbackContext):
        """
        Add an entry to the json file

        Parameters
        ---
        update: Update
            The update object
        context: CallbackContext
            The context object

        Returns
        ---
        None
        """
        if str(update.effective_user.id) == str(self.user_id):
            # Get the current time and then get year, month and day
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            day = now.day
            monthly_budget = []
            # Check if the json file exists
            if os.path.exists("../data/{}/{}.json".format(year, month)):
                # Open the json file and load the data
                with open("../data/{}/{}.json".format(year, month)) as f:
                    monthly_budget = json.load(f)
            else:
                # Check if the directory exists
                if not os.path.exists("../data/{}".format(year)):
                    # Create the directory if it doesn't exist
                    os.makedirs("../data/{}".format(year))

            # Split the message
            splitted_message = update.message.text.split(" ")
            # Check the length of the splitted message
            entry_value = ""
            amount_value = ""
            if len(splitted_message) == 2:
                # The format of the text is: <entry> <amount>
                if splitted_message[0].isdigit() and not splitted_message[1].isdigit():
                    entry_value = splitted_message[1]
                    amount_value = splitted_message[0]
                elif not splitted_message[0].isdigit() and splitted_message[1].isdigit():
                    entry_value = splitted_message[0]
                    amount_value = splitted_message[1]
                entry = {
                    "date": "{}-{}-{}".format(year, month, day),
                    "entry": entry_value,
                    "amount": amount_value,
                    "description": "",
                }
                monthly_budget.append(entry)
            elif len(splitted_message) == 3:
                # The format of the text can be: <entry> <amount> <description>
                if splitted_message[0].isdigit() and not splitted_message[1].isdigit():
                    entry_value = splitted_message[1]
                    amount_value = splitted_message[0]
                elif not splitted_message[0].isdigit() and splitted_message[1].isdigit():
                    entry_value = splitted_message[0]
                    amount_value = splitted_message[1]
                entry = {
                    "date": "{}-{}-{}".format(year, month, day),
                    "entry": entry_value,
                    "amount": amount_value,
                    "description": splitted_message[2],
                }
                monthly_budget.append(entry)
            else:
                await update.message.reply_text("Invalid command")
                return

            # Write the data to the json file
            with open("../data/{}/{}.json".format(year, month), "w") as f:
                json.dump(monthly_budget, f, indent=4)
                await update.message.reply_text("Entry added successfully " + "\u2705")

    async def report_callback(self, update: Update, context: CallbackContext):
        # Check if the user id is the correct
        if (str(update.effective_user.id)) == self.user_id:
            buttons = [
                [
                    InlineKeyboardButton("1", callback_data="1"),
                    InlineKeyboardButton("3", callback_data="3"),
                ],
                [
                    InlineKeyboardButton("6", callback_data="6"),
                    InlineKeyboardButton("12", callback_data="12"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            # Reply with a message containing InlineMarkup
            await update.message.reply_text("How many months do you want to consider?", reply_markup=reply_markup)
