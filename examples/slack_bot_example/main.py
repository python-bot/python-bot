import time
from slackclient import SlackClient

token = "xoxb-66919509936-ks52a9VQDoFp9KzxYZHTIHYQ"  # found at https://api.slack.com/web#authentication
sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        for message in sc.rtm_read():
            if message.get("type") == "message":
                self.on_message(user_id=message["user"], text=message["text"], channel=message["channel"])
        print(sc.rtm_read())
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
