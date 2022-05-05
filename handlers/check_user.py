# (c) N A C BOTS


import datetime

import logging

from handlers.database import Database

from fpdf import FPDF
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

db = Database(DB_URL, DB_NAME)

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await bot.send_message(
                LOG_CHANNEL,
                f"#مستخدم_جديد: \n\nمستخدم جديد [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) داس ابدا @{BOT_USERNAME} !!",
            )
        else:
            logging.info(f"#مستخدم_جديد :- اسم : {cmd.from_user.first_name} معرف : {cmd.from_user.id}")

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("أنت ممنوع من استخدام هذا الروبوت ", quote=True)
            return
    await cmd.continue_propagation()
