import asyncio
import message_handler
import random

next_id = 0

messages = []

class Messageable:
    def __init__(self, name="Some user or channel"):
        self.name = name

    async def send(self, message):
        print(f"\033[96mMessage to {self.name}\033[39m> {message}")
        global messages
        #print(len(messages))
        messages.append(f"Message to {self.name}> {message}")

class Member(Messageable):
    def __init__(
        self, 
        id=None,
        name=None
        ):
        if id != None:
            self.id = id
        else: 
            global next_id
            self.id = next_id
            next_id += 1
        if name == None:
            self.name = str(id)
        self.status = "online"
        Messageable.__init__(self, name=name)

    def __str__(self):
        return self.name

    async def create_dm(self):
        return Messageable(name=self.name)

class Message:
    def __init__(self, author=None, message="message", channel=None):
        self.content = message
        self.author = author
        self.channel = channel

async def main():
    test = True

    global message_handler
    people = {
        "john": Member(name="john"), 
        "robert": Member(name="robert"), 
        "alice": Member(name="alice"),
        "zack": Member(name="zack"),
        }
    person = people["john"]
    channel = Messageable(name="channel")
    if test:
        try:
            async def send(person, message):
                print(f"\033[95m{person.name}\033[39m>{message}")
                await message_handler.on_message(Message(person, message, channel))
            from importlib import reload
            message_handler = reload(message_handler)
            for person in [Member(name="bob"), Member(name="alice"), Member(name="zack")]:
                for message in [".grant", ".en", ".intro placeholder_intro"]:
                    await send(person, message)
            person = Member(name="robert")
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
        except:
            print(f"\033[91mtest failed\033[39m")
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
                    people.update({name: Member(name=name)})
                else: 
                    name = argv[1]
                try: person = people[name]
                except KeyError: print("Not found")
            if argv[0] == "/id": print(person.id)
        else:
            await message_handler.on_message(Message(person, message, channel))

asyncio.get_event_loop().run_until_complete(main())
