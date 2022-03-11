#    Copyright (C) Midhun KM 2020
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import io
import os
import re

from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest

from RXE import bot
from RXE.Configs import Config
from RXE.modules.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from RXE.modules.sql_helper.botusers_sql import add_me_in_db, his_userid
from RXE.modules.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)


@assistant_cmd("start", is_args=False)
async def start(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    devlop = await bot.get_me()
    hmmwow = devlop.first_name
    vent = event.chat_id
    mypic = Config.ASSISTANT_START_PIC
    starttext = f"Halo, {firstname} ! Senang Bertemu Dengan Anda, Baiklah, Saya { bot_id } , Asisten Bot yang Kuat. \n \n Tuan Saya [ { hmmwow } ](tg://user?id= { bot . uid } ) \n Anda Dapat Berbicara/Menghubungi Tuan Saya Menggunakan Bot Ini \n \n Jika Anda Ingin Asisten Anda Sendiri, Anda Dapat Menyebarkan Dari Tombol Di Bawah. \n \n Didukung Oleh [RXE](t.me/ezzraez) "
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"Hai Master, Ini Saya { bot_id } , Asisten Anda ! \n Apa yang Ingin Anda Lakukan hari ini ?",
            buttons=[
                [custom.Button.inline("Tampilkan Pengguna 🔥", data="users")],
                [custom.Button.inline("Perintah Untuk Asisten", data="gibcmd")],
                [
                    Button.url(
                        "Add Me to Group 👥", f"t.me/{bot_username}?startgroup=true"
                    )
                ],
            ],
        )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_file(
            event.chat_id,
            file=mypic,
            caption=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("Deploy a bot like this", data="deploy")],
                [Button.url("Help Me ❓", "t.me/ezzraez")],
            ],
        )
        if os.path.exists(mypic):
            os.remove(mypic)


# Data's


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
            message="Ini adalah milik pribadi. \n Terima Kasih Telah Menghubungi Saya.",
            buttons=[
                [Button.url("Manage BY", "t.me/ezzraez")],
            ],
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "Daftar Total Pengguna Di Bot. \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "userlist.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                caption="Daftar Total Pengguna Di Bot Anda.",
                allow_cache=False,
            )
    else:
        pass


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
    await event.delete()
    grabon = "Halo Ini Beberapa Perintah \n /start - Periksa apakah saya sudah menyala \n ➤ /ping - Pong! \n ➤ /tr <lang-code> \n /broadcast - Mengirim Pesan Ke semua Pengguna Di Bot \n /id - Menampilkan ID Pengguna Dan Media \n ➤ /addnote - Tambahkan Catatan \n ➤ /notes - Menampilkan Catatan \n ➤ /rmnote - Hapus Catatan \n /alive - Apakah Saya Hidup? \n ➤ /bun - Bekerja Dalam Grup , Mencekal Pengguna \n ➤ /unbun - Membatalkan Larangan Pengguna di Grup \n /prumote - Mempromosikan Pengguna \n /demute - Menurunkan Pengguna \n/pin - Menyematkan Pesan \n /stats - Menampilkan Total Pengguna Di Bot"
    await tgbot.send_message(event.chat_id, grabon)


# Bot Permit.
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def all_messages_catcher(event):
    if is_he_added(event.sender_id):
        return
    if event.raw_text.startswith("/"):
        pass
    elif event.sender_id == bot.uid:
        return
    else:
        await event.get_sender()
        event.chat_id
        sed = await event.forward_to(bot.uid)
        # Add User To Database ,Later For Broadcast Purpose
        # (C) @SpecHide
        add_me_in_db(sed.id, event.sender_id, event.id)


@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def sed(event):
    msg = await event.get_reply_message()
    if msg is None:
        return
    msg.id
    msg_s = event.raw_text
    user_id, reply_message_id = his_userid(msg.id)
    if event.sender_id == Config.OWNER_ID:
        if event.raw_text.startswith("/"):
            return
        if event.text is not None and event.media:
            bot_api_file_id = pack_bot_file_id(event.media)
            await tgbot.send_file(
                user_id,
                file=bot_api_file_id,
                caption=event.text,
                reply_to=reply_message_id,
            )
        else:
            msg_s = event.raw_text
            await tgbot.send_message(
                user_id,
                msg_s,
                reply_to=reply_message_id,
            )


@assistant_cmd("broadcast", is_args=True)
@god_only
async def sedlyfsir(event):
    msgtobroadcast = event.pattern_match.group(1)
    userstobc = get_all_users()
    error_count = 0
    sent_count = 0
    hmmok = ""
    if msgtobroadcast == None:
        await event.reply("`Sebentar,. Apa yang di broadcast?`")
        return
    elif msgtobroadcast == " ":
        await event.reply("`Sebentar, apa yang akan di broadcast?`")
        return
    for starkcast in userstobc:
        try:
            sent_count += 1
            await tgbot.send_message(
                int(starkcast.chat_id),
                "**Hey, You Have Received A New Broadcast Message**",
            )
            await tgbot.send_message(int(starkcast.chat_id), msgtobroadcast)
            await asyncio.sleep(0.2)
        except Exception as e:
            hmmok += f"Errors : {e} \n"
            error_count += 1
    await tgbot.send_message(
        event.chat_id,
        f"Broadcast Done in {sent_count} Group/Users {error_count} Error and Total Number Was {len(userstobc)}",
    )


@assistant_cmd("stats", is_args=False)
@peru_only
async def starkisnoob(event):
    starkisnoob = get_all_users()
    await event.reply(
        f"**Stats Of Bot Anda** \n Total Pengguna Di Bot => {len(starkisnoob)}"
    )


@assistant_cmd("help", is_args=False)
@peru_only
async def starkislub(event):
    grabonx = "Halo Ini Beberapa Perintah \n /start - Periksa apakah saya sudah menyala \n ➤ /ping - Pong! \n /tr <lang-code> \n /broadcast - Mengirim Pesan Ke semua Pengguna Di Bot \n /id - Menampilkan ID Pengguna Dan Media \n ➤ /addnote - Tambahkan Catatan \n ➤ /notes - Menampilkan Catatan \n ➤ /rmnote - Hapus Catatan \n /alive - Apakah Saya Hidup? \n ➤ /bun - Bekerja Dalam Grup , Mencekal Pengguna \n ➤ /unbun - Membatalkan Larangan Pengguna di Grup \n /prumote - Mempromosikan Pengguna \n /demute - Menurunkan Pengguna \n/pin - Menyematkan Pesan \n /stats - Menampilkan Total Pengguna Di Bot"
    await event.reply(grabonx)


@assistant_cmd("block", is_args=False)
@god_only
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if is_he_added(user_id):
        await event.reply("Already Blacklisted")
    elif not is_he_added(user_id):
        add_nibba_in_db(user_id)
        await event.reply("masuk ke daftar blacklist")
        await tgbot.send_message(
            user_id,
            "Anda Telah Masuk Daftar Hitam Dan Anda Tidak Dapat Mengirim Pesan Kepada Tuan Saya Sekarang.",
        )


@assistant_cmd("unblock", is_args=False)
@god_only
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if not is_he_added(user_id):
        await event.reply("Not Even. Blacklisted 🤦🚶")
    elif is_he_added(user_id):
        removenibba(user_id)
        await event.reply("DisBlacklisted This Dumb Person")
        await tgbot.send_message(user_id, "Anda Telah Di-Unblacklist oleh Tuan Saya.")
