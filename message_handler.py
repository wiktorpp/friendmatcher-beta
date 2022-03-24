import random 
import sys
import traceback

from user import User

print("Module message_handler has been loaded.")

async def pager(string, function):
    import textwrap
    stringWrapped = textwrap.wrap(str(string), 2000, replace_whitespace=False)
    for line in stringWrapped:
        await function(line)

users = dict()
User.users = users

async def on_message(message):
    global users
    
    try:
        self = users[message.author.id]
    except KeyError:
        self = users[message.author.id] = User(member=message.author)

    if message.content.startswith(".grant"):
        await self.store_permissions_for_user(message.author)
        await message.channel.send("Permissions granted, you can leave this server now")

    if message.content.startswith(".help"):
        await message.channel.send(
            "Aviable commands:\n"
            ".enable .en\n"
            ".disable .dis\n"
            ".match\n"
        )

    if message.content == ".enable" or message.content == ".en":
        try: await message.delete()
        except:pass
        await self.enable_service()

    if message.content == ".disable" or message.content == ".dis":
        try: await message.delete()
        except: pass
        await self.disable_service()
    
    if message.content.startswith(".intro"):
        try: await message.delete()
        except: pass
        new_introduction = message.content[7:]
        if len(new_introduction) == 0:
            await self.dm(
                "Your introduction is:\n"
                f"{self.introduction}\n"
                "To change your introduction, type \".intro <new intro>\""
            )
        else:
            self.introduction = new_introduction
            await self.dm("Ok")

    if message.content == ".match":
        try: await message.delete()
        except: pass
        await self.match()

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
            globals().update(locals())
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