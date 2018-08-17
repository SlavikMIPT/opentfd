# OpenTFD
* Merges serial Telegram messages, if between them a pause of less than 30 seconds
* Integrated Google translator (just put /en in end of message to translate to english or /ru to translate to russian). Full list of supported languages you can see in supported_langs at opentfd.py

You can find compiled versions on [releases](https://github.com/kotwizkiy/opentfd/releases)

### Scripts
* opentfd.service - template of linux systemd service for 24/7 execution on VDS

### For non-compiled versions
1. `pip3 install reqirements.txt`
2. Add [API token and hash](https://core.telegram.org/api/obtaining_api_id) to secret.template.py and rename it to secret.py
3. `python3 opentfd.py`

### Requirements
* Latest version of Telethon: http://telethon.readthedocs.io/en/stable/
* Translator: https://github.com/mouuff/mtranslate.git

Follow author and contributors at Telegram:
* https://t.me/MediaTube_stream
* https://t.me/nastalo
