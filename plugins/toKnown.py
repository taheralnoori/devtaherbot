# fileName : plugins/toKnown.py
# copyright ©️ 2021 nabilanavab

from pyrogram.types import Message
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`ماذا أريد أن أفعل بهذا الملف.؟`

File Name(اسم الملف : `{}`
File Size(حجم الملف) : `{}`

`عدد الصفحات: {}`✌️"""

#--------------->
#--------> EDIT CHECKPDF MESSAGE (IF PDF & NOT ENCRYPTED)
#------------------->

# convert unknown to known page number msgs
async def toKnown(callbackQuery, number_of_pages):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            pdfInfoMsg.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⭐ معلومات ⭐", callback_data=f"KpdfInfo|{number_of_pages}"),
                        InlineKeyboardButton("🗳️ معاينة 🗳️", callback_data="Kpreview")
                    ],[
                        InlineKeyboardButton("🖼️ إلى الصور 🖼️", callback_data=f"KtoImage|{number_of_pages}"),
                        InlineKeyboardButton("✏️ الى نص ✏️", callback_data=f"KtoText|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🔐 تشفير 🔐", callback_data=f"Kencrypt|{number_of_pages}"),
                        InlineKeyboardButton("🔓 فك تشفير 🔓", callback_data=f"notEncrypted")
                    ],[
                        InlineKeyboardButton("🗜️ ضغط 🗜️", callback_data=f"Kcompress"),
                        InlineKeyboardButton("🤸 استدارة 🤸", callback_data=f"Krotate|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("✂️ تقسيم ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                        InlineKeyboardButton("🧬 دمج 🧬",callback_data="merge")
                    ],[
                        InlineKeyboardButton("™️ ️ختم ™️",callback_data=f"Kstamp|{number_of_pages}"),
                        InlineKeyboardButton("✏️ إعادة تسمية ✏️",callback_data="rename")
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
        )
    except Exception as e:
        print(f"plugins/toKnown: {e}")

#                                                                                  Telegram: @nabilanavab
