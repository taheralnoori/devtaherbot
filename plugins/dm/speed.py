# © BugHunterCodeLabs ™
# © bughunter0 / nuhman_pk
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import speedtest   
import logging
import pyrogram
import math
from fpdf import FPDF
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

@ILovePDF.on_message(filters.private & filters.command(["speedtext"]) & ~filters.edited)
async def download_upload(bot, message):
     alert = await message.reply_text("Processing....")
     speed = speedtest.Speedtest() 
     await alert.edit("Getting Best server")
     speed.get_best_server()
     await alert.edit(f'**Connected to :** {speed.results.server["sponsor"]} ({speed.results.server["name"]})')
     message = await message.reply_text("Checking Download / Upload Speed ...")
     downloadspeed = speed.download()
     downloadspeed = downloadspeed/1000000 # bit to kbps
     uploadspeed = speed.upload()
     uploadspeed = uploadspeed/1000000 # bit to kbps
     await alert.delete()
     await message.edit_text(f' **Download Speed :** `{downloadspeed} kbps` \n**Upload Speed :** `{uploadspeed} kbps` \n**Server :** {speed.results.server["sponsor"]} ({speed.results.server["name"]})\n \n © @BugHunterBots')

