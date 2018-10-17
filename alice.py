#!/usr/bin/env python3
import asyncio
from datetime import timedelta
from time import time, sleep
from contextlib import suppress

import mtranslate
from telethon import TelegramClient, events
from telethon.tl.types import SendMessageTypingAction
from telethon.tl.types import SendMessageRecordRoundAction

from telethon.tl.functions.messages import SetTypingRequest
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import DocumentAttributeVideo
import telethon.sync
import io
import secret
import re

supported_langs = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq',
                   'Italian': 'it', 'Arabic': 'ar', 'Japanese': 'ja',
                   'Azerbaijani': 'az', 'Kannada': 'kn', 'Basque': 'eu',
                   'Korean': 'ko', 'Bengali': 'bn', 'Latin': 'la',
                   'Belarusian': 'be', 'Latvian': 'lv', 'Bulgarian': 'bg',
                   'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk',
                   'Chinese Simplified': 'zh-CN', 'Malay': 'ms',
                   'Chinese Traditional': 'zh-TW', 'Maltese': 'mt',
                   'Croatian': 'hr', 'Norwegian': 'no', 'Czech': 'cs',
                   'Persian': 'fa', 'Danish': 'da', 'Polish': 'pl',
                   'Dutch': 'nl', 'Portuguese': 'pt', 'English': 'en',
                   'Romanian': 'ro', 'Esperanto': 'eo', 'Russian': 'ru',
                   'Estonian': 'et', 'Serbian': 'sr', 'Filipino': 'tl',
                   'Slovak': 'sk', 'Finnish': 'fi', 'Slovenian': 'sl',
                   'French': 'fr', 'Spanish': 'es', 'Galician': 'gl',
                   'Swahili': 'sw', 'Georgian': 'ka', 'Swedish': 'sv',
                   'German': 'de', 'Tamil': 'ta', 'Greek': 'el',
                   'Telugu': 'te', 'Gujarati': 'gu', 'Thai': 'th',
                   'Haitian Creole': 'ht', 'Turkish': 'tr', 'Hebrew': 'iw',
                   'Ukrainian': 'uk', 'Hindi': 'hi', 'Urdu': 'ur',
                   'Hungarian': 'hu', 'Vietnamese': 'vi', 'Icelandic': 'is',
                   'Welsh': 'cy', 'Indonesian': 'id', 'Yiddish': 'yi'}
client = TelegramClient(
    'alice_redqueen',
    secret.api_id,
    secret.api_hash
).start()
last_msg = None
break_date = None
last_reply_date = None
please_text_list = ['Пожалуйста😊', 'да не за что)', 'пожалуйста))', '😊']
hello_text_list = ['ПриФФки😊', 'приветик)', 'приветики)', 'здравствуй😊', '😊', '😘']
die_note_id = 'AAQCABMmdPQOAATjfnf6CUJoaTOtAAIC'
current_please_num = 0
current_hello_num = 0
async def send_python_zen(event):
    with io.open('zen.txt','r',encoding='utf-8') as zen_fp:
        text = ''.join(zen_fp.readlines())
        await asyncio.sleep(0.5)
        await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
        await asyncio.sleep(2.5)
        await event.reply(text,parse_mode='Markdown')
    return
async def send_video_note(event):
    thumbnail_path = 'thumb.jpg'
    filename = 'vnote2.mp4'
    await asyncio.sleep(0.5)
    await client(SetTypingRequest(event.input_chat, SendMessageRecordRoundAction()))
    document_attribute = [DocumentAttributeVideo(duration=3, w=260, h=260, round_message=True,
                                                 supports_streaming=True),
                          DocumentAttributeFilename(filename)]
    await asyncio.sleep(2.5)
    await client.send_file(event.input_chat, filename, caption='Вы все здесь умрете',
                     file_name=str(filename), allow_cache=True, part_size_kb=512,
                     thumb=str(thumbnail_path), attributes=document_attribute)
    return
@client.on(events.NewMessage(incoming=True))
async def break_updater(event):
    global break_date
    global last_msg
    global last_reply_date
    global current_please_num
    global please_text_list
    global hello_text_list
    global current_hello_num
    ad_text = '@AudioTubeBot @VideoTubeBot'
    with suppress(Exception):
        text = event.text
        res = re.search('(youtube)|(ютуб)|(с вк)', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            res = re.search('(кач)|(груз)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                res = re.search('бот', text, flags=re.UNICODE | re.IGNORECASE)
                if res:
                    res = re.search('\?', text, flags=re.UNICODE | re.IGNORECASE)
                    if res:
                        res = re.search('(вид)', text, flags=re.UNICODE | re.IGNORECASE)
                        if res:
                            ad_text = '@VideoTubeBot'
                        else:
                            res = re.search('(муз)|(ауд)|(звук)', text, flags=re.UNICODE | re.IGNORECASE)
                            if res:
                                ad_text = '@AudioTubeBot'
                        last_reply_date = event.date if not last_reply_date else last_reply_date
                        if event.date - last_reply_date > timedelta(seconds=1 * 60):
                            await asyncio.sleep(0.5)
                            await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                            await asyncio.sleep(3)
                            last_reply_date = event.date
                            await event.reply(ad_text)
                            print(text)
                        return
        res = re.search('(гиф)|(gif)|(круг)', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            res = re.search('(вид)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                last_reply_date = event.date if not last_reply_date else last_reply_date
                if event.date - last_reply_date > timedelta(seconds=1 * 30):
                    ad_text = '@VideoTubeBot'
                    await asyncio.sleep(0.5)
                    await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                    await asyncio.sleep(3)
                    last_reply_date = event.date
                    await event.reply(ad_text)
                return
        res = re.search('Что скажешь, Алиса\?', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await send_video_note(event)
            return
        res = re.search('Алиса, твой выход', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await send_video_note(event)
            return
        res = re.search('Алиса, что думаешь по этому поводу\?', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await send_video_note(event)
            return
        res = re.search('^Алиса,(.*)?дзен(.*)?((python)|(питон))(.*)?', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await send_python_zen(event)
            return
        res = re.search('^Алиса, покажи им - что такое настоящий гимн', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await send_python_zen(event)
            return
        res = re.search('^Алиса, как пропатчить KDE2 под FreeBSD\?', text, flags=re.UNICODE | re.IGNORECASE)
        if res:
            await asyncio.sleep(0.5)
            await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
            await asyncio.sleep(2.5)
            await event.reply('Это может сделать только хокагэ. Но тебе им никогда не стать - не хватит фурёку')
            return
        if event.mentioned:
            res = re.search('(пасиб)|(спс)|(благодарю)|(атдуши)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await asyncio.sleep(0.5)
                await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                await asyncio.sleep(2.5)
                await event.reply(please_text_list[current_please_num])
                current_please_num = (current_please_num + 1) % len(please_text_list)
                return
            res = re.search('(прив)|(хай)|(здаров)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await asyncio.sleep(0.5)
                await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                await asyncio.sleep(2.5)
                await event.reply(hello_text_list[current_hello_num])
                current_hello_num = (current_hello_num + 1) % len(hello_text_list)
                return
            res = re.search('(погнали)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await asyncio.sleep(0.5)
                await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                await asyncio.sleep(2.5)
                await event.reply('ну погнали')
                return
            res = re.search('(кто)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await asyncio.sleep(0.5)
                await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                await asyncio.sleep(2.5)
                await event.reply('Я - Алиса')
                return
            res = re.search('(ты бот)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await send_video_note(event)
            res = re.search('(делаешь)|(занимаешься)', text, flags=re.UNICODE | re.IGNORECASE)
            if res:
                await asyncio.sleep(0.5)
                await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
                await asyncio.sleep(2.5)
                await event.reply('Славику помогаю')
                return
    if last_msg:
        try:
            if (event.message.to_id.user_id == last_msg.from_id and
                    last_msg.to_id.user_id == event.message.sender_id):
                break_date = event.date
        except Exception:
            if event.to_id == last_msg.to_id:
                break_date = event.date


client.run_until_disconnected()
