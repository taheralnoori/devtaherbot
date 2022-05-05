# fileName : Plugins/dm/feedback.py
# copyright ©️ 2021 nabilanavab




from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup




#--------------->
#--------> config vars
#------------------->

BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب 🛑"


feedbackMsg = "[اكتب تعليقًا 📋](https://t.me/engineering_electrical9/719?comment=1)"


button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😉 موقع بوت😉",
                    url="https://electrical-engineer-cc40b.web.app/"
                )
            ]
       ]
    )

#--------------->
#--------> REPLY TO /feedback
#------------------->


@ILovePDF.on_message(filters.private & filters.command(["feedback"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button,
                quote=True
            )
            return
        await bot.send_message(
            message.chat.id, feedbackMsg,
            disable_web_page_preview = True
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
