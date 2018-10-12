from telegram.ext import *
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

import logging

logger = logging.getLogger(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define states
RECOGNIZE_INTENT, ASK_LOCATION, LOCATION = range(3)

# Define intents
intents = {
        'restaurant': {'eat', 'drink', 'hungry', 'thirsty', 'restaurant', 'bar', 'pub', 'meal', 'lunch', 'dinner', 'breakfast', 'brunch', 'pizzeria', 'fast-food'},
        'pharmacy': {'pharmacy', 'medicine', 'cream', 'heal', 'sick', 'ill', 'drug', 'pills'}
        }

# Current intent
current_intent = 'default'


def start(bot, update):

    message = "Hello, what do you need to find?"
    bot.send_message(chat_id=update.message.chat_id, text=message)

    return RECOGNIZE_INTENT


# This is the callback for the state where the bots recognizes the intent
def recognize_intent(bot, update):

    logger.info("RECOGNIZE_INTENT state")

    new_states = {
        'restaurant': LOCATION,
        'pharmacy': LOCATION,
        'default': RECOGNIZE_INTENT
    }

    messages = {
        'restaurant': "So you want to find a restaurant?",
        'pharmacy': "So you want to find a pharmacy?",
        'default': "Sorry I didn't understand. What do you want to find? I can help you with restaurants and pharmacies"
    }

    # Choose intent and answer appropriately
    choice = choose_intent(intents, update.message.text)
    global current_intent
    current_intent = choice

    logger.info("Choice was %s, returning state %s" % (choice, new_states[choice]))

    bot.send_message(chat_id=update.message.chat_id, text=messages[choice])

    return new_states[choice]


def ask_location(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Can you tell me your location?")
    return LOCATION

def wrong_location(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Nono don't tell me, just share your location with me")
    return LOCATION

def location(bot, update):

    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return None


def clean(text) :

    punct = list(string.punctuation)
    stopw = stopwords.words('english')

    tokens = word_tokenize(text)
    filtered_words = [w.lower() for w in tokens if w.lower() not in stopw]
    filtered_words = [w for w in filtered_words if w not in punct]

    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatised = [wordnet_lemmatizer.lemmatize(t) for t in filtered_words]

    return lemmatised


# This method chooses the intent
def choose_intent(intent_sets, message):

    clean_mex = clean(message)

    counts = []

    for k, v in intent_sets.items():
        logger.info(k, v)
        counts.append(sum([1 for w in v if w in clean_mex]))

    max_count = max(counts)

    if max_count == 0:
        # Keep listening if no overlap between sets is found
        return 'default'
    else:
        return list(intent_sets.keys())[counts.index(max_count)]


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

            RECOGNIZE_INTENT: [MessageHandler(Filters.text, recognize_intent)],

            ASK_LOCATION: [MessageHandler(Filters.text, ask_location)],

            LOCATION: [MessageHandler(Filters.location, location),
                       MessageHandler(Filters.text, wrong_location)]

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