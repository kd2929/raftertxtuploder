import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import time
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import sys
import re
from pyrogram import Client as bot
import time
from typing import List, Dict

@bot.on_message(filters.command(["appx3"]))
async def account_login(bot: Client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Rojgar", callback_data="a1"),
                InlineKeyboardButton("Last Exam", callback_data="a2"),
                InlineKeyboardButton("Mission Institute", callback_data="a3")
            ]
        ]
    )    
    sent_message = await message.reply_photo(
        photo="https://telegra.ph/file/0eca3245df8a40c7e68d4.jpg",
        caption="Choose an option:",
        reply_markup=keyboard
    )

@bot.on_callback_query()
async def callback_handler(client, callback_query): 
    chosen_option = callback_query.data
    if chosen_option in ["a1", "a2", "a3"]:
        Ins = {
            "a1": "rozgarapinew.teachx.in",
            "a2": "lastexamapi.teachx.in",
            "a3": "missionapi.appx.co.in"
        }[chosen_option]
        rwa_url = "https://" + Ins + "/post/login"
        await callback_query.message.reply_text(f"You selected {chosen_option}!")
        await callback_query.message.reply_text(f"URL for login: {rwa_url}")

        # Here you should define and call process_login if needed

        editable = await callback_query.message.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
        hdr = {"Client-Service": "Appx",
               "Auth-Key": "appxapi",
               "User-ID": "-2",
               "Authorization": "",
               "User_app_category": "",
               "Language": "en",
               "Content-Type": "application/x-www-form-urlencoded",
               "Content-Length": "236",
               "Accept-Encoding": "gzip, deflate",
               "User-Agent": "okhttp/4.9.1"
               }
        info = {"email": "", "password": ""}
        input1: Message = await bot.listen(editable.chat.id)
        raw_text = input1.text
        info["email"] = raw_text.split("*")[0]
        info["password"] = raw_text.split("*")[1]
        await input1.delete(True)
        res = requests.post(rwa_url, data=info, headers=hdr).content
        output = json.loads(res)
        userid = output["data"]["userid"]
        token = output["data"]["token"]
    else:
        await callback_query.answer("Invalid option selected.", show_alert=True)

    hdr1 = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-ID": userid,
        "Authorization": token,
        "User_app_category": "",
        "Language": "en",
        "Host": Ins,
        "User-Agent": "okhttp/4.9.1"
    }
    await editable.edit("**login Successful**")
    res1 = requests.get(f"https://{Ins}/get/mycourse?userid={userid}", headers=hdr1)
    b_data = res1.json().get('data', [])
    batch_info = "\n".join([f"`{data['id']}` - **{data['course_name']}**" for data in b_data])
    await message.reply_text(f"**Your batches:**\n{batch_info}")
    editable = await message.reply_text("Now send the Batch ID to Download")


    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text.strip()

    res2 = requests.get(f"https://{Ins}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}", headers=hdr1)
    subjID = res2.json().get("data", [])
    await message.reply_text(f"**Subject IDs:**\n{subjID}")

    # Wait for the Subject ID input from the user
    editable1 = await message.reply_text("Enter the Subject ID from the above response")
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text.strip()

    res3 = requests.get(f"https://{Ins}/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={raw_text3}", headers=hdr1)
    b_data2 = res3.json().get("data", [])

    topic_info = "\n".join([f"`{data['topicid']}` - **{data['topic_name']}** ({len(data['topicid'])})" for data in b_data2])
    await message.reply_text(f"**Topic details:**\n{topic_info}")

    editable2 = await message.reply_text("Now send the Topic IDs to Download")

    # Wait for the Topic IDs input from the user
    input4 = await bot.listen(editable2.chat.id)
    raw_text4 = input4.text.strip()
  
    if Ins == "lastexamapi.teachx.in":
        hdr11 = {
            "Host": "lastexamapi.teachx.in",
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
        }
    elif Ins == "missionapi.appx.co.in":
        hdr11 = {
            "Host": "missionapi.appx.co.in",
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
        }
    else:
        hdr11 = {
            "Host": "rozgarapinew.teachx.in",
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
        }

    try:
        topic_ids_list = topic_ids.split('&')
        mm = "Ankit-Wih-Rojgar"
        for topic_id in topic_ids_list:
            res4 = requests.get(f"https://{Ins}/get/livecourseclassbycoursesubtopconceptapiv3?topicid={topic_id}&start=-1&courseid={course_id}&subjectid={subject_id}", headers=hdr11)
            topic_data = res4.json().get("data", [])

            with open(f'{mm}.txt', 'a') as f:
                for data in topic_data:
                    title = data["Title"].replace(" : ", " ").replace(" :- ", " ").replace(" :-", " ").replace(":-", " ").replace("_", " ").replace("(", "").replace(")", "").replace("&", "").strip()
                    if data["download_link"]:
                        b64 = data["download_link"]
                    else:
                        b64 = data["pdf_link"]
                    key = "638udh3829162018".encode("utf8")
                    iv = "fedcba9876543210".encode("utf8")
                    ciphertext = bytearray.fromhex(b64decode(b64.encode()).hex())
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                    b = plaintext.decode('utf-8')
                    cc0 = f"{title}:{b}\n"
                    f.write(cc0)

        await message.reply_document(f"{mm}.txt")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


