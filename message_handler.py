import random 
import sys
import traceback

from user import User

print("Module message_handler has been loaded.")

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
        import sys
        import traceback
        import textwrap
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            request = message.content[1:]
            try:
                exec(
                    "async def request_funct():\n" +
                    "    return_value = (" + request + ")" + "\n"
                    "    globals().update(locals())\n"
                    "    return return_value",
                    globals()
                )
            except:
                exec(
                    "async def request_funct():\n" +
                    "    " + request.replace("\n", "\n    ") + "\n"
                    "    globals().update(locals())\n"
                    "    return None",
                    globals()
                )
            return_value = await request_funct()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            if return_value != None:
                output = str(return_value) + "\n" + output
        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            for chunk in textwrap.wrap(output, 2000, replace_whitespace=False):
                await message.channel.send(chunk)

    globals().update(locals())