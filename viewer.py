#!/usr/bin/env python3

import toml
from telethon.sync import TelegramClient, events

config = toml.load("config.toml")

client = TelegramClient(config["phone_number"], config["api_id"], config["api_hash"])
client.start()

async def main():
    archived = []

    async for d in client.iter_dialogs():
        if d.archived:
            archived.append(d.id)
            if d.unread_count > 0:
                await client.send_read_acknowledge(d)

    @client.on(events.NewMessage(archived))
    async def read(e):
        await e.mark_read()

    await client.run_until_disconnected()

client.loop.run_until_complete(main())
