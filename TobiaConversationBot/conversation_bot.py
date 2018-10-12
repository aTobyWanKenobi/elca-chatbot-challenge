from telegram.ext import *
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging

logger = logging.getLogger(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define states
CHOICE, NAME_FIRST, NAME_LAST, HOLIDAY, HOLIDAY_SEA, HOLIDAY_MOUNTAIN = range(6)

# Current user name
name = "Bro"
name_given = False

def start(bot, update):

    message = "Since we already know each other, why don't we talk about vacations?" if name_given else "Hey " + name + ", I'm a pretty stupid bot, I can talk with you about holidays or we can start to know each other a bit better!"

    bot.send_message(chat_id=update.message.chat_id, text=message)

    return HOLIDAY if name_given else CHOICE


def choice(bot, update):

    logger.info("CHOICE state")

    intents = {
        'greet': {'greet', 'know', 'name', 'meet', 'hi', 'hey', 'hello'},
        'holiday': {'holiday', 'vacation', 'free time', 'leisure', 'travel', 'weekend', 'summer'}
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


def first_name(bot, update):

    global name
    name = update.message.text

    bot.send_message(chat_id=update.message.chat_id, text="What about your last name?")

    return NAME_LAST


def last_name(bot, update):

    logger.info("giving last name")

    global name, name_given
    name = name + " " + update.message.text
    name_given = True

    bot.send_message(chat_id=update.message.chat_id, text="Well hello " + name + ", nice to meet you, I'm a simple test bot. Let's move on and talk about holidays")

    return HOLIDAY

def holyday(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Holydays!")


def choose_intent(intent_sets, message):

    logger.info("Choosing intent")
    logger.info(intent_sets)
    logger.info(message)

    counts = []

    for k, v in intent_sets.items():
        logger.info(k, v)
        counts.append(sum([1 for w in v if w in message]))

    logger.info(counts)

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

            CHOICE: [MessageHandler(Filters.text, choice)],

            NAME_FIRST: [MessageHandler(Filters.text, first_name)],

            NAME_LAST: [MessageHandler(Filters.text, last_name)],

            HOLIDAY: [MessageHandler(Filters.location, holyday)]

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