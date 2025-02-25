import telebot
from deep_translator import GoogleTranslator
from better_profanity import profanity
import os

bad_words_file = os.path.join(os.path.dirname(__file__), "list_of_bad_words.txt")

bad_word_list = []
with open(bad_words_file, "r", encoding="utf-8") as file:
    bad_word_list = [line.strip() for line in file.readlines()]
    print(bad_word_list)
    
# Load bad words from the file
profanity.load_censor_words()

def has_bad_word(text):
    """Translate message to English and check for bad words."""
    try:
        translated_text = GoogleTranslator(source="auto", target="en").translate(text)
        return profanity.contains_profanity(translated_text)
    except Exception as e:
        print(f"Translation error: {e}")
        return False 


warnings = {}

def register(bot):
    @bot.message_handler(func = lambda message:True)
    def message_handler(message):
        user_id = str(message.from_user.id)
        if has_bad_word(message.text):
            if user_id in warnings:
                warnings[user_id] += 1
            else :
                warnings[user_id] = 1  
            
            if warnings[user_id] >= 3:
                bot.kick_chat_member(message.chat.id ,message.from_user.id )
                bot.send_message(message.chat.id 
                                , f"User @{message.from_user.username} is kicked out because of breaking bad word rule" 
                                if message.from_user.username
                                else f"User @{message.from_user.first_name} is kicked out because of breaking bad word rule")
            
            else:
                bot.reply_to(message , f"Please don't use bad words , You have {warnings[user_id]} warnings . After third warning you will be removed.")