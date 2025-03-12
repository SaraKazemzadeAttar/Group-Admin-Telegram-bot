import logging
import telebot
from telebot import types
from telebot.types import ChatPermissions

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def register(bot):
    # Temporary test command
    @bot.message_handler(commands=['check_perms'])
    def check_perms(message):
        bot_member = bot.get_chat_member(message.chat.id, bot.get_me().id)
        bot.reply_to(message, f"Bot status: {bot_member.status}\nCan pin: {bot_member.can_pin_messages}")
    def is_admin(message):
        try:
            user = bot.get_chat_member(message.chat.id, message.from_user.id)
            return user.status in ["creator", "administrator"]
        except Exception as e:
            logger.error(f"Admin check error: {e}")
            return False

    def bot_is_admin(chat_id):
        try:
            bot_member = bot.get_chat_member(chat_id, bot.get_me().id)
            # Check both admin status and pin permission
            return bot_member.status in ["administrator", "creator"] and bot_member.can_pin_messages
        except Exception as e:
            logger.error(f"Bot admin check error: {e}")
            return False

    @bot.message_handler(commands=['pin'])
    def handle_pin_command(message):
        if not is_admin(message):
            bot.reply_to(message, "❌ You must be an admin to use this command.")
            return

        if not bot_is_admin(message.chat.id):
            bot.reply_to(message, "❌ I need admin privileges with 'Pin Messages' permission.")
            return

        if not message.reply_to_message:
            msg = bot.reply_to(message, "🔍 Reply to a message to pin it.", allow_sending_without_reply=True)
            bot.register_next_step_handler(msg, confirm_pin)
            return

        pin_message(message)

    def confirm_pin(message):
        if not message.reply_to_message:
            bot.reply_to(message, "❌ You must reply to a message.")
            return

        pin_message(message)

    def pin_message(message):
        try:
            bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id,
                disable_notification=False 
            )
            bot.reply_to(message, "📌 Message pinned!", allow_sending_without_reply=True)
        except Exception as e:
            logger.error(f"Pin failed: {e}")
            bot.reply_to(message, f"❌ Failed to pin: {str(e)}")