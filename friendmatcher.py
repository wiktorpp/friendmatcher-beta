import discord
from TOKEN import TOKEN

import message_handler

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

message_handler.client = client

users_enabled = set()
message_handler.users_enabled = users_enabled
user_id_to_priviledged_user = dict()
message_handler.user_id_to_priviledged_user = user_id_to_priviledged_user
already_matched = dict()
message_handler.already_matched = already_matched

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))

@client.event
async def on_message(message):
    if message.content == ".reload":
        pass
    else:
        await message_handler.on_message(message)

if __name__ == "__main__":
    client.run(TOKEN)

#https://discord.com/oauth2/authorize?client_id=738728621459505184&permissions=8&scope=bot