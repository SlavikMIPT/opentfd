import asyncio
from datetime import datetime, timedelta
from time import time, sleep
from contextlib import suppress

import mtranslate
from telethon import TelegramClient, events, sync, errors, custom
from telethon.tl.types import UpdateDraftMessage
from telethon.tl.types import SendMessageRecordRoundAction, SendMessageUploadRoundAction, SendMessageTypingAction
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import pack_bot_file_id
from telethon.tl.functions.messages import SetTypingRequest
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import DocumentAttributeVideo
from proxy import mediatube_proxy
from supported_langs import supported_langs
import secret
import getopt
import sys
import os
import io
import animation

default_proxy = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'p', ['proxy'])
    for opt, arg in opts:
        if opt in ('-p', '--proxy'):
            default_proxy = mediatube_proxy
except getopt.GetoptError:
    sys.exit(2)
VIDEOTUBEBOT_ID = 599312585
client = TelegramClient('opentfd_session', secret.api_id, secret.api_hash, proxy=default_proxy).start()
last_msg = None
break_time = None
last_msg_time = time()
MERGE_TIMEOUT = 30
merge_semaphore = asyncio.Semaphore(value=1)
draft_semaphore = asyncio.Semaphore(value=1)


async def send_video_note(event):
    msg = event.message
    try:
        filename = msg.media.document.attributes[1].file_name
    except Exception:
        filename = 'video_noname.mp4'
    chat = await event.get_chat()
    replied_msg_id = None
    if event.reply_to_msg_id:
        replied_msg_id = event.reply_to_msg_id
    await client(SetTypingRequest(chat, SendMessageRecordRoundAction()))
    if not os.path.exists(filename):
        filename = await client.download_media(event.message, file=filename)
    await asyncio.sleep(0.5)
    await event.delete()
    document_attribute = [DocumentAttributeVideo(duration=0, w=260, h=260, round_message=True,
                                                 supports_streaming=True),
                          DocumentAttributeFilename(filename)]
    result = await client.send_file(chat, filename, caption='',
                           file_name=str(filename), allow_cache=True, supports_streaming=True, part_size_kb=512,
                           thumb=None, attributes=document_attribute, reply_to=replied_msg_id)
    return


async def run_command_shell(cmd, e):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    msg_text = f'{cmd}\n'
    msg_text_old = f'{cmd}\n'
    blank_lines_count = 0
    lines_max = 20
    last_update_time = 0
    start_time = time()
    msg_lines = []
    await asyncio.sleep(1)
    while time() - start_time <= 60:
        for _ in range(lines_max):
            data = await process.stdout.readline()
            line = data.decode().strip()
            if blank_lines_count <= 5:
                if line == '':
                    blank_lines_count += 1
                if line != '':
                    blank_lines_count = 0
                    msg_lines.append(line)
            else:
                break
        msg_lines = msg_lines[-lines_max:]
        msg_text = f'{cmd}\n'
        for ln in msg_lines:
            msg_text += f'`${ln}`\n'
        with suppress(Exception):
            if msg_text_old != msg_text:
                await e.edit(msg_text, parse_mode='Markdown')
                msg_text_old = msg_text
        await asyncio.sleep(5)
        if blank_lines_count >= 5:
            break

    msg_text += '$-----TERMINATED-----\n'
    msg_text += 'Open-source [telegram shell](https://github.com/mediatube/opentfd)'
    await e.edit(msg_text)
    return await process.kill()


@client.on(events.NewMessage(pattern=r'^!zen.*', outgoing=True))
async def send_python_zen(event):
    with io.open('zen.txt', 'r', encoding='utf-8') as zen_fp:
        text = ''.join(zen_fp.readlines())
        await asyncio.sleep(0.5)
        await client(SetTypingRequest(event.input_chat, SendMessageTypingAction()))
        await asyncio.sleep(2.5)
        await event.reply(text, parse_mode='Markdown')


@client.on(events.Raw(types=UpdateDraftMessage))
async def translator(event: events.NewMessage.Event):
    global draft_semaphore
    await draft_semaphore.acquire()
    try:
        draft_list = await client.get_drafts()
        for draft in draft_list:
            if draft.is_empty:
                continue
            text = draft.text
            for lang_code in supported_langs.values():
                if text.endswith('/{0}'.format(lang_code)):
                    translated = mtranslate.translate(text[:-(len(lang_code) + 1)], lang_code, 'auto')
                    for _ in range(3):
                        try:
                            await draft.set_message(text=translated)
                            await asyncio.sleep(7)
                            return
                        except Exception as e:
                            print(e)
    except Exception as e:
        print(e)
    finally:
        draft_semaphore.release()


@client.on(events.NewMessage(pattern=r'^!type->.*', outgoing=True))
async def typing_imitate(message: events.NewMessage.Event):
    text, text_out = str(message.raw_text).split('->')[-1], str()
    word = list(text)
    with suppress(Exception):
        for letter in word:
            text_out += letter
            try:
                if word.index(letter) % 2 == 1:
                    await message.edit(f'`{text_out}`|')
                else:
                    await message.edit(f'`{text_out}`')
                await asyncio.sleep(0.2)
            except errors.MessageNotModifiedError:
                continue
    raise events.StopPropagation

@client.on(events.NewMessage(pattern=r'^!scan', outgoing=True))
async def scan_chat(message: events.NewMessage.Event):
    await client.get_participants(await message.get_chat())
    raise events.StopPropagation

@client.on(events.NewMessage(pattern=r'^!kick .*', outgoing=True))
async def kick_users(message: events.NewMessage.Event):
    id_list = str(message.raw_text).split(' ')[1:]
    # await client.get_participants('MediaTube_chat')
    with suppress(Exception):
        chat = await client.get_entity('MediaTube_chat')
        for user_id in id_list:
            # The above is equivalent to
            # rights = ChatBannedRights(
            #     until_date=datetime.now() + timedelta(days=366),
            #     send_media=True,
            #     send_stickers=True,
            #     send_gifs=True,
            #     send_games=True,
            #     send_inline=True,
            #     embed_links=True
            # )
            try:

                user = await client.get_input_entity(int(user_id))
                print(id, chat, user)
                # res = await client(EditBannedRequest(chat, user, rights))
                res = await client(EditBannedRequest(
                    chat, user, ChatBannedRights(
                        until_date=None,
                        view_messages=True
                    )
                ))
                print(res)
            except Exception as e:
                print(e)
            finally:
                await asyncio.sleep(0.5)
    raise events.StopPropagation


@client.on(events.NewMessage(pattern=r'^!an.*', outgoing=True))
async def typing_imitate(message: events.NewMessage.Event):
    with suppress(Exception):
        for _ in range(2):
            for frame in animation.frames:
                text_out = f'`{frame}`'
                try:
                    await message.edit(text_out)
                    await asyncio.sleep(0.5)
                except errors.MessageNotModifiedError:
                    continue
        await asyncio.sleep(5)
        await message.delete()
    raise events.StopPropagation


@client.on(events.NewMessage(incoming=True))
async def break_updater(event: events.NewMessage.Event):
    global break_time
    global last_msg
    with suppress(Exception):
        if event.chat and event.chat.bot:
            return
    if last_msg:
        try:
            if (event.message.to_id.user_id == last_msg.from_id and
                    last_msg.to_id.user_id == event.message.sender_id):
                break_time = time()
        except Exception:
            if event.to_id == last_msg.to_id:
                break_time = time()


@client.on(events.NewMessage(pattern=r'^!bash (.+)', outgoing=True))
async def bash(e: events.NewMessage.Event):
    cmd = e.pattern_match.group(1)
    print(cmd)
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(run_command_shell(cmd, e), timeout=60.0)
    except asyncio.TimeoutError:
        print('timeout!')
    raise events.StopPropagation


@client.on(events.NewMessage(outgoing=True))
async def merger(event: custom.Message):
    global last_msg
    global break_time
    global last_msg_time
    global merge_semaphore

    event_time = time()
    with suppress(Exception):
        if event.text and event.text.startswith('!bash'):
            return
        with suppress(Exception):
            if event.chat and event.chat.bot:
                return
        if (event.media or event.fwd_from or event.via_bot_id or
                event.reply_to_msg_id or event.reply_markup):
            last_msg = None
            if event.media and event.via_bot_id == VIDEOTUBEBOT_ID:
                with suppress(Exception):
                    await asyncio.wait_for(send_video_note(event), timeout=60.0)
        elif last_msg is None:
            last_msg = event
        elif last_msg.to_id == event.to_id:
            if break_time:
                if break_time < event_time:
                    last_msg = event
                    last_msg_time = event_time
                    break_time = 0
            elif event_time - last_msg_time < MERGE_TIMEOUT:
                async with merge_semaphore:
                    last_msg = await last_msg.edit('{0}\n{1}'.format(last_msg.text, event.text))
                    last_msg_time = event_time
                    await event.delete()
            else:
                last_msg = event
                last_msg_time = event_time
        else:
            last_msg = event
            last_msg_time = event_time


final_credits = ["OpenTFD is running", "Do not close this window", "t.me/mediatube_stream",
                 "https://github.com/mediatube/opentfd\n", "Supported languages:", ''
                 ]

print('\n'.join(final_credits))
print('\n'.join([f'{k:<25}/{v}' for k, v in supported_langs.items()]))
try:
    client.run_until_disconnected()
finally:
    client.close()
