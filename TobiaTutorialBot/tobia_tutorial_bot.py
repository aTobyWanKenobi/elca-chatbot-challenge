from telegram.ext import *
from TobiaTutorialBot.command_handlers import *
from TobiaTutorialBot.custom_classes import *
import logging

## Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

## Create updater
updater = Updater(token='639740998:AAFwBteCfMrgGzzTzCIGrWVH6sGcgZN7CJ0')
dispatcher = updater.dispatcher

## Add /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

## Echo all messages
echo_handler = MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)

## /caps command
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

## answer lucio
lucio_filter = FilterLucio()
lucio_handler = MessageHandler(lucio_filter, answer_lucio)
dispatcher.add_handler(lucio_handler)

## Unknown message handler ADD LAST
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
