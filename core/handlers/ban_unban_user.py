import telebot
from telebot.types import ChatPermissions

def register(bot):
    @bot.message_handler(commands=['ban'])
    def ban_user(message):
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            bot.ban_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, f"⛔ User {message.reply_to_message.from_user.first_name} has been banned!")
        else:
            bot.send_message(message.chat.id, "Reply to a user's message to ban them.")

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
        if len(message.text.split()) > 1:
            user_id = message.text.split()[1]
            bot.unban_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, f"✅ User {message.reply_to_message.from_user.first_name} has been unbanned!")
        else:
            bot.send_message(message.chat.id, "Usage: /unban USER-NAME")