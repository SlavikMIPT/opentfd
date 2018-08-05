# OpenTFD
* Merges serial Telegram messages, if between them a pause of less than 30 seconds
* Integrated google translator
### Compiled
* opentfd-win-noproxy.exe - windows daemon without proxy
* opentfd-win-proxy.exe - windows daemon with proxy
* opentfd-linux-noproxy - linux daemon without proxy
* opentfd-ubuntu-noproxy - ubunti daemon without proxy
* opentfd.service - template of linux systemd service for 24/7 execution on VDS

requires latest version of Telethon
http://telethon.readthedocs.io/en/stable/

Translator:
https://github.com/mouuff/mtranslate.git
