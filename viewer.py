#!/usr/bin/env python3

import toml
from telethon import TelegramClient, utils, types, events

config = toml.load("config.toml")

client = TelegramClient(config["phone_number"], config["api_id"], config["api_hash"])
client.start()

async def main():
    archived = set()

    async for d in client.iter_dialogs():
        if d.archived:
            archived.add(d.id)
            if d.unread_count > 0:
                await client.send_read_acknowledge(d)

    @client.on(events.NewMessage(func=lambda e: e.chat_id in archived))
    async def read(e):
        await e.mark_read()

    @client.on(events.Raw(types.UpdateFolderPeers))
    async def _(e):
        added = e.folder_peers[0].folder_id == 1
        peers = (utils.get_peer_id(x.peer) for x in e.folder_peers)

        if added:
            for i in peers:
                print(f"chat {i} has been added to the archived list.")
                archived.add(i)
                await client.send_read_acknowledge(i)
        else:
            for i in peers:
                print(f"chat {i} has been removed from the archived list.")
                archived.remove(i)

    await client.run_until_disconnected()

client.loop.run_until_complete(main())
