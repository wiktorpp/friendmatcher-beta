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

users_enabled = set()
users_elevated_priviledges = dict()
already_matched = {}

react_messages = []

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))
    await (await client.get_user(496709767914586112).create_dm()).send("Already disabled.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #if not message.content.startswith("/"):
    #    return
    globals().update(locals())

    global users_enabled
    global users_elevated_priviledges
    global already_matched
    try: already_matched[message.author.id]
    except KeyError:
        already_matched[message.author.id] = set([message.author.id])
    
    if message.content.startswith(".grant"):
        with open("dm.txt", "a+") as file :
            file.write(str(message.author.id) + "\n")

        users_elevated_priviledges[message.author.id]=message.author
        #print("success")
        #print(users_elevated_priviledges)
        #TODO: send welcome message
        try: 
            status = users_elevated_priviledges[message.author.id].status
        except: await message.channel.send("error")
        else: 
            await message.channel.send("Permissions granted, you can leave this server now")
            dm = await message.author.create_dm()
            await dm.send(
                "Permissions granted. For aviable commands type .help"
            )

    if message.content.startswith(".reactmsg"):
        text = message.content[10:]
        message = await message.channel.send(text)
        global react_messages
        react_messages.append(message.id)
        #print(react_messages)

    if message.content.startswith(".help"):
        await message.channel.send(
            "Aviable commands:\n"
            ".enable .en\n"
            ".disable .dis\n"
            ".match\n"
        )

    if message.content.startswith(".enable") or message.content.startswith(".en"):
        try: await message.delete()
        except:pass
        dm = await message.author.create_dm()
        try: users_elevated_priviledges[message.author.id].status
        except: 
            await dm.send(
                "Failed, permissions not granted\n"
                "https://discord.gg/cgTQFtzrry"
            )
            #TODO: Change this message
            return
        users_enabled.add(message.author.id)
        await dm.send("Enabled. To leave the list type .disable or .dis")

    if message.content.startswith(".disable") or message.content.startswith(".dis"):
        try: await message.delete()
        except: pass
        try: users_enabled.remove(message.author.id)
        except KeyError: await (await message.author.create_dm()).send("Already disabled.")
        else: await (await message.author.create_dm()).send("Already disabled.")

    if message.content.startswith(".match"):
        try: await message.delete()
        except: pass
        #this is so dumb
        shuffled_users=list(users_enabled)
        random.shuffle(shuffled_users)
        for stranger_id in shuffled_users:
            if stranger_id in already_matched[message.author.id]:
                continue
            elif message.author.id in already_matched[stranger_id]:
                continue
            stranger=users_elevated_priviledges[stranger_id]
            if not (str(stranger.status) == "online" or str(stranger.status) == "idle"):
                continue
            else:
                already_matched[message.author.id].add(stranger)
                try: users_enabled.remove(message.author.id)
                except: pass
                try: users_enabled.remove(stranger_id)
                except: pass
                text = (
                    "You have been matched with {person}.\n"
                    "Also, you have been removed from the list of aviable users.\n"
                    "To enable it again, type .enable or .en"
                )
                await stranger.send(text.format(person=message.author))
                await message.author.send(text.format(person=stranger))
                return
        await message.author.send("Noone seems to be online at the moment, please try again later.")
        
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

#https://discord.com/oauth2/authorize?client_id=738728621459505184&permissions=8&scope=bot