import discord
from TOKEN import TOKEN
import sys
import io
import traceback
import textwrap

import random

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

async def pager(string, function):
    stringWrapped = textwrap.wrap(str(string), 2000, replace_whitespace=False)
    for line in stringWrapped:
        await function(line)

users = set()
user_dict = dict()
already_matched = {}

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #if not message.content.startswith("/"):
    #    return
    globals().update(locals())

    global users
    global user_dict
    global already_matched
    try: user_dict[str(message.author)]
    except: pass
    try: already_matched[message.author]
    except KeyError:
        already_matched[message.author] = set([message.author])
    
    if message.content.startswith("/help"):
        await message.channel.send(
            "Aviable commands: "
            "/enable"
            "/disable"
            "/match"
        )

    if message.content.startswith("/enable"):
        try: await message.delete()
        except:pass
        dm = await message.author.create_dm()
        try: message.author.status
        except: 
            await dm.send("Failed, did you send the command in a DM? (this command doesn't work through DMs)")
            return
        users.add(message.author)
        await dm.send("Enabled. To leave the list type /remove")

    if message.content.startswith("/disable"):
        try: await message.delete()
        except: pass
        users.remove(message.author)
        dm = await message.author.create_dm()
        await dm.send("Disabled.")

    if message.content.startswith("/match"):
        try: await message.delete()
        except: pass
        #this is so dumb
        shuffled_users=list(users)
        random.shuffle(shuffled_users)
        for stranger in shuffled_users:
            if stranger in already_matched[message.author]:
                continue
            elif not (str(stranger.status) == "online" or str(stranger.status) == "idle"):
                continue
            else:
                already_matched[message.author].add(stranger)
                await stranger.send(f"You have been matched with {str(message.author)}")
                await message.author.send(f"You have been matched with {str(stranger)}")
                return
        await message.author.send("Noone seems to be online at the moment, please try again later.")

    if message.content.startswith("/backup"):
        print(f"users = {users}")
        print(f"user_dict = {user_dict}")
        print(f"already_matched = {already_matched}")

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

#https://discord.com/oauth2/authorize?client_id=738728621459505184&permissions=8