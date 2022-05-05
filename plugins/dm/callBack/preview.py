# fileName : plugins/dm/callBack/preview.py
# copyright ©️ 2021 nabilanavab

import os
import fitz
import time
import shutil
from PIL import Image
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from pyrogram.types import InputMediaPhoto

#--------------->
#--------> LOCAL VARIABLES
#------------------->

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

media = {}

#--------------->
#--------> PDF TO IMAGES
#------------------->

preview = filters.create(lambda _, __, query: query.data in ["Kpreview", "preview"])

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(preview)
async def _preview(bot, callbackQuery):
    try:
        # CALLBACK DATA
        data=callbackQuery.data
        # CHECK USER PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل .. 🙇"
            )
            return
        await callbackQuery.answer(
            "يرسل فقط صفحات البداية والوسط والنهاية (إذا وجدت 😅)",
            cache_time=10
        )
        # ADD USER TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # DOWNLOAD MESSAGE
        downloadMessage = await callbackQuery.message.reply_text(
            "`قم بتنزيل ملف pdf ..` ⏳", quote=True
        )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        c_time=time.time()
        downloadLoc = await bot.download_media(
            message=file_id,
            file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
            progress=progress,
            progress_args=(
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECK DOWNLOAD COMPLETED/CANCELLED
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        # CHECK PDF CODEC, ENCRYPTION..
        if data!="Kpreview":
            checked=await checkPdf(
                f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery
            )
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
        # OPEN PDF WITH FITZ
        doc = fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
        number_of_pages = doc.pageCount
        if number_of_pages == 1:
            totalPgList=[1]
            caption="معاينة الصورة:\n__بداية: 1__"
        elif number_of_pages == 2:
            totalPgList = [1, 2]
            caption="معاينة الصورة:\n__بداية: 1__,\n__نهاية: 2__"
        elif number_of_pages == 3:
            totalPgList = [1, 2, 3]
            caption="معاينة الصورة:\n__بداية: 1__,\n__وسط: 2__,\n__نهاية: 3__"
        else:
            totalPgList = [1, number_of_pages//2, number_of_pages]
            caption=f"معاينة الصورة:\n__بداية: 1__,\n__وسط: {number_of_pages//2}__,__\nنهاية: {number_of_pages}__"
        await downloadMessage.edit(
            f"`عدد الصفحات: {len(totalPgList)}..⏳`"
        )
        zoom=2
        mat = fitz.Matrix(zoom, zoom)
        os.mkdir(f'{callbackQuery.message.message_id}/pgs')
        for pageNo in totalPgList:
            page=doc.loadPage(int(pageNo)-1)
            pix=page.getPixmap(matrix = mat)
            # SAVING PREVIEW IMAGE
            with open(
                f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
            ):
                pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
        try:
            await downloadMessage.edit(
                f"`جارٍ تحضير ألبوم ..` 🤹"
            )
        except Exception:
            pass
        directory=f'{callbackQuery.message.message_id}/pgs'
        # RELATIVE PATH TO ABS. PATH
        imag=[os.path.join(directory, file) for file in os.listdir(directory)]
        # SORT FILES BY MODIFIED TIME
        imag.sort(key=os.path.getctime)
        # LIST TO SAVE GROUP IMAGE OBJ.
        media[callbackQuery.message.chat.id] = []
        for file in imag:
            # COMPRESSION QUALITY
            qualityRate=95
            # JUST AN INFINITE LOOP
            for i in range(200):
                # print("size: ",file, " ",os.path.getsize(file)) LOG MESSAGE
                # FILES WITH 10MB+ SIZE SHOWS AN ERROR FROM TELEGRAM 
                # SO COMPRESS UNTIL IT COMES LESS THAN 10MB.. :(
                if os.path.getsize(file) >= 1000000:
                    picture=Image.open(file)
                    picture.save(
                        file, "JPEG",
                        optimize=True,
                        quality=qualityRate
                    )
                    qualityRate-=5
                # ADDING TO GROUP MEDIA IF POSSIBLE
                else:
                    if len(media[callbackQuery.message.chat.id]) == 1:
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media=file, caption=caption)
                        )
                    else:
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media=file)
                        )
                    break
        await downloadMessage.edit(
            f"`جارٍ الرفع: معاينة الصفحات .. 🐬`"
        )
        await callbackQuery.message.reply_chat_action("upload_photo")
        await bot.send_media_group(
            chat_id=callbackQuery.message.chat.id,
            reply_to_message_id=callbackQuery.message.reply_to_message.message_id,
            media=media[callbackQuery.message.chat.id]
        )
        await downloadMessage.delete()
        doc.close
        del media[callbackQuery.message.chat.id]
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f'{callbackQuery.message.message_id}')
    
    except Exception as e:
        try:
            PROCESS.remove(callbackQuery.message.chat.id)
            await downloadMessage.edit(f"حدث خطأ ما\n\nخطا: {e}")
            shutil.rmtree(f'{callbackQuery.message.message_id}')
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
