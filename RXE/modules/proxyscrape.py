# Created By @StarkXD
# Fixed By @MrConfused
# UserBot Plugin To Send Fresh Proxies From Proxyscrape.com
# Banned For Sensible Userbot And Users.
# Usage : For Http Proxy : .proxyhttp , For Socks4 : .proxysocks4 , For socks5 : .proxysocks5

import os

from pySmartDL import SmartDL

from RXE import CMD_HELP
from RXE.utils import friday_on_cmd, sudo_cmd

STARK_HTTP = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all"
HTTP_TXT = "**Proxy Info** \nType: __HTTPS__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: All \nAnonymity: __All__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇"
STARK_SOCKS4 = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all"
SOCKS4_TXT = "**Proxy Info** \nType: __SOCKS4__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: __Only For Http Proxy__ \nAnonymity: __Only For Http__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇"
STARK_SOCKS5 = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all"
SOCKS5_TXT = "**Proxy Info** \nType: __SOCKS4__ \nTimeOut: __10000__ \nCountry: __All__ \nSsl: __Only For Http Proxy__ \nAnonymity: __Only For Http__ \n[Click Here To View Or Download File Manually](https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all) \nUploaded By [Friday](https://github.com/starkgang/FridayUserBot) \n**Here Is Your Proxy** 👇"
sedpng = "https://soon.proxyscrape.com/asset/img/service/downloadicon.svg"


@friday.on(friday_on_cmd(pattern="http$"))
@friday.on(sudo_cmd(pattern="http$", allow_sudo=True))
async def starkxD(event):
    await event.get_chat()
    file_name = "proxy_http.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name)
    downloader = SmartDL(f"{STARK_HTTP}", downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    await event.client.send_file(
        event.chat_id,
        downloaded_file_name,
        force_document=False,
        thumb=sedpng,
        caption=HTTP_TXT,
    )


@friday.on(friday_on_cmd(pattern="socks4$"))
@friday.on(friday_on_cmd(pattern="socks4$", allow_sudo=True))
async def starkgang(event):
    await event.get_chat()
    file_name = "proxy_socks4.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name)
    downloader = SmartDL(f"{STARK_SOCKS4}", downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    # await borg.send_message(event.chat_id , SOCKS4_TXT)
    await event.client.send_file(
        event.chat_id,
        downloaded_file_name,
        thumb=sedpng,
        caption=SOCKS4_TXT,
        allow_cache=False,
        force_document=False,
    )


@friday.on(friday_on_cmd(pattern="socks5$"))
@friday.on(friday_on_cmd(pattern="socks5$", allow_sudo=True))
async def friday(event):
    await event.get_chat()
    file_name = "proxy_socks5.txt"
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name)
    downloader = SmartDL(f"{STARK_SOCKS5}", downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    # await borg.send_message(event.chat_id , SOCKS5_TXT)
    await event.client.send_file(
        event.chat_id,
        downloaded_file_name,
        thumb=sedpng,
        caption=SOCKS5_TXT,
        allow_cache=False,
        force_document=False,
    )


CMD_HELP.update(
    {
        "proxyscrape": "**Proxy scrape**\
\n\n**Syntax : **`.http`\
\n**Usage :** scrapes http proxies automatically from many websites.\
\n\n**Syntax : **`.socks4`\
\n**Usage :** scrapes socks4 proxies automatically from many websites.\
\n\n**Syntax : **`.socks5`\
\n**Usage :** Scrapes socks5 proxies automatically from many websites."
    }
)
