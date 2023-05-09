import telegram
import datetime
import os
import json
from telegram import Update
from telegram.ext import CallbackContext
from category import check_category, set_category


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
            commands = telegram.BotCommand("start", "Start the bot")
            await telegram.Bot.set_my_commands(context.bot, [commands])

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
            if os.path.exists("../data/{}/{}.json".format(year, month)):
                # Open the json file and add the entry
                with open("../data/{}/{}.json".format(year, month)) as f:
                    monthly_budget = json.load(f)
                splitted_message = update.message.text.split(" ")
                # Check the length of the splitted message
                if len(splitted_message) == 2:
                    # The format of the text is: <entry> <amount>
                    entry = {
                        "date": "{}-{}-{}".format(year, month, day),
                        "entry": splitted_message[0],
                        "amount": splitted_message[1],
                        "description": "",
                    }
                    check_category()
                    monthly_budget.append(entry)
                elif len(splitted_message) == 3:
                    # The format of the text is: <entry> <amount> <description>
                    entry = {
                        "date": "{}-{}-{}".format(year, month, day),
                        "entry": splitted_message[0],
                        "amount": splitted_message[1],
                        "description": splitted_message[2],
                    }
                    monthly_budget.append(entry)
                    pass
                else:
                    await update.message.reply_text("Invalid command")
                    return
                # Add the entry
            else:
                # Create the directory if it doesn't exist
                os.mkdir("../data/{}".format(year))
            # Write the data to the json file
            with open("../data/{}/{}.json".format(year, month), "w") as f:
                json.dump(monthly_budget, f, indent=4)
