import telebot
from telebot.types import ChatPermissions

def register(bot):
    def is_admin(chat_id, user_id):
        try:
            member = bot.get_chat_member(chat_id, user_id)
            return member.status in ["administrator", "creator"]
        except:
            return False

    @bot.message_handler(func=lambda message: message.reply_to_message and message.text.startswith('/demote'))
    def demote_user(message):
        if not is_admin(message.chat.id, message.from_user.id):
            bot.reply_to(message, "❌ You must be an admin to demote users.")
            return

        if not message.reply_to_message:
            bot.send_message(message.chat.id, "❌ Reply to an admin's message.")
            return

        user_id = message.reply_to_message.from_user.id

        try:
            bot_admin = bot.get_chat_member(message.chat.id, bot.get_me().id)
            if not bot_admin.can_promote_members:
                bot.send_message(message.chat.id, "⚠️ I need 'Promote Members' permission.")
                return
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Bot error: {str(e)}")
            return

        try:
            target_admin = bot.get_chat_member(message.chat.id, user_id)
            if target_admin.status == "creator":
                bot.send_message(message.chat.id, "⚠️ Cannot demote group owner.")
                return
            if target_admin.status != "administrator":
                bot.send_message(message.chat.id, "⚠️ User is not an admin.")
                return
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Error: {str(e)}")
            return

        try:
            # Revoke ALL admin permissions
            bot.promote_chat_member(
                message.chat.id, 
                user_id,
                is_anonymous=False,
                can_manage_chat=False,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_video_chats=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_manage_topics=False,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False
            )
            bot.send_message(message.chat.id, f"✅ Demoted {message.reply_to_message.from_user.first_name}!")
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Failed to demote: {str(e)}")