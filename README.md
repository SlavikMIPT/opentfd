# OpenTFD
* Merges series of Telegram messages if there is a pause of less than 30 seconds between them
* Integrated Google Translator (just put /en in the end of message to translate into English or /ru to translate into russian). Full list of supported languages you can see in supported_langs at opentfd.py
* Bash assistant - type '!bash command' in any chat to execute command on your host

Compiled versions is on [releases of this repo](https://github.com/SlavikMIPT/opentfd/releases/tag/latest)

### Scripts
* opentfd.service - template of linux systemd service for 24/7 execution on VDS

### For non-compiled versions
1. `pip3 install reqirements.txt`
2. Add [API token and hash](https://core.telegram.org/api/obtaining_api_id) to secret.template.py and rename it to secret.py
3. `python3 opentfd.py`

### Dependencies
* Latest version of Telethon: http://telethon.readthedocs.io/en/stable/
* Translator: https://github.com/mouuff/mtranslate.git

Follow author and contributors at Telegram:
* https://t.me/MediaTube_stream
* https://t.me/nastalo
