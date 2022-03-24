import random

class User:
    def __init__(self, member=None):
        self.member = member
        self.enabled = False
        self.already_matched_with = {self}
        self.dm_channel = None
        self.introduction = "This user did not set their introduction."

    """
    def __eq__(self, other):
        try:
            return self.member.id == other.id
            print(1)
        except:
            print(2)
            return self.member.id == other.member.id
    """

    async def store_permissions_for_user(self, member):
        with open("dm.txt", "a+") as file :
            file.write(f"{member.id}\n")

        try: member.status
        except AttributeError: 
            await (await member.create_dm()).send(
                "Unknown error occurred."
            )
        else:
            self.member = member
            #TODO: send welcome message
            await (await member.create_dm()).send(
                "Permissions granted. For aviable commands type .help"
            )
    
    async def dm(self, message):
        if self.dm_channel == None:
            self.dm_channel = await self.member.create_dm()
        await self.dm_channel.send(message)

    async def enable_service(self):
        try: self.member.status
        except: 
            await self.dm(
                "Failed, permissions not granted\n"
                "https://discord.gg/cgTQFtzrry"
            )
            #TODO: Change this message
        else: 
            self.enabled = True
            await self.dm("Enabled. To disable type .disable or .dis")

    async def disable_service(self):
        if self.enabled:
            self.enabled = False
            await self.dm("Disabled.")
        else:
            await self.dm("Already disabled.")

    async def match(self):
        shuffled_users=list(self.users.values())
        random.shuffle(shuffled_users)
        for other in shuffled_users:
            if other.enabled != True:
                continue
            elif other in self.already_matched_with:
                continue
            elif self in other.already_matched_with:
                continue
            elif not str(other.member.status) in ("online", "idle"):
                continue
            else:
                self.already_matched_with.add(other)
                self.enabled = False
                other.enabled = False
                text = (
                    "You have been matched with {person}.\n"
                    "Also, you have been removed from the list of aviable users.\n"
                    "To enable aviability again, type .enable or .en\n\n"
                    "{introduction}"
                )
                await other.dm(text.format(person=self.member, introduction=self.introduction))
                await self.dm(text.format(person=other.member, introduction=other.introduction))
                return
        await self.dm("Noone seems to be online at the moment, please try again later.")