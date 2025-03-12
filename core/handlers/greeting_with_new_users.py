import telebot
from telebot.types import ChatPermissions
import datetime

GROUP_RULES = """
📜 **Group Rules** 📜
1️⃣ Respect all members.
2️⃣ No offensive language.
4️⃣ Follow admin instructions.
6️⃣ **Admins can:**
    - `/ban` users 🚫
    - `/unban` users ✅
    - `/kick` users 🚪
    - `/pin` messages 📌
    - `/promote` users to admin 🔼
    - `/demote` admins to members 🔽
⚠️ Breaking rules will result in warnings, kicks, or bans.
"""

def register(bot):

    def is_Admin(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        user_info = bot.get_chat_member(chat_id, user_id)
        return user_info.status in ["creator" , "adminstrator"]
    
    @bot.chat_join_request_handler()
    def join_request_handler(request):
        telebot.logger.info(request)
        bot.approve_chat_join_request(request.chat.id , request.from_user.id)
        if not is_Admin(request):
            permissions = ChatPermissions(
                can_send_polls=False, 
                can_change_info=False, 
                can_invite_users=False)
            bot.set_chat_permissions(message.chat.id, permissions)

    @bot.message_handler(content_types=["new_chat_members"])
    def handle_new_chat_members(message):
        current_time = datetime.datetime.now().strftime("%A, %d %B %Y - %I:%M %p")  
        for new_member in message.new_chat_members:
            welcome_text = (
                f"👋 Welcome @{new_member.username} to the group! 🎉\n"
                f"📅 Date & Time: {current_time}"
                if new_member.username
                else   f"👋 Welcome {new_member.first_name} to the group! 🎉\n"
                f"📅 Date & Time: {current_time}"
            )
            bot.send_message(message.chat.id, welcome_text)
            bot.send_message(message.chat.id, GROUP_RULES)