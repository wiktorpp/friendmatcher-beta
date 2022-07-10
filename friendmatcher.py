import discord
from TOKEN import TOKEN

import message_handler

from importlib import reload
import traceback

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")
    message_handler.client = client

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        try:
            await message_handler.on_message(message)
        except Exception:
            error = traceback.format_exc()
            await message.channel.send(f"```\n{error}\n```")

if __name__ == "__main__":
    client.run(TOKEN)

#https://discord.com/oauth2/authorize?client_id=738728621459505184&permissions=8&scope=bot