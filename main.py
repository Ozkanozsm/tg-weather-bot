"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests
import datas

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

weatherurl = "https://api.openweathermap.org/data/2.5/weather?units=metric&"


def display_buttons(update: Update, context: CallbackContext) -> None:
    print("START")
    """Sends a message with three inline buttons attached."""
    keyboard = [[]]
    for i in datas.addresses:
        keyboard[0].append(InlineKeyboardButton(i, callback_data=datas.addresses[i]))

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    print("BUTON", update)
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    print("query", query)
    query.answer()
    query.edit_message_text(text=f"Loading...")
    tempurl = weatherurl + query.data + datas.geoapitoken
    print("tempurl", tempurl)
    resjson = requests.get(tempurl).json()
    time.sleep(2)
    nowMain = resjson["main"]
    nowWeather = resjson["weather"][0]["main"]
    print("nowMain", nowMain)
    print("nowWeather", nowWeather)
    print("res", resjson)
    print("qdata", query.data)
    query.edit_message_text(text=f"Weather For - "
                                 f"Weather: {nowWeather} - "
                                 f"Temp: {nowMain['temp']} - "
                                 f"Temp Min: {nowMain['temp_min']} - "
                                 f"Temp Max: {nowMain['temp_max']}")


def help_command(update: Update, context: CallbackContext) -> None:
    print("HELP")
    update.message.reply_text("Use /weather to test this bot.")


def main() -> None:
    print("MAIN")
    """Run the bot."""
    updater = Updater(datas.tgtoken)

    updater.dispatcher.add_handler(CommandHandler('weather', display_buttons))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    print("NAME")
    main()
