# fileName : plugins/dm/Callback/pdfMetaData.py
# copyright ©️ 2021 nabilanavab




import fitz
import time
import shutil
from pdf import PROCESS
from pyrogram import filters
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`ماذا تريد أن أفعل بهذا الملف.؟`

أسم الملف: `{}`
حجم الملف: `{}`

`عدد الصفحات: {}`✌️"""

encryptedMsg = """`FILE IS ENCRYPTED` 🔐

أسم الملف: `{}`
حجم الملف: `{}`

`عدد الصفحات: {}`✌️"""

#--------------->
#--------> PDF META DATA
#------------------->

pdfInfo = filters.create(lambda _, __, query: query.data == "pdfInfo")
KpdfInfo = filters.create(lambda _, __, query: query.data.startswith("KpdfInfo"))


@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        # CHECKS PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل .. 🙇"
            )
            return
        # CB MESSAGE DELETES IF USER DELETED PDF
        try:
            fileExist = callbackQuery.message.reply_to_message.document.file_id
        except Exception:
            await bot.delete_messages(
                chat_id = callbackQuery.message.chat.id,
                message_ids = callbackQuery.message.message_id
            )
            return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # DOWNLOADING STARTED
        downloadMessage = await callbackQuery.edit_message_text(
            "`قم بتنزيل ملف pdf ..`⏳",
        )
        pdf_path = f"{callbackQuery.message.message_id}/pdfInfo.pdf"
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = pdf_path,
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS IS DOWNLOADING COMPLETED OR PROCESS CANCELED
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        # OPEN FILE WITH FITZ
        with fitz.open(pdf_path) as pdf:
            isPdf = pdf.is_pdf
            metaData = pdf.metadata
            isEncrypted = pdf.is_encrypted
            number_of_pages = pdf.pageCount
            # CHECKS IF FILE ENCRYPTED
            if isPdf and isEncrypted:
                pdfMetaData = f"\nملف مشفر 🔐\n"
            if isPdf and not(isEncrypted):
                pdfMetaData = "\n"
            # ADD META DATA TO pdfMetaData STRING
            if metaData != None:
                for i in metaData:
                    if metaData[i] != "":
                        pdfMetaData += f"`{i}: {metaData[i]}`\n"
            fileName = callbackQuery.message.reply_to_message.document.file_name
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            if isPdf and not(isEncrypted):
                editedPdfReplyCb=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⭐معلومات ⭐", callback_data=f"KpdfInfo|{number_of_pages}"),
                            InlineKeyboardButton("🗳️ معاينة 🗳️", callback_data=f"Kpreview"),
                        ],[
                            InlineKeyboardButton("إالى صور 🖼️", callback_data=f"KtoImage|{number_of_pages}"),
                            InlineKeyboardButton("إالى نص ✏️", callback_data=f"KtoText|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("تشفير 🔐",callback_data=f"Kencrypt|{number_of_pages}"),
                            InlineKeyboardButton("فك تشفير 🔓", callback_data=f"notEncrypted"
                            )
                        ],[
                            InlineKeyboardButton("ضغط 🗜️", callback_data=f"Kcompress"),
                            InlineKeyboardButton("استدارة 🤸", callback_data=f"Krotate|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("تقسيم ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                            InlineKeyboardButton("دمج 🧬", callback_data="merge")
                        ],[
                            InlineKeyboardButton("ختم ™️", callback_data=f"Kstamp|{number_of_pages}"),
                            InlineKeyboardButton("إعادة تسمية ✏️", callback_data="rename")
                        ],[
                            InlineKeyboardButton("📝 مسح ضوئي 📝", callback_data=f"Kocr|{number_of_pages}"),
                            InlineKeyboardButton("🥷 A4 تنسيق 🥷", callback_data=f"Kformat|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("🤐 ZIP 🤐", callback_data=f"Kzip|{number_of_pages}"),
                            InlineKeyboardButton("🎯 TAR 🎯", callback_data=f"Ktar|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("🚫 أغلق 🚫", callback_data="closeALL")
                        ]
                    ]
                )
                await callbackQuery.edit_message_text(
                    pdfInfoMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup = editedPdfReplyCb
                )
            elif isPdf and isEncrypted:
                await callbackQuery.edit_message_text(
                    encryptedMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🔓فك تشفير",
                                    callback_data = "decrypt"
                                )
                            ]
                        ]
                    )
                )
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    # EXCEPTION DURING FILE OPENING
    except Exception as e:
        try:
            await callbackQuery.edit_message_text(
                f"شئ ما خاطئ .. 🐉\n\nخطأ: {e}",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "❌ خطأ في الملف ❌",
                                callback_data = f"error"
                            )
                        ]
                    ]
                )
            )
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


@ILovePDF.on_callback_query(KpdfInfo)
async def _KpdfInfo(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await bot.answer_callback_query(
            callbackQuery.id,
            text = f"مجموع {number_of_pages} الصفحات 😉",
            show_alert = True,
            cache_time = 0
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
