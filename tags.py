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

    def __len__(self):
        return len(self.am) + len(self.looking_for) + len(self.block)

    def __add__(self, other):
        return type(self)(
            am=set.union(self.am, other.am),
            looking_for=set.union(self.looking_for, other.looking_for),
            block=set.union(self.block, other.block)
        )
    
    def __sub__(self, other):
        return type(self)(
            am=self.am.difference(other.am),
            looking_for=self.looking_for.difference(other.looking_for),
            block=self.block.difference(other.block)
        )
    
    def __eq__(self, other):
        return all((
            self.am == other.am,
            self.looking_for == other.looking_for,
            self.block == other.block
        ))

    def add_from_str(self, string):
        tags = string.split(" ")
        try: tags.remove("")
        except ValueError: pass
        for tag in tags:
            stripped_tag = tag.replace(">", "").replace("<", "").replace("#", "")
            if ">" in tag or "<" in tag or "#" in tag:
                if ">" in tag:
                    self.am.add(stripped_tag)
                if "<" in tag:
                    self.looking_for.add(stripped_tag)
                if "#" in tag:
                    self.block.add(stripped_tag)
            else:
                self.am.add(stripped_tag)
                self.looking_for.add(stripped_tag)

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
        other = Tags.from_str(">1")
        other += Tags.from_str(">2")
        passed = other == Tags.from_str(">1 >2")
        passed = passed and self.calculate_weight(other) == 2
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