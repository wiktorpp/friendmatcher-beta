import asyncio
import message_handler
import random

next_id = 0

messages = []

class Messageable:
    def __init__(self, name="Some user or channel"):
        self.name = name

    def __str__(self): raise NotImplementedError

    async def send(self, message):
        print(f"\033[96mMessage to {self.name}\033[39m> {message}")
        global messages
        messages.append(f"Message to {self.name}> {message}")

class Member(Messageable):
    def __init__(self, name=None, id=None):
        if id != None:
            self.id = id
        else: 
            global next_id
            self.id = next_id
            next_id += 1
        if name == None:
            self.name = str(id)
        self.status = "online"
        Messageable.__init__(self, name=f"{name}#0000")

    def __str__(self): return self.name

    async def create_dm(self):
        return Messageable(name=self.name)

class Message:
    def __init__(self, message="message", author=None, channel=None):
        self.content = message
        self.author = author
        self.channel = channel

async def main():
    test = True

    global message_handler
    people = {
        "john": Member("john"), 
        "robert": Member("robert"), 
        "alice": Member("alice"),
        "zack": Member("zack"),
        }
    person = people["john"]
    channel = Messageable(name="channel")
    if test:
        try:
            async def send(person, message):
                print(f"\033[95m{person.name}\033[39m>{message}")
                await message_handler.on_message(Message(message, person, channel))
            from importlib import reload
            #message_handler = reload(message_handler)
            for person in [Member("bob"), Member("alice"), Member("zack")]:
                for message in [".grant", ".en", ".intro placeholder_intro"]:
                    await send(person, message)
            person = Member("robert")
            for _ in range(4):
                await send(person, ".match")

            tests_passed = all((
                "You have been matched" in messages[17],
                "Noone seems to be online" in messages[18],
                "placeholder_intro" in messages[15]
            ))
            if tests_passed:
                print(f"\033[92mtest passed\033[39m")
            else:
                raise Exception
        except Exception as exception:
            print(f"\033[91mtest failed: {exception}\033[39m")
            raise exception

    person = people["john"]
    while True:
        message = input(f"\033[95m{person.name}\033[39m>")
        if message.startswith("/"):
            argv = message.split(" ")
            if argv[0] == "/exit": exit()
            if argv[0] == "/pdb": import pdb; pdb.set_trace()
            if argv[0] == "/su":
                if argv[1] == "new":
                    name = argv[2]
                    people.update({name: Member(name)})
                else: 
                    name = argv[1]
                try: person = people[name]
                except KeyError: print("Not found")
            if argv[0] == "/id": print(person.id)
        else:
            await message_handler.on_message(Message(message, person, channel))

asyncio.get_event_loop().run_until_complete(main())
