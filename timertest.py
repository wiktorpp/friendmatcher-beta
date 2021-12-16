from threading import Timer

users=dict()

def hello(user):
    print(f"hello, {user}")

while True:
    cmd=input("cmd")
    user=input("user")
    if cmd == "start":
        t = Timer(5, hello, [user])
        users[user]=t
        t.start()
    elif cmd == "stop":
        users[user].cancel()
    elif cmd == "check":
        print(users[user].is_alive())
