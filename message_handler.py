import random 
import sys
import traceback

print("Module message_handler has been loaded.")

async def pager(string, function):
    import textwrap
    stringWrapped = textwrap.wrap(str(string), 2000, replace_whitespace=False)
    for line in stringWrapped:
        await function(line)

users_enabled = set()
user_id_to_priviledged_user = dict()
already_matched = {}
client = None

async def add_user_to_database_if_not_already_there(user_id):
    global already_matched
    try: already_matched[user_id]
    except KeyError:
        already_matched[user_id] = set([user_id])

async def get_permission_from_user(user):
    global user_id_to_priviledged_user

    with open("dm.txt", "a+") as file :
        file.write(str(user.id) + "\n")

    user_id_to_priviledged_user[user.id]=user
    #print("success")
    #print(user_id_to_priviledged_user)
    #TODO: send welcome message

    #will raise exception if getting permission failed
    user_id_to_priviledged_user[user.id].status
    dm = await user.create_dm()
    await dm.send(
        "Permissions granted. For aviable commands type .help"
    )

async def enable_service_for_user(user):
    global users_enabled
    dm = await message.author.create_dm()
    try: user_id_to_priviledged_user[message.author.id].status
    except: 
        await dm.send(
            "Failed, permissions not granted\n"
            "https://discord.gg/cgTQFtzrry"
        )
        #TODO: Change this message
        return
    users_enabled.add(user.id)
    await dm.send("Enabled. To leave the list type .disable or .dis")

async def disable_service_for_user(user):
    global users_enabled
    dm = await message.author.create_dm()
    try: users_enabled.remove(message.author.id)
    except KeyError: await dm.send("Already disabled.")
    else: await dm.send("Disabled.")

async def match(me):
    global users_enabled
    shuffled_users=list(users_enabled)
    random.shuffle(shuffled_users)
    for stranger_id in shuffled_users:
        if stranger_id in already_matched[me.id]:
            continue
        elif me.id in already_matched[stranger_id]:
            continue
        stranger=user_id_to_priviledged_user[stranger_id]
        if not str(stranger.status) in ("online", "idle"):
            continue
        else:
            already_matched[me.id].add(stranger)
            try: users_enabled.remove(me.id)
            except: pass
            try: users_enabled.remove(stranger_id)
            except: pass
            text = (
                "You have been matched with {person}.\n"
                "Also, you have been removed from the list of aviable users.\n"
                "To enable it again, type .enable or .en"
            )
            await stranger.send(text.format(person=me))
            await me.send(text.format(person=stranger))
            return
    await me.send("Noone seems to be online at the moment, please try again later.")

async def on_message(message):
    if message.author == client.user:
        return
    #if not message.content.startswith("/"):
    #    return
    globals().update(locals())

    global users_enabled
    global user_id_to_priviledged_user
    global already_matched
    
    await add_user_to_database_if_not_already_there(message.author.id)

    if message.content.startswith(".grant"):
        await get_permission_from_user(
            user=message.author
        )
        await message.channel.send("Permissions granted, you can leave this server now")

    """
    if message.content.startswith(".reactmsg"):
        text = message.content[10:]
        message = await message.channel.send(text)
        global react_messages
        react_messages.append(message.id)
        #print(react_messages)
    """

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
        await enable_service_for_user(message.author)

    if message.content.startswith(".disable") or message.content.startswith(".dis"):
        try: await message.delete()
        except: pass
        await disable_service_for_user(message.author)

    if message.content.startswith(".match"):
        try: await message.delete()
        except: pass
        await match(message.author)

    if message.content.startswith("%"):
        import io
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