# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab




from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup





#--------------->
#--------> LOCAL VARIABLES
#------------------->

welcomeMsg = """مرحبا [{}](tg://user?id={})..!!🌝💛
سيساعدك هذا الروبوت على القيام بأشياء كثيرة باستخدام ملفات pdf 

بعض الميزات الرئيسية هي:
◍ `تحويل الصور إلى PDF`
◍ `تحويل ملفات PDF إلى صور`
◍ `تحويل الملفات إلى pdf`

Dev&eng: @ta_ja199 👨‍💻

[💡 موسوعة المهندس الكهربائي 💡 🏆](https://electrical-engineer-cc40b.web.app/)
[اكتب تعليقًا 📋](https://t.me/engineering_electrical9/719?comment=1)"""


UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب 🛑"


forceSubMsg = """انتظر [{}](tg://user?id={})..!!

نظرًا لحركة المرور الهائلة ، يمكن لأعضاء القناة فقط استخدام هذا الروبوت 🚶

هذا يعني أنك بحاجة إلى الانضمام إلى القناة المذكورة أدناه لاستخدامي!

اضغط على "أعد المحاولة ♻️" بعد الانضمام .. 😅"""


aboutDev = """مطور البوت: @ta_ja199
قناة البوت :@engineering_electrical9

[موسوعة المهندس الكهربائي 🏆](https://electrical-engineer-cc40b.web.app/)
[اكتب تعليقًا 📋](https://t.me/engineering_electrical9/719?comment=1)"""


exploreBotEdit = """
[العمل قيد الإنجاز

الانضمام إلى قناة بوت 💎](https://t.me/engineering_electrical9/)
"""


foolRefresh = "سوف يتم تحديث بوت 😐"

#--------------->
#--------> config vars
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> /start (START MESSAGE)
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["start"]))
async def start(bot, message):
        global invite_link
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        # CHECK IF USER BANNED, ADMIN ONLY..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await bot.send_message(
                message.chat.id, UCantUse
            )
            return
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
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
                                    "🌟 الانضمام إلى القناة 🌟",
                                    url = invite_link.invite_link
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "تحديث ♻️",
                                    callback_data = "refresh"
                                )
                            ]
                        ]
                    )
                )
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                return
        
        await bot.send_message(
            message.chat.id,
            welcomeMsg.format(
                message.from_user.first_name,
                message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌟 حول البوت 🌟",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "استكشف البوت 🎊",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "أغلق 🚶",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        # DELETES /start MESSAGE
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = message.message_id
        )


#--------------->
#--------> START CALLBACKS
#------------------->


strtDevEdt = filters.create(lambda _, __, query: query.data == "strtDevEdt")
exploreBot = filters.create(lambda _, __, query: query.data == "exploreBot")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")



@ILovePDF.on_callback_query(strtDevEdt)
async def _strtDevEdt(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            aboutDev,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💎 موقع البوت💎",
                            url = "https://electrical-engineer-cc40b.web.app/"
                        ),
                        InlineKeyboardButton(
                            "الصفحة الرئيسية 🏡",
                            callback_data = "back"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "أغلق 🚶",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(exploreBot)
async def _exploreBot(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            exploreBotEdit,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "الصفحة الرئيسية 🏡",
                            callback_data = "back"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "أغلق 🚶",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌟 حول البوت 🌟",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "استكشاف المزيد 🎊",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "اغلق 🚶",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(refresh)
async def _refresh(bot, callbackQuery):
    try:
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        await bot.get_chat_member(
            str(UPDATE_CHANNEL),
            callbackQuery.message.chat.id
        )
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌟 حول البوت 🌟",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "استكشاف المزيد 🎊",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "أغلق 🚶",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
    except Exception:
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                callbackQuery.id,
                text = foolRefresh,
                show_alert = True,
                cache_time = 0
            )
        except Exception as e:
            print(e)


@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        await bot.delete_messages(
            chat_id = callbackQuery.message.chat.id,
            message_ids = callbackQuery.message.message_id
        )
        return
    except Exception as e:
        print(e)


#                                                                                  Telegram: @nabilanavab
