from telegram.ext import *
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging

logger = logging.getLogger(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define states
RECOGNIZE_INTENT, RESTAURANT, PHARMACY = range(3)

def start(bot, update):

    message = "Hello, what do you need to know?"
    bot.send_message(chat_id=update.message.chat_id, text=message)

    return RECOGNIZE_INTENT

# This is the callback for the state where the bots recognizes the intent
def recognize_intent(bot, update):

    logger.info("CHOICE state")

    intents = {
        'restaurant': {},
        'pharmacy': {}
    }

    new_states = {
        'greet': NAME_FIRST,
        'holiday': HOLIDAY
    }

    messages = {
        'greet': "So you want to know each other a bit better? What's your first name?",
        'holiday': "I love holidays, let's speak about that! Do you prefer sea or mountain?"
    }

    # Choose intent and answer appropriately
    choice = choose_intent(intents, update.message.text)

    logger.info("Choice was %s, returning state %s" % (choice, new_states[choice]))

    bot.send_message(chat_id=update.message.chat_id, text=messages[choice])
    return new_states[choice]

# This method chooses the intent
def choose_intent(intent_sets, message):

    counts = []

    for k, v in intent_sets.items():
        logger.info(k, v)
        counts.append(sum([1 for w in v if w in message]))

    # TODO: pretty bad solution, in case of multiple maxs
    return list(intent_sets.keys())[counts.index(max(counts))]

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('639740998:AAFwBteCfMrgGzzTzCIGrWVH6sGcgZN7CJ0')
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={

            RECOGNIZE_INTENT: [MessageHandler(Filters.text, choice)],

            RESTAURANT: [MessageHandler(Filters.text, first_name)],

            PHARMACY: [MessageHandler(Filters.text, last_name)],

        },

        fallbacks=[CommandHandler('cancel', cancel)],

        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()