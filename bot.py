import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@yourchannelusername"  # example: @exclusive_drops

bot = telebot.TeleBot(TOKEN)

def check_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"),
    )
    keyboard.add(
        InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")
    )

    bot.send_message(
        message.chat.id,
        "Welcome 👋\nGet access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock.",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id

    if check_user_joined(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("🎰 Play Now", url="https://yourlink.com")
        )
        keyboard.add(
            InlineKeyboardButton("🎁 Today's Offer", callback_data="offer")
        )
        keyboard.add(
            InlineKeyboardButton("💬 Support", url="https://t.me/your_support")
        )

        bot.edit_message_text(
            "Unlocked 🎉\nStep 2/2: Continue to the site.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"),
        )
        keyboard.add(
            InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")
        )

        bot.answer_callback_query(call.id, "Not subscribed yet!")
        bot.edit_message_text(
            "Not subscribed yet—join to unlock access.\n\n• Exclusive drops\n• Winner alerts\n• Special bonuses",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )


bot.polling()
