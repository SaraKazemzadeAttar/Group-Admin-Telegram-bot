import telebot
import logging
import os
import sys
import importlib.util
from telebot.types import ChatPermissions 
import importlib

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Add the core directory to Python path
sys.path.append(os.path.dirname(__file__))

handlers_dir = os.path.join(os.path.dirname(__file__), 'handlers')

for file in os.listdir(handlers_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"handlers.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(handlers_dir, file))
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, 'register'):
            module.register(bot)

def is_Admin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        user_info = bot.get_chat_member(chat_id, user_id)
        return user_info.status in ["creator", "administrator"]
    except Exception as e:
        return False

@bot.message_handler(commands=["restrict"])
def handle_restriction(message):
    if not is_Admin(message):
        bot.reply_to(message, "You must be an admin to restrict users!")
        return
    
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_change_info=False
    )
    bot.set_chat_permissions(message.chat.id, permissions)
    bot.delete_message(message.chat.id, message.message_id) 
    bot.send_message(message.chat.id, "USERS ARE RESTRICTED")
    logger.info("Applying restriction")

@bot.message_handler(commands=["unrestrict"])
def handle_unrestriction(message):
    if not is_Admin(message):
        bot.reply_to(message, "You must be an admin to unrestrict users!")
        return
    
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_other_messages=True
    )
    bot.set_chat_permissions(message.chat.id, permissions)
    bot.delete_message(message.chat.id, message.message_id) 
    bot.send_message(message.chat.id, "USERS ARE UNRESTRICTED")
    logger.info("Removing restriction")

bot.infinity_polling()