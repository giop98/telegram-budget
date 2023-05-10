import json
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from user import User
from user import report_button

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
    logger = logging.getLogger(__name__)

    logger.info("Starting up")

    logger.info("Reading config")

    # Open the conf.json file, that contains the api-key of the telegram bot and the user id
    with open("../conf.json") as f:
        config = json.load(f)

    # Create a new user
    user = User(config["user_id"], config["name"], config["surname"], is_admin=config["is_admin"])

    # Create the application
    application = Application.builder().token(config["api_key"]).build()

    # Add the start command handler
    application.add_handler(CommandHandler("start", user.start_callback))
    application.add_handler(CommandHandler("report", user.report_callback))
    application.add_handler(CallbackQueryHandler(report_button, pattern="1|3|6"))
    application.add_handler(MessageHandler(filters.ALL, user.add_entry_callback))

    application.run_polling()
