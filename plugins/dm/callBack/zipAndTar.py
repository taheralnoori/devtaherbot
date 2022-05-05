# fileName : plugins/dm/callBack/zipAndTar.py
# copyright ©️ 2021 nabilanavab

import os
import time
import fitz                      # PDF IMAGE EXTRACTION
import shutil                    # DLT DIR, DIR TO ZIP
import asyncio                   # asyncronic sleep
from PIL import Image            # COMPRESS LARGE FILES
from pdf import PROCESS          # CHECKS CURRENT PROCESS
from pyromod import listen       # ADD-ON (Q/A)
from pyrogram import filters     # CUSTOM FILTERS FOR CALLBACK
from Configs.dm import Config
from plugins.checkPdf import checkPdf    # CHECK CODEC
from plugins.progress import progress    # DOWNLOAD PROGRESS
from pyrogram.types import ForceReply    # FORCE REPLY
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF    # HUMAN READABLE FILE SIZE
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

cancel=InlineKeyboardMarkup([[InlineKeyboardButton("💤 إلغاء 💤", callback_data="cancelP2I")]])
canceled=InlineKeyboardMarkup([[InlineKeyboardButton("🍄 أكتمل 🍄", callback_data="canceled")]])

#--------------->
#--------> CHECKS IF USER CANCEL PROCESS
#------------------->

async def notInPROCESS(chat_id, message, deleteID):
    if chat_id in PROCESS:
        return False
    else:
        await message.edit(
            text=f"`تم إلغاء العملية ...😏`",
            reply_markup=canceled
        )
        shutil.rmtree(f'{deleteID}')
        doc.close()
        return True

#--------------->
#--------> PDF TO IMAGES
#------------------->

KzipANDtar=["KzipA|", "KzipR|", "KzipS|", "KtarA|", "KtarR|", "KtarS"]
ZIPandTAR=filters.create(lambda _, __, query: query.data in ["zipA", "zipR", "zipS", "tarA", "tarR", "tarS"])
KZIPandTAR=filters.create(lambda _, __, query: query.data.startswith(tuple(KzipANDtar)))

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(ZIPandTAR)
async def _ZIPandTAR(bot, callbackQuery):
    try:
        # CHECK USER PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer("جاري العمل .. 🙇")
            return
        # ADD USER TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # CALLBACK DATA
        data=callbackQuery.data
        # ACCEPTING PAGE NUMBER
        if data in ["zipA", "tarA"]:
            nabilanavab=False
        # RANGE (START:END)
        elif data in ["zipR", "tarR"]:
            nabilanavab=True; i=0
            # 5 EXCEPTION, BREAK MERGE PROCESS
            while(nabilanavab):
                if i >= 5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                    )
                    break
                i+=1
                # PYROMOD ADD-ON (PG NO REQUEST)
                needPages=await bot.ask(
                    text="__Pdf - Zip » صفحات:\nالآن ، أدخل النطاق (البداية: النهاية):__\n\n/exit __لالغاء__",
                    chat_id=callbackQuery.message.chat.id,
                    reply_to_message_id=callbackQuery.message.message_id,
                    filters=filters.text,
                    reply_markup=ForceReply(True)
                )
                # EXIT PROCESS
                if needPages.text=="/exit":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`تم إلغاء العملية ..` 😏"
                    )
                    break
                # SPLIT STRING TO START & END
                pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
                # IF STRING HAVE MORE THAN 2 LIMITS
                if len(pageStartAndEnd) > 2:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`خطأ في بناء الجملة: تحتاج فقط إلى البداية والنهاية`🚶"
                    )
                # CORRECT FORMAT
                elif len(pageStartAndEnd)==2:
                    start=pageStartAndEnd[0]
                    end=pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                                nabilanavab=False
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
                # ERPOR MESSAGE
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`خطأ في بناء الجملة: لا يوجد رقم صفحة منتهية أو ليس رقمًا` 🚶"
                    )
        # SINGLE PAGES
        else:
            newList=[]
            nabilanavab=True; i=0
            # 5 REQUEST LIMIT
            while(nabilanavab):
                if i>=5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                    )
                    break
                i+=1
                # PYROMOD ADD-ON
                needPages=await bot.ask(
                    text="__Pdf - Zip » صفحات:\nالآن ، أدخل أرقام الصفحات مفصولة بـ__ (,) :\n\n/exit __لالغاء__",
                    chat_id=callbackQuery.message.chat.id,
                    reply_to_message_id=callbackQuery.message.message_id,
                    filters=filters.text,
                    reply_markup=ForceReply(True)
                )
                # SPLIT PAGE NUMBERS (,)
                singlePages=list(needPages.text.replace(',',':').split(':'))
                # PROCESS CANCEL
                if needPages.text=="/exit":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`تم إلغاء العملية ..` 😏"
                    )
                    break
                # PAGE NUMBER LESS THAN 100
                elif 1 <= len(singlePages) <= 100:
                    # CHECK IS PAGE NUMBER A DIGIT(IF ADD TO A NEW LIST)
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList!=[]:
                        nabilanavab=False
                        break
                    # AFTER SORTING (IF NO DIGIT PAGES RETURN)
                    elif newList==[]:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`لا يمكن العثور على أي رقم ..`😏"
                        )
                        continue
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`هناك خطأ ما..`😅"
                    )
        if nabilanavab==True:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        if nabilanavab==False:
            # DOWNLOAD MESSAGE
            downloadMessage=await callbackQuery.message.reply_text(text="`قم بتنزيل ملف pdf ..` ⏳", quote=True)
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            # DOWNLOAD PROGRESS
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize, downloadMessage, c_time
                )
            )
            # CHECK DOWNLOAD COMPLETED/CANCELED
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            # CHECK PDF CODEC, ENCRYPTION..
            checked=await checkPdf(
                f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery
            )
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
            await downloadMessage.edit("`ملف مضغوط ..` 😅")
            # OPEN PDF WITH FITZ
            doc=fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages=doc.pageCount
            if data in ["zipA", "tarA"]:
                if number_of_pages > 50:
                    await downloadMessage.edit("__بسبب بعض القيود ، يرسل البوت 50 صفحة فقط على هيئة ZIP ..__😅")
                    await asyncio.sleep(5)
                    pageStartAndEnd=[1, 50]
                else:
                    pageStartAndEnd=[1, int(number_of_pages)]
            if data in ["zipR", "tarR"]:
                if int(pageStartAndEnd[1])-int(pageStartAndEnd[0])>50:
                    await downloadMessage.edit("__بسبب بعض القيود ، يرسل البوت 50 صفحة فقط على هيئة ZIP ..__😅")
                    await asyncio.sleep(5)
                    pageStartAndEnd=[int(pageStartAndEnd[0]), int(pageStartAndEnd[0])+50]
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await downloadMessage.edit(
                        f"`فقط pdf {number_of_pages} صفحات` 💩"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
            zoom=2
            mat=fitz.Matrix(zoom, zoom)
            if data in ["zipA", "zipR", "tarA", "tarR"]:
                await downloadMessage.edit(
                    text=f"`اجمالي صفحات: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}..⏳`",
                    reply_markup=cancel
                )
                totalPgList=range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
            if data in ["zipS", "tarS"]:
                totalPgList=[]
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await downloadMessage.edit(
                        text=f"`فقط PDF  {number_of_pages} صفحات `😏"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f'{callbackQuery.message.message_id}')
                    doc.close()
                    return
                await downloadMessage.edit(
                    text=f"`صفحات: {len(totalPgList)}..⏳`",
                    reply_markup=cancel
                )
            cnvrtpg=0
            os.mkdir(f'{callbackQuery.message.message_id}/pgs')
            for i in totalPgList:
                page=doc.load_page(int(i)-1)
                pix=page.get_pixmap(matrix=mat)
                cnvrtpg+=1
                if cnvrtpg%5==0:
                    await downloadMessage.edit(
                        text=f"`تم تحويلة: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} صفحات.. 🤞`",
                        reply_markup=cancel
                    )
                    if await notInPROCESS(callbackQuery.message.chat.id, downloadMessage, callbackQuery.message.message_id):
                        return
                with open(
                    f'{callbackQuery.message.message_id}/pgs/{i}.jpg','wb'
                ):
                    pix.save(f'{callbackQuery.message.message_id}/pgs/{i}.jpg')
            directory=f'{callbackQuery.message.message_id}/pgs'
            imag=[os.path.join(directory, file) for file in os.listdir(directory)]
            imag.sort(key=os.path.getctime)
            for file in imag:
                qualityRate=95
                for i in range(200):
                    if os.path.getsize(file)>=1000000:
                        picture=Image.open(file)
                        picture.save(
                            file, "JPEG",
                            optimize=True,
                            quality=qualityRate
                        )
                        qualityRate-=5
                    else:
                        break
            output_file=f'{callbackQuery.message.message_id}/zipORtar'
            if data in ["zipA", "zipR", "zipS"]:
                shutil.make_archive(output_file, 'zip', directory)
            if data in ["tarA", "tarR", "tarS"]:
                path=shutil.make_archive(output_file, 'tar', directory)
            await downloadMessage.edit("`بدأ التحميل ..` 🏋️")
            await bot.send_chat_action(
                callbackQuery.message.chat.id, "upload_document"
            )
            # Getting File Name
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
            await callbackQuery.message.reply_document(
                file_name=f"{fileNm}.zip" if data.startswith("zip") else f"{fileNm}.tar", quote=True,
                document=open(f"{output_file}.zip" if data.startswith("zip") else f"{output_file}.tar", "rb"),
                thumb=PDF_THUMBNAIL, caption="__ملف المضغوط بصيغة Zip __" if data.startswith("zip") else "__ الملف المضغوط بصيغة Tar__"
            )
            PROCESS.remove(callbackQuery.message.chat.id)
            doc.close()
            await downloadMessage.delete()
            shutil.rmtree(f'{callbackQuery.message.message_id}')
    except Exception as e:
        try:
            print("zipANDtar: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.message_id}')
        except Exception:
            pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KZIPandTAR)
async def _KZIPandTAR(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer("جاري العمل .. 🙇")
            return
        data=callbackQuery.data[:5]
        _, number_of_pages=callbackQuery.data.split("|")
        PROCESS.append(callbackQuery.message.chat.id)
        if data in ["KzipA", "KtarA"]:
            nabilanavab = False
        elif data in ["KzipR", "KtarR"]:
            nabilanavab=True; i=0
            while(nabilanavab):
                if i >= 5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                    )
                    break
                i+=1
                needPages=await bot.ask(
                    text="__Pdf - Zip » صفحات:\nالآن ، أدخل النطاق (البداية: النهاية):__\n\n/exit __لالغاء__",
                    chat_id=callbackQuery.message.chat.id,
                    reply_to_message_id=callbackQuery.message.message_id,
                    filters=filters.text,
                    reply_markup=ForceReply(True)
                )
                if needPages.text=="/exit":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`تم إلغاء العملية ..` 😏"
                    )
                    break
                pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd) > 2:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`خطأ في بناء الجملة: تحتاج فقط إلى البداية والنهاية`🚶"
                    )
                elif len(pageStartAndEnd)==2:
                    start=pageStartAndEnd[0]
                    end=pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if int(pageStartAndEnd[0]) < int(pageStartAndEnd[1]) and int(pageStartAndEnd[1]) <= int(number_of_pages):
                                nabilanavab=False
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
        elif data in ["KzipS", "KtarS"]:
            newList=[]
            nabilanavab=True; i=0
            while(nabilanavab):
                if i >= 5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 محاولة أكثر .. تم إلغاء العملية ..`😏"
                    )
                    break
                i+=1
                needPages=await bot.ask(
                    text="__Pdf - Img›Doc » صفحات:\nالآن ، أدخل أرقام الصفحات مفصولة بـ__ (,) :\n\n/exit __لالغاء__",
                    chat_id=callbackQuery.message.chat.id,
                    reply_to_message_id=callbackQuery.message.message_id,
                    filters=filters.text,
                    reply_markup=ForceReply(True)
                )
                singlePages=list(needPages.text.replace(',',':').split(':'))
                if needPages.text=="/exit":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`تم إلغاء العملية ..` 😏"
                    )
                    break
                elif 1 <= len(singlePages) <= 100:
                    for i in singlePages:
                        if i.isdigit() and int(i) <= int(number_of_pages):
                            newList.append(i)
                    if newList!=[]:
                        nabilanavab=False
                        break
                    elif newList==[]:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`لا يمكن العثور على أي رقم ..`😏"
                        )
                        continue
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`100 صفحة كافية ..`😅"
                    )
        if nabilanavab==True:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        if nabilanavab==False:
            downloadMessage=await callbackQuery.message.reply_text(
                text="`قم بتنزيل ملف pdf ..` ⏳", quote=True
            )
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            # DOWNLOAD PROGRESS
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize, downloadMessage, c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            await downloadMessage.edit("`ملف مضغوط ..` 😅")
            doc=fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages=doc.pageCount
            if data in ["KzipA", "KtarA"]:
                if number_of_pages > 50:
                    await downloadMessage.edit("__بسبب بعض القيود ، يرسل البوت 50 صفحة فقط على هيئة ZIP ..__😅")
                    await asyncio.sleep(5)
                    pageStartAndEnd=[1, 50]
                else:
                    pageStartAndEnd=[1, int(number_of_pages)]
            if data in ["KzipR", "KtarR"]:
                if int(pageStartAndEnd[1])-int(pageStartAndEnd[0])>50:
                    await downloadMessage.edit("__بسبب بعض القيود ، يرسل البوت 50 صفحة فقط على هيئة ZIP ..__😅")
                    await asyncio.sleep(5)
                    pageStartAndEnd=[int(pageStartAndEnd[0]), int(pageStartAndEnd[0])+50]
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await downloadMessage.edit(
                        text=f"`فقط PDF  {number_of_pages} صفحات` 💩"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
            zoom=2
            mat=fitz.Matrix(zoom, zoom)
            if data in ["KzipA", "KzipR", "KtarA", "KtarR"]:
                await downloadMessage.edit(
                    text=f"`اجمالي صفحات: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}..⏳`",
                    reply_markup=cancel
                )
                totalPgList=range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
            if data in ["KzipS", "KtarS"]:
                totalPgList=[]
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await downloadMessage.edit(
                        text=f"`فقط PDF   {number_of_pages} صفحات `😏"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f'{callbackQuery.message.message_id}')
                    doc.close()
                    return
                await downloadMessage.edit(
                    text=f"`صفحات: {len(totalPgList)}..⏳`",
                    reply_markup=cancel
                )
            cnvrtpg=0
            os.mkdir(f'{callbackQuery.message.message_id}/pgs')
            for i in totalPgList:
                page=doc.load_page(int(i)-1)
                pix=page.get_pixmap(matrix=mat)
                cnvrtpg+=1
                if cnvrtpg%5==0:
                    await downloadMessage.edit(
                        text=f"`تم تحويلة : {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} صفحات.. 🤞`",
                        reply_markup=cancel
                    )
                    if await notInPROCESS(callbackQuery.message.chat.id, downloadMessage, callbackQuery.message.message_id):
                        return
                with open(
                    f'{callbackQuery.message.message_id}/pgs/{i}.jpg','wb'
                ):
                    pix.save(f'{callbackQuery.message.message_id}/pgs/{i}.jpg')
            directory=f'{callbackQuery.message.message_id}/pgs'
            imag=[os.path.join(directory, file) for file in os.listdir(directory)]
            imag.sort(key=os.path.getctime)
            for file in imag:
                qualityRate=95
                for i in range(200):
                    if os.path.getsize(file)>=1000000:
                        picture=Image.open(file)
                        picture.save(
                            file, "JPEG",
                            optimize=True,
                            quality=qualityRate
                        )
                        qualityRate-=5
                    else:
                        break
            output_file=f'{callbackQuery.message.message_id}/zipORtar'
            if data in ["KzipA", "KzipR", "KzipS"]:
                shutil.make_archive(output_file, 'zip', directory)
            if data in ["KtarA", "KtarR", "KtarS"]:
                shutil.make_archive(output_file, 'tar', directory)
            await downloadMessage.edit("`بدأ التحميل ..` 🏋️")
            await bot.send_chat_action(
                callbackQuery.message.chat.id, "upload_document"
            )
            # Getting File Name
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
            await callbackQuery.message.reply_document(
                file_name=f"{fileNm}.zip" if data.startswith("Kzip") else f"{fileNm}.tar", quote=True,
                document=open(f"{output_file}.zip" if data.startswith("Kzip") else f"{output_file}.tar", "rb"),
                thumb=PDF_THUMBNAIL, caption="__ملف مضغوط Zip__" if data.startswith("Kzip") else "__ملف مضغوط Tar __"
            )
            PROCESS.remove(callbackQuery.message.chat.id)
            doc.close()
            await downloadMessage.delete()
            shutil.rmtree(f'{callbackQuery.message.message_id}')
    except Exception as e:
        try:
            print("zipANDtar: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.message_id}')
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
