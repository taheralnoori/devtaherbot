# fileName : plugins/dm/callBack/asImgOrDoc.py
# copyright ©️ 2021 nabilanavab




from pyrogram import filters
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfReply=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐ معلومات ⭐", callback_data="pdfInfo"),
                InlineKeyboardButton("🗳️ معاينة 🗳️", callback_data="preview")
            ],[
                InlineKeyboardButton("🖼️ الى صور 🖼️", callback_data="toImage"),
                InlineKeyboardButton("✏️ الى نص ✏️", callback_data="toText")
            ],[
                InlineKeyboardButton("🔐 تشفير 🔐", callback_data="encrypt"),
                InlineKeyboardButton("🔒 فك تشفير 🔓",callback_data="decrypt")
            ],[
                InlineKeyboardButton("🗜️ ضغط 🗜️", callback_data="compress"),
                InlineKeyboardButton("🤸 استدارة 🤸", callback_data="rotate")
            ],[
                InlineKeyboardButton("✂️ تقسيم ✂️", callback_data="split"),
                InlineKeyboardButton("🧬 دمج 🧬", callback_data="merge")
            ],[
                InlineKeyboardButton("™️ ختم ™️", callback_data="stamp"),
                InlineKeyboardButton("✏️ إعادة تسمية ✏️", callback_data="rename")
            ],[
                InlineKeyboardButton("📝 مسح ضوئي 📝", callback_data="ocr"),
                InlineKeyboardButton("🥷 A4 تنسيق 🥷", callback_data="format")
            ],[
                InlineKeyboardButton("🤐 ZIP 🤐", callback_data="zip"),
                InlineKeyboardButton("🎯 TAR 🎯", callback_data="tar")
            ],[
                InlineKeyboardButton("🚫 أغلق 🚫", callback_data="closeALL")
            ]
        ]
    )

BTPMcb = """`ماذا تريد أن أفعل بهذا الملف.؟`

اسم الملف: `{}`
حجم الملف: `{}`"""


KBTPMcb = """`ماذا تريد أن أفعل بهذا الملف.؟`

اسم الملف: `{}`
حجم الملف: `{}`

`عدد الصفحات: {}`✌️"""

#--------------->
#--------> LOCAL VARIABLES
#------------------->

"""
______VARIABLES______

I : as image
D : as document
K : pgNo known
A : Extract All
R : Extract Range
S : Extract Single page
BTPM : back to pdf message
KBTPM : back to pdf message (known pages)
______المتغيرات______

I: كصورة
D: كوثيقة
K: صغير معروف
A: استخراج الكل
R: استخراج المدى
S: استخراج صفحة واحدة
BTPM: العودة إلى رسالة pdf
KBTPM: العودة إلى رسالة pdf (الصفحات المعروفة)
"""

#--------------->
#--------> PDF TO IMAGES (CB/BUTTON)
#------------------->


BTPM = filters.create(lambda _, __, query: query.data == "BTPM")
toImage = filters.create(lambda _, __, query: query.data == "toImage")
KBTPM = filters.create(lambda _, __, query: query.data.startswith("KBTPM|"))
KtoImage = filters.create(lambda _, __, query: query.data.startswith("KtoImage|"))

I = filters.create(lambda _, __, query: query.data == "I")
D = filters.create(lambda _, __, query: query.data == "D")
KI = filters.create(lambda _, __, query: query.data.startswith("KI|"))
KD = filters.create(lambda _, __, query: query.data.startswith("KD|"))


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(I)
async def _I(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » مثل Img »الصفحات:           \nمجموع الصفحات: غير معروف _ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄استخراج الكل",
                            callback_data="IA"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق",
                            callback_data="IR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة",
                            callback_data="IS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data="toImage"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(D)
async def _D(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » مثل Doc » الصفحات:           \nمجموع الصفحات: غير معروف _ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄استخراج الكل",
                            callback_data="DA"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق",
                            callback_data="DR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة",
                            callback_data="DS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data="toImage"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KI)
async def _KI(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » مثل Img » الصفحات:           \nمجموع الصفحات: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄استخراج الكل",
                            callback_data=f"KIA|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق",
                            callback_data=f"KIR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة",
                            callback_data=f"KIS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data=f"KtoImage|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KD)
async def _KD(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » مثل Doc » الصفحات:           \nمجموع الصفحات: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄استخراج الكل",
                            callback_data=f"KDA|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق",
                            callback_data=f"KDR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة",
                            callback_data=f"KDS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data=f"KtoImage|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toImage)
async def _toImage(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__ إرسال صور بتنسيق pdf:           \nمجموع الصفحات: غير معروف _ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🖼️صور ",
                            callback_data="I"
                        ),
                        InlineKeyboardButton(
                            "📂مستندات",
                            callback_data="D"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data="BTPM"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoImage)
async def _KtoImage(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__ إرسال صور بتنسيق pdf:           \nمجموع الصفحات: {number_of_pages}__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🖼️صور",
                            callback_data=f"KI|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "📂مستندات",
                            callback_data=f"KD|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "عودة «",
                            callback_data=f"KBTPM|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# back to pdf message (unknown page number)
@ILovePDF.on_callback_query(BTPM)
async def _BTPM(bot, callbackQuery):
    try:
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            BTPMcb.format(
                fileName, await gSF(fileSize)
            ),
            reply_markup = pdfReply
        )
    except Exception:
        pass


# back to pdf message (with known page Number)
@ILovePDF.on_callback_query(KBTPM)
async def _KBTPM(bot, callbackQuery):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            KBTPMcb.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⭐ معلومات الصفحة ⭐", callback_data=f"KpdfInfo|{number_of_pages}"),
                        InlineKeyboardButton("🗳️ معاينة 🗳️", callback_data="Kpreview")
                    ],[
                        InlineKeyboardButton("🖼️ الى صور 🖼️", callback_data=f"KtoImage|{number_of_pages}"),
                        InlineKeyboardButton("✏️ الى نص ✏️", callback_data=f"KtoText|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🔐 تشفير 🔐", callback_data=f"Kencrypt|{number_of_pages}"),
                        InlineKeyboardButton("🔓 فك تشفير 🔓", callback_data=f"notEncrypted")
                    ],[
                        InlineKeyboardButton("🗜️ ضغط 🗜️", callback_data=f"Kcompress"),
                        InlineKeyboardButton("🤸 إستدارة 🤸", callback_data=f"Krotate|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("✂️ تقسيم ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                        InlineKeyboardButton("🧬 دمج 🧬", callback_data="merge")
                    ],[
                        InlineKeyboardButton("™️ ختم ™️", callback_data=f"Kstamp|{number_of_pages}"),
                        InlineKeyboardButton("✏️ إعادة تسمية ✏️", callback_data="rename")
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
    except Exception:
        pass

#                                                                                             Telegram: @nabilanavab
