# fileName : Plugins/dm/photo.py
# copyright ©️ 2021 nabilanavab




import os
from pdf import PDF
from PIL import Image
from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> Config var.
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب 🛑"


imageAdded = """`تمت إضافة {} صفحة / إلى ملف pdf ..`🤓
اضغط لإنشاء ملف PDF 🤞 \n
/generate اذا ارت اسم للملف فقط اكتب هذا امر مع فراغ واكتب اسم ملفك """


forceSubMsg = """انتظر [{}](tg://user?id={}) 🤚🏻..!!

يجيب اولاً انضمام للقناة البوت لمتابعة كافة تحديثات البوت 📢 🚶

هذا يعني أنك بحاجة إلى الانضمام إلى القناة المذكورة أدناه لاستخدامي😁😇!

◍ `اضغط على " تحديث ♻️" بعد الانضمام .. 😅😇`"""


button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😉 موقع بوت 😉",
                    url="https://electrical-engineer-cc40b.web.app/"
                )
            ]
       ]
    )

#--------------->
#--------> REPLY TO IMAGES
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.photo)
async def images(bot, message):
    try:
        global invite_link
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link=await bot.create_chat_invite_link(
                        int(UPDATE_CHANNEL)
                    )
                await bot.send_message(
                    message.chat.id,
                    forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🌟 الانضمام إلى القناة  🌟",
                                    url=invite_link.invite_link
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "تحديث ♻️",
                                    callback_data="refresh"
                                )
                            ]
                        ]
                    )
                )
                return
        # CHECKS IF USER BAN/ADMIN..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button
            )
            return
        imageReply = await bot.send_message(
            message.chat.id,
            "`تحميل صورتك ..⏳`",
            reply_to_message_id = message.message_id
        )
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        await message.download(
            f"{message.chat.id}/{message.chat.id}.jpg"
        )
        img = Image.open(
            f"{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        PDF[message.chat.id].append(img)
        await imageReply.edit(
            imageAdded.format(len(PDF[message.chat.id]))
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
