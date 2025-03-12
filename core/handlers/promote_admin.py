import telebot
from telebot.types import ChatPermissions

def register(bot):
    @bot.message_handler(commands=['promote'])
    def promote_user(message):
        if not message.reply_to_message:
            bot.send_message(message.chat.id, "❌ Please reply to an admin's message to demote them.")
            return
        user_id = message.reply_to_message.from_user.id
        bot_info = bot.get_me()
        bot_admin = bot.get_chat_member(message.chat.id, bot_info.id)
        target_admin = bot.get_chat_member(message.chat.id, user_id)


        if bot_admin.status not in ["administrator", "creator"]:
            bot.send_message(message.chat.id, "⚠️ I need admin rights to promote users.")
            return

        if not bot_admin.can_promote_members:
            bot.send_message(message.chat.id, "⚠️ I don't have permission to promote/demote members.")
            return

        if target_admin.status in ["administrator", "creator"]:
            bot.send_message(message.chat.id, "⚠️ The user is already an admin.")
            return
        
        if message.reply_to_message:
            bot.promote_chat_member(
                message.chat.id, user_id,
                can_change_info=True, can_delete_messages=True,
                can_invite_users=True, can_restrict_members=True,
                can_pin_messages=True, can_promote_members=True
            )
            bot.send_message(message.chat.id, f"🎩 User {message.reply_to_message.from_user.first_name} is now an admin!")
        else:
            bot.send_message(message.chat.id, "Reply to a user's message to promote them.")