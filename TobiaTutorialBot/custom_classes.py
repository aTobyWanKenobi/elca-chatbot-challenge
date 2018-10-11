from telegram.ext import *

class FilterLucio(BaseFilter):

    def filter(self, message):
        return 'Lucio' in message.text or 'lucio' in message.text