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

def load_users_from_file():
    global users
    data = eval(open("dump.dat").read())
    print(data.items())
    for member_id, user_data in data.items():
        users.update(
            {member_id: User()}
        )
        print(1)

class User:
    def __init__(self, member=None):
        self.member = member
        self.enabled = False
        self.already_matched_with = {self.member.id}
        self.dm_channel = None
        self.tags = Tags()
        self.introduction = "This user did not set their introduction."

    def from_dict(dict):
        user = User()
        user.enabled = dict["enabled"]
        user.already_matched_with = dict["already_matched_with"]
        user.tags = dict["tags"]
        user.introduction = dict["introduction"]
        return user

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "already_matched_with": self.already_matched_with,
            "tags": self.tags,
            "introduction": self.introduction,
        }

    def __str__(self):
        return str(self.member)

    def __repr__(self):
        return str(self.member)
    
    def __eq__(self, other):
        try:
            return self.member.id == other.member.id
        except KeyError:
            return self.member.id == other.id

    async def store_permissions_for_user(self, member):
        with open("dm.txt", "a+") as file:
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
    
    async def dm(self, message, file=None):
        if self.dm_channel == None:
            self.dm_channel = await self.member.create_dm()
        if file == None:
            await self.dm_channel.send(message)
        else:
            from discord import File
            await self.dm_channel.send(message, file=File(file))

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
        possible_matches = dict()
        for other in users.values():
            if other.enabled != True:
                continue
            elif other.member.id in self.already_matched_with:
                continue
            elif self.member.id in other.already_matched_with:
                continue
            elif not str(other.member.status) in ("online", "idle"):
                continue
            else:
                weight = self.tags.calculate_weight(other.tags) + other.tags.calculate_weight(self.tags)
                while True:
                    try: possible_matches[weight]
                    except KeyError:
                        possible_matches[weight] = other
                        break
                    else:
                        weight -= 1

        try:
            match = possible_matches[max(possible_matches.keys())]
        except ValueError: 
            await self.dm("Noone seems to be online at the moment, please try again later.")
        else:
            self.already_matched_with.add(match.member.id)
            self.enabled = False
            match.enabled = False
            text = (
                "You have been matched with {person}.\n"
                "Also, you have been removed from the list of aviable users.\n"
                "To enable aviability again, type .enable or .en\n\n"
                "Their tags are: {tags}\n"
                "And their introduction is:\n"
                "{introduction}"
            )
            await match.dm(text.format(person=self, tags=self.tags, introduction=self.introduction))
            await self.dm(text.format(person=match, tags=match.tags, introduction=match.introduction))

if __name__ == "__main__":
    Tags.test()
    import pdb
    pdb.set_trace()