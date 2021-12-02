import discord
from TOKEN import TOKEN
import sys
import io
import traceback
import textwrap

import random

client = discord.Client()


async def pager(string, function):
    stringWrapped = textwrap.wrap(str(string), 2000, replace_whitespace=False)
    for line in stringWrapped:
        await function(line)

users = set()
already_picked = {}

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))

@client.event
async def on_message(message):
    globals().update(locals())

    global users
    if message.content.startswith("/add"):
        try: await message.delete()
        except:pass
        users.add(message.author)
        dm = await message.author.create_dm()
        await dm.send("Added. To leave the list type /remove")

    if message.content.startswith("/remove"):
        try: await message.delete()
        except: pass
        users.remove(message.author)
        dm = await message.author.create_dm()
        await dm.send("Removed.")

    if message.content.startswith("/match"):
        while True:
            try: await message.delete()
            except: pass
            stranger = random.choice(list(users))
            #if stranger == message.author:
            #    continue
            await stranger.send(f"You have been picked by {str(message.author)}")
            break


    if message.content.startswith("%"):
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            progArr = message.content[1:].splitlines()
            progStrIndented = ""
            for i in progArr:
                progStrIndented += "\n    " + i
            exec(
                "async def t():" +
                progStrIndented +
                "\n    globals().update(locals())",
                globals()
            )
            await t()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            await pager(output, message.channel.send)

    globals().update(locals())

    #await message.channel.send(new_stderr.getvalue())
    #sys.stderr = old_stderr

client.run(TOKEN)

