import asyncio
import message_handler
import random

next_id = 0

class Messageable:
    def __init__(self, name="Some user or channel"):
        self.name = name

    async def send(self, message):
        print(f"Message to {self.name}> {message}")

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
    global message_handler
    people = {"John": Member(name="John")}
    person = people["John"]
    channel = Messageable(name="channel")
    while True:
        message = input(f"{person.name}>")
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
                person = people[name]
            if argv[0] == "/id": print(person.id)
            if argv[0] == "/test":
                from importlib import reload
                message_handler = reload(message_handler)
                bob = Member(name="bob")
                alice = Member(name="alice")
                person = bob
                for message in [".grant", ".en", ".match"]:
                    print(f"{person.name}>{message}")
                    await message_handler.on_message(Message(person, message, channel))
                person = alice
                for message in [".grant", ".en", ".match"]:
                    print(f"{person.name}>{message}")
                    await message_handler.on_message(Message(person, message, channel))
        else:
            await message_handler.on_message(Message(person, message, channel))

asyncio.get_event_loop().run_until_complete(main())
