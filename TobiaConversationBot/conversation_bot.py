from telegram.ext import *
import logging

logger = logging.getLogger(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define states
CHOICE, NAME_FIRST, NAME_LAST, HOLIDAY, HOLIDAY_SEA, HOLIDAY_MOUNTAIN = range(6)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a pretty stupid bot, I can talk with you about holidays"
                                                          "or we start to know each other a bit better!")
    return CHOICE


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
    choice = choose_intent(intents, update.message)

    logger.info("Choice was %s, returning state %s" % (choice, new_states[choice]))

    bot.send_message(chat_id=update.message.chat_id, text=messages[choice])
    return new_states[choice]


def first_name(bot, update):
    None


def last_name(bot, update):
    None

def holyday(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Holydays!")


def choose_intent(intent_sets, message):

    logger.info("Choosing intent")
    logger.info(intent_sets, message)

    counts = []

    for k, v in intent_sets.items():
        logger.info(k, v)
        counts.append(sum([1 for w in v if w in message]))

    logger.info(counts)

    # TODO: pretty bad solution, in case of multiple maxs
    return list(intent_sets.keys())[counts.index(max(counts))]

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

            NAME_FIRST: [MessageHandler(Filters.photo, first_name)],

            HOLIDAY: [MessageHandler(Filters.location, holyday)]

        },

        fallbacks=[CommandHandler('cancel', last_name)]
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