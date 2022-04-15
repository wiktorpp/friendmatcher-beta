import random

users = dict()

class Tags:
    def __init__(self, am=None, looking_for=None, block=None):
        if am == None: self.am = set()
        else: self.am = set(am)

        if looking_for == None: self.looking_for = set()
        else: self.looking_for = set(looking_for)

        if block == None: self.block = set()
        else: self.block = set(block)
    
    def __repr__(self):
        return f"Tags(am={self.am}, looking_for={self.looking_for}, block={self.block})"
    
    def __str__(self):
        dictionary = dict()
        for tag in self.am:
            try: dictionary[tag][0] = True
            except KeyError: dictionary[tag] = [True, False, False]
        for tag in self.looking_for:
            try: dictionary[tag][1] = True
            except KeyError: dictionary[tag] = [False, True, False]
        for tag in self.block:
            try: dictionary[tag][2] = True
            except KeyError: dictionary[tag] = [False, False, True]
        result = ""
        for key, value in dictionary.items():
            tag = ""
            if value[0]:
                tag += ">"
            if value[1]:
                tag += "<"
            if value[2]:
                tag += "#"
            tag += key
            result += f"{tag} "
        return result

    def add_from_str(self, string):
        tags = string.split(" ")
        for tag in tags:
            if ">" in tag or "<" in tag or "#" in tag:
                if ">" in tag:
                    self.am.add(tag.replace(">", "").replace("<", "").replace("#", ""))
                if "<" in tag:
                    self.looking_for.add(tag.replace(">", "").replace("<", "").replace("#", ""))
                if "#" in tag:
                    self.block.add(tag.replace(">", "").replace("<", "").replace("#", ""))
            else:
                self.am.add(tag.replace(">", "").replace("<", "").replace("#", ""))
                self.looking_for.add(tag.replace(">", "").replace("<", "").replace("#", ""))

    def from_str(string):
        result = Tags()
        result.add_from_str(string)
        return result
    
    class Blocked(Exception):
        pass

    def calculate_weight(self, other):
        result = 0
        for tag in self.looking_for:
            if tag in other.am:
                result += 1
        for tag in self.block:
            if tag in other.am:
                raise self.Blocked
        return result

    def test():
        self = Tags.from_str("<1 <2 <3 >4")
        other = Tags.from_str(">1 >2")
        passed = self.calculate_weight(other) == 2
        self = Tags.from_str("#blocked")
        other = Tags.from_str(">blocked")
        try:
            self.calculate_weight(other)
        except self.Blocked:
            passed = passed and True
        else:
            passed = False
        if passed:
            print(f"\033[92mTags test passed\033[39m")
        else:
            print(f"\033[91mTags test failed\033[39m")

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
        self.already_matched_with = {self}
        self.dm_channel = None
        self.introduction = "This user did not set their introduction."

    def __str__(self):
        return str(self.member)

    def __repr__(self):
        return str(self.member)

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
                await other.dm(text.format(person=self, introduction=self.introduction))
                await self.dm(text.format(person=other, introduction=other.introduction))
                return
        await self.dm("Noone seems to be online at the moment, please try again later.")

if __name__ == "__main__":
    Tags.test()