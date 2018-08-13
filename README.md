# OpenTFD
* Merges serial Telegram messages, if between them a pause of less than 30 seconds
* Integrated Google translator
### Compiled
* opentfd-win-noproxy.exe - windows daemon without proxy
* opentfd-win-proxy.exe - windows daemon with proxy
* opentfd-linux-noproxy - linux daemon without proxy
* opentfd-ubuntu-noproxy - ubunti daemon without proxy
### Scripts
* opentfd.service - template of linux systemd service for 24/7 execution on VDS
* Dockerfile

### For non-compiled versions
1. `pip3 install reqirements.txt`
2. Add (API token and hash)[https://core.telegram.org/api/obtaining_api_id] to secret.template.py and rename it to secret.py
3. `python3 opentfd.py`

### Requirements
* Latest version of Telethon: http://telethon.readthedocs.io/en/stable/
* Translator: https://github.com/mouuff/mtranslate.git

Telegram канал разработчика 
https://t.me/MediaTube_stream
