"""Emoji
Available Commands:
.support
Credits to noone
"""


import asyncio

from RXE import CMD_HELP
from RXE.utils import friday_on_cmd


@friday.on(friday_on_cmd("infinityje"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 36)
    # input_str = event.pattern_match.group(1)
    # if input_str == "support":
    await event.edit("for our support group")
    animation_chars = [
        "Click here",
        "[Support Group](https://t.me/Infinityje)",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])


CMD_HELP.update(
    {
        "supportgroup": "**Support Group**\
\n\n**Syntax : **`.infinityje`\
\n**Usage :** Creates link for VirtualUserbot support group."
    }
)
