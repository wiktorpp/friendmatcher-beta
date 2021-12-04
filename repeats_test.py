import random

users = set([1,2,3])
already_matched = {"me":[1]}

while True:
    stranger = random.choice(list(users))
    print(stranger)
    if stranger in already_matched["me"]:
        print("Already matched")
        continue
    print("Found")
    already_matched["me"].append(stranger)
    break

print(already_matched["me"])