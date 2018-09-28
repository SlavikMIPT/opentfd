#!/usr/bin/env python3
import asyncio
from datetime import timedelta
from time import time
from contextlib import suppress

import mtranslate
from telethon import TelegramClient, events

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
    'opentfd_session',
    secret.api_id,
    secret.api_hash
).start()
last_msg = None
break_date = None

async def run_command_shell(cmd, e):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    msg_text = ''
    msg_text_old = ''
    lines_count = 0
    lines_max = 10
    last_update_time = 0
    start_time = time()
    msg_lines = []
    while time() - start_time <= 30:
        data = await process.stdout.readline()
        line = data.decode("ascii").strip()
        msg_lines.append(line)
        if line == '' and not await process.communicate():
            break
        print(line)
        msg_lines = msg_lines[-lines_max:]
        # if lines_count <= 10:
        msg_text = ''
        for ln in msg_lines:
            msg_text += f'${ln}\n'
        current_time = time()
        if current_time - last_update_time >= 1:
            last_update_time = current_time
            with suppress(Exception):
                if not msg_text_old == msg_text:
                    await e.edit(msg_text)
                    msg_text_old = msg_text
                    # await e.edit(msg_text)
                # last_update_time = time()
    msg_text += '$-----TERMINATED-----\n'
    await e.edit(msg_text)
    return await process.kill()
    # results = await process.communicate()
    # return ''.join(x.decode() for x in results)


@client.on(events.Raw())
async def translator(event):
    drafts = await client.get_drafts()
    for draft in drafts:
        if draft.is_empty:
            continue
        text = str(draft.text)
        for lang_code in supported_langs.values():
            if text.endswith('/{0}'.format(lang_code)):
                translated = mtranslate.translate(text[:-(len(lang_code) + 1)], lang_code, 'auto')
                await draft.set_message(text=translated)
        # print(draft.text)


@client.on(events.NewMessage(incoming=True))
async def break_updater(event):
    global break_date
    global last_msg
    if last_msg:
        try:
            if (event.message.to_id.user_id == last_msg.from_id and
                    last_msg.to_id.user_id == event.message.sender_id):
                break_date = event.date
        except Exception:
            if event.to_id == last_msg.to_id:
                break_date = event.date


@client.on(events.NewMessage(pattern=r'^!bash (.+)', outgoing=True))
async def bash(e):
    cmd = e.pattern_match.group(1)
    print(cmd)
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(run_command_shell(cmd, e), timeout=60.0)
    except asyncio.TimeoutError:
        print('timeout!')


@client.on(events.NewMessage(outgoing=True))
async def merger(event):
    global last_msg
    global break_date
    with suppress(Exception):
        if event.text:
            if event.text.startswith('!bash'):
                return
        if (event.media or event.fwd_from or event.via_bot_id or
                event.reply_to_msg_id or event.reply_markup):
            last_msg = None
        elif last_msg is None:
            last_msg = event
        elif last_msg.to_id == event.to_id:
            if break_date:
                if break_date < event.date:
                    last_msg = event
                    break_date = 0
            elif event.date - last_msg.date < timedelta(seconds=30):
                last_msg = await last_msg.edit(
                    '{0}\n{1}'.format(last_msg.text, event.text))
                last_msg.date = event.date
                await event.delete()
            else:
                last_msg = event
        else:
            last_msg = event


client.run_until_disconnected()
