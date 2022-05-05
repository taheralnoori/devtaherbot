# fileName : plugins/dm/callBack/split.py
# copyright ©️ 2021 nabilanavab
import time
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

pdfInfoMsg = """`ماذا تريد أن أفعل بهذا الملف.؟`

أسم الملف: `{}`
حجم الملف: `{}`

`عدد الصفحات: {}`✌️
"""

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

# ----- ----- ----- ----- ----- ----- ----- CALLBACK SPLITTING PDF ----- ----- ----- ----- ----- ----- -----

split = filters.create(lambda _, __, query: query.data == "split")
Ksplit = filters.create(lambda _, __, query: query.data.startswith("Ksplit|"))

splitR = filters.create(lambda _, __, query: query.data == "splitR")
splitS = filters.create(lambda _, __, query: query.data == "splitS")

KsplitR = filters.create(lambda _, __, query: query.data.startswith("KsplitR|"))
KsplitS = filters.create(lambda _, __, query: query.data.startswith("KsplitS|"))



# Split pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__تقسيم pdf » الصفحات:            \n\nإجمالي عدد الصفحات:__ `unknown(مجهول)`",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "مع نطاق 🦞",
                            callback_data = "splitR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "صفحة واحدة 🐛",
                            callback_data = "splitS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data = "BTPM"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Split pgNo (with known pdf page number)
@ILovePDF.on_callback_query(Ksplit)
async def _Ksplit(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"تقسيم pdf » الصفحات:          \n\nإجمالي عدد الصفحات: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "مع نطاق 🦞",
                            callback_data = f"KsplitR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "صفحة واحدة 🐛",
                            callback_data = f"KsplitS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة «",
                            callback_data = f"KBTPM|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitR)
async def _splitROrS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل ..🙇"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        nabilanavab = True; i = 0
        while(nabilanavab):
            
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = "__Pdf تقسيم » حسب النطاق\nالآن ، أدخل النطاق (البداية: النهاية): __\n\n/exit __للإلغاء__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                break
            
            pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`خطأ في بناء الجملة: تحتاج فقط إلى البداية والنهاية`🚶"
                )
            
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                
                if start.isdigit() and end.isdigit():
                
                    if (1 <= int(pageStartAndEnd[0])):
                        
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                            nabilanavab = False
                            break
                        
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`خطأ في بناء الجملة: خطأ في إنهاء رقم الصفحة `🚶"
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`خطأ في بناء الجملة: خطأ في بدء رقم الصفحة `🚶"
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`خطأ في بناء الجملة: يجب أن يكون رقم الصفحة رقمًا` 🧠"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`خطأ في بناء الجملة: لا يوجد رقم صفحة منتهية أو ليس رقمًا` 🚶"
                )
        
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if nabilanavab == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`تنزيل ملف pdf الخاص بك ..` ⏳"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`اكتمل التنزيل ...`"
            )
            
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`1 تحقق من عدد الصفحات` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            
            splitOutput = PdfFileWriter()
            
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            
            file_path = f"{callbackQuery.message.message_id}/ملف المقسم.pdf"
            
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/ملف المقسم.pdf",
                caption = f"من `{pageStartAndEnd[0]}` الى `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.edit(
                "`اكتمل التحميل ..`🤞"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("SplitR: ",e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitS)
async def _splitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل ..🙇"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        newList = []
        nabilanavab = True; i = 0
        while(nabilanavab):
            
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = "__Pdf تقسيم » حسب الصفحات\nالآن ، أدخل أرقام الصفحات مفصولة بعلامة _ (,) :\n\n/exit __للإلغاء__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            singlePages = list(needPages.text.replace(',',':').split(':'))
            
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                break
            
            elif 1 <= len(singlePages) <= 100:
                try:
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList != []:
                        nabilanavab = False
                        break
                    elif newList == []:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`لايمكن إيجاد أي رقم ..`😏"
                        )
                        continue
                except Exception:
                    pass
            
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`هناك خطأ ما..`😅"
                )
        
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if nabilanavab == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`قم بتنزيل ملف pdf ..`⏳"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`اكتمل التنزيل ...`"
            )
            
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            
            splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = splitInputPdf.getNumPages()
            splitOutput = PdfFileWriter()
            
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            
            with open(
                f"{callbackQuery.message.message_id}/ملف المقسم.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/ملف المقسم.pdf",
                caption = f"الصفحات : `{newList}`"
            )
            
            await downloadMessage.edit(
                "`اكتمل التحميل ..🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("splitS ;", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with known pdf page number)
@ILovePDF.on_callback_query(KsplitR)
async def _KsplitR(bot, callbackQuery):
    try:
        
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل ..🙇"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        _, number_of_pages = callbackQuery.data.split("|")
        number_of_pages = int(number_of_pages)
        
        nabilanavab = True; i = 0
        while(nabilanavab):
            
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = f"__Pdf تقسيم » حسب\nالآن ، أدخل النطاق (البداية: النهاية):\nإجمالي الصفحات : __`{number_of_pages}` 🌟\n\n/exit __للإلغاء__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                break
            
            pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`خطأ في بناء الجملة: تحتاج فقط إلى البداية والنهاية `🚶"
                )
            
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                
                if start.isdigit() and end.isdigit():
                    
                    if (int(1) <= int(start) and int(start) < number_of_pages):
                        
                        if (int(start) < int(end) and int(end) <= number_of_pages):
                            nabilanavab = False
                            break
                        
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`خطأ في بناء الجملة: خطأ في إنهاء رقم الصفحة `🚶"
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`خطأ في بناء الجملة: خطأ في بدء رقم الصفحة `🚶"
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`خطأ في بناء الجملة: يجب أن يكون رقم الصفحة رقمًا` 🧠"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`خطأ في بناء الجملة: لا يوجد رقم صفحة منتهية أو ليس رقمًا` 🚶"
                )
        
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if nabilanavab == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`قم بتنزيل ملف pdf ..` ⏳"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`اكتمل التنزيل ...🤞`"
            )
            
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`1 تحقق من عدد الصفحات` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            
            splitOutput = PdfFileWriter()
            
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            
            file_path = f"{callbackQuery.message.message_id}/ملف المقسم.pdf"
            
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/ملف المقسم.pdf",
                caption = f"من `{pageStartAndEnd[0]}` الى `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.edit(
                "`اكتمل التحميل ..🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("KsplitR :", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(KsplitS)
async def _KsplitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل ..🙇"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        _, number_of_pages = callbackQuery.data.split("|")
        
        newList = []
        nabilanavab = True; i = 0
        while(nabilanavab):
            
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = f"__Pdf تقسيم »  \nأدخل أرقام الصفحات مفصولة بعلامة _(,) :\n__إجمالي الصفحات : __`{number_of_pages}` 🌟\n\n/exit __لالغاء__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            singlePages = list(needPages.text.replace(',',':').split(':'))
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                break
            
            elif 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                try:
                    for i in singlePages:
                        if (i.isdigit() and int(i) <= int(number_of_pages)):
                            newList.append(i)
                    if newList == []:
                        await bot.send_message(
                             callbackQuery.message.chat.id,
                            f"`أدخل أرقامًا أقل من {number_of_pages}..`😏"
                        )
                        continue
                    else:
                        nabilanavab = False
                        break
                except Exception:
                    pass
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`هناك خطأ ما..`😅"
                )
        
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if nabilanavab == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`قم بتنزيل ملف pdf ..`⏳"
            )
            
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`اكتمل التنزيل ...`"
            )
            
            splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = splitInputPdf.getNumPages()
            splitOutput = PdfFileWriter()
            
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            
            with open(
                f"{callbackQuery.message.message_id}/ملف المقسم.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/ملف المقسم.pdf",
                caption = f"الصفحات : `{newList}`"
            )
            
            await downloadMessage.edit(
                "`اكتمل التحميل ..🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("Ksplits: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass
