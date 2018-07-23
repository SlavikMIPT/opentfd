import subprocess
from datetime import timedelta

import socks
from telethon import TelegramClient
from telethon import events

import secret

client = TelegramClient('opentfd_session', secret.api_id, secret.api_hash).start()
last_msg = None
break_date = None


@client.on(events.NewMessage(incoming=True))
async def inc_handler(event):
    global break_date
    global last_msg
    if last_msg:
        try:
            if event.message.to_id.user_id == last_msg.from_id and last_msg.to_id.user_id == event.message.sender_id:
                break_date = event.date
        except Exception:
            if event.to_id == last_msg.to_id:
                break_date = event.date


@client.on(events.NewMessage(outgoing=True))
async def out_handler(event):
    global last_msg
    global break_date
    try:
        if event.media or event.fwd_from or event.via_bot_id or event.reply_to_msg_id or event.reply_markup:
            last_msg = None
        elif last_msg is None:
            last_msg = event
        elif last_msg.to_id == event.to_id:
            if break_date:
                if break_date < event.date:
                    last_msg = event
                    break_date = 0
            elif event.date - last_msg.date < timedelta(seconds=30):
                last_msg = await last_msg.edit('{0}\n{1}'.format(last_msg.text, event.text))
                last_msg.date = event.date
                await event.delete()
            else:
                last_msg = event
        else:
            last_msg = event
    except Exception:
        pass


client.run_until_disconnected()