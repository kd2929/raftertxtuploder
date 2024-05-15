import urllib
import urllib.parse
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
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
import uuid
import urllib.parse
import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from pyrogram import Client, filters
from pyrogram.types import Message

@bot.on_message(filters.command(["muskan"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    rwa_url = "https://rozgarapinew.teachx.in/post/login"
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
    input1 = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)
    res = requests.post(rwa_url, data=info, headers=hdr).content
    output = json.loads(res)
    userid = output["data"]["userid"]
    token = output["data"]["token"]
    hdr1 = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-ID": userid,
        "Authorization": token,
        "User_app_category": "",
        "Language": "en",
        "Host": "rozgarapinew.teachx.in",
        "User-Agent": "okhttp/4.9.1"
    }
    
    await editable.edit("**login Successful**")
    res1 = requests.get("https://rozgarapinew.teachx.in/get/mycourse?userid="+userid, headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    
    for data in b_data:
        t_name = data['course_name']
        FFF = "**BATCH-ID -      BATCH NAME **"
        aa = f" `{data['id']}`      - **{data['course_name']}**\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await editable.delete(True)
    await input2.delete(True)
    editable2 = await m.reply_text("📥**Please wait keep patientce.** 🧲    `Scraping Url.`")
    time.sleep(2)
    # Before the loop where you process topic data
    b_name = None  # Define b_name with a default value



# Inside the loop where you reply with the document

    # Fetch subject IDs corresponding to the batch ID
    res2 = requests.get("https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid="+raw_text2, headers=hdr1).json()
    subject_data = res2["data"]
    # Extract subject IDs from the response
    subject_ids = [subject["subjectid"] for subject in subject_data]
    await editable2.edit("📥**Please wait keep patientce.** 🧲    `Scraping Url..`")
    time.sleep(2)
    # Fetch topic IDs corresponding to each subject ID
    all_topic_ids = []
    for subject_id in subject_ids:
        res3 = requests.get("https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid="+raw_text2+"&subjectid="+subject_id, headers=hdr1)
        topic_data = res3.json()['data']
        topic_ids = [topic["topicid"] for topic in topic_data]
        all_topic_ids.extend(topic_ids)
    # Inside the loop where you check for batch name
    b_name = next((x['id'] for x in b_data if str(x['course_name']) == raw_text2), None)
    # Now all_topic_ids contains all the topic IDs for the given batch ID

    xv = all_topic_ids  # Use all_topic_ids as the list of topic IDs

    hdr11 = {
        "Host": "rozgarapinew.teachx.in",
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": userid,
        "Authorization": token
    }    
    
    cool2 = ""  # Define cool2 outside the loop to accumulate all URLs
    await editable2.edit("📥**Please wait keep patientce.** 🧲    `Scraping Url...`")
    for t in xv:  # Loop through all topic IDs
        res4 = requests.get("https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&conceptid=1&courseid=" + raw_text2 + "&subjectid=" + subject_id, headers=hdr11).json()
        topicid = res4["data"]
        for data in topicid:
            if data["download_link"]:
                b64 = (data["download_link"])
            else:
                b64 = (data["pdf_link"])
            tid = data["Title"].replace(" : ", " ").replace(" :- ", " ").replace(" :-", " ").replace(":-", " ").replace("_", " ").replace("(", "").replace(")", "").replace("&", "").strip()
            zz = len(tid)
            key = "638udh3829162018".encode("utf8")
            iv = "fedcba9876543210".encode("utf8")
            ciphertext = bytearray.fromhex(b64decode(b64.encode()).hex())
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            b = plaintext.decode('utf-8')
            cc0 = f"{tid}:{b}\n"
            if len(f'{cool2}{cc0}') > 9999:
                cool2 = ""
            cool2 += cc0
    await editable2.edit("Scraping completed successfully!")
    await editable2.delete(True)
    # Outside the loop, write all URLs to a single file and reply with the document
    file_name = b_name if b_name else str(uuid.uuid4())  # Use batch name if available, else generate a random file name
    with open(f'{file_name}.txt', 'w') as f:
        f.write(cool2)
    await m.reply_document(f"{file_name}.txt")
    
