import telebot
from telebot.types import ChatPermissions
import datetime

def register(bot):
    @bot.chat_join_request_handler()
    def join_request_handler(request):
        telebot.logger.info(request)
        bot.approve_chat_join_request(request.chat.id , request.from_user.id)
        if not is_Admin(request):
            permissions = ChatPermissions(
                can_send_polls=False, 
                can_change_info=False, 
                can_invite_users=False,
                can_pin_messages=False)
            bot.set_chat_permissions(message.chat.id, permissions)

    @bot.message_handler(content_types=["new_chat_members"])
    def handle_new_chat_members(message):
        current_time = get_current_time()
        for new_member in message.new_chat_members:
            welcome_text = (
                f"👋 Welcome @{new_member.username} to the group! 🎉\n"
                f"📅 Date & Time: {current_time}"
                if new_member.username
                else   f"👋 Welcome {new_member.first_name} to the group! 🎉\n"
                f"📅 Date & Time: {current_time}"
            )
            bot.send_message(message.chat.id, welcome_text)