import random
from tags import Tags

users = dict()

def get_user(member):
    global users
    try:
        return users[member.id]
    except KeyError:
        users.update(
            {member.id: User(member=member)}
        )
        return users[member.id]

class User:
    def __init__(self, member=None):
        self.member = member
        self.enabled = False
        self.already_matched_with = {self.member.id}
        self.dm_channel = None
        self.tags = Tags()
        self.introduction = "This user did not set their introduction."

    def __str__(self):
        return str(self.member)
    
    def __eq__(self, other):
        try:
            return self.member.id == other.member.id
        except KeyError:
            return self.member.id == other.id

    async def store_permissions_for_user(self, member):
        with open("dm.txt", "a+") as file :
            file.write(f"{member.id}\n")

        try: member.status
        except AttributeError: 
            await (await member.create_dm()).send(
                "Unknown error occurred. (This command does not work in DMs)"
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
                "https://discord.gg/xxxxxxxxxx"
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
        shuffled_users=list(users.values())
        random.shuffle(shuffled_users)
        for other in shuffled_users:
            if other.enabled != True:
                continue
            elif other.member.id in self.already_matched_with:
                continue
            elif self.member.id in other.already_matched_with:
                continue
            elif not str(other.member.status) in ("online", "idle"):
                continue
            else:
                self.already_matched_with.add(other.member.id)
                self.enabled = False
                other.enabled = False
                text = (
                    "You have been matched with {person}.\n"
                    "Also, you have been removed from the list of aviable users.\n"
                    "To enable aviability again, type .enable or .en\n\n"
                    "{introduction}"
                )
                await other.dm(text.format(person=self, introduction=self.introduction))
                await self.dm(text.format(person=other, introduction=other.introduction))
                return
        await self.dm("Noone seems to be online at the moment, please try again later.")

if __name__ == "__main__":
    Tags.test()
    import pdb
    pdb.set_trace()