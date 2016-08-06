from wit import Wit
access_token = "YD75LLWGUB4GZPTHTZNWDURHMTHHELIR"

def send(request, message):
    print('Sending to user...', message['text'])


def my_action(request):
    print('Received from user...', request['text'])


actions = {
    'send': send,
    'my_action': my_action,
}

client = Wit(access_token=access_token, actions=actions)

session_id = 'my-user-session-42'
context0 = {}
context1 = client.run_actions(session_id, 'what is the weather in London?', context0)
print('The session state is now: ' + str(context1))
context2 = client.run_actions(session_id, 'and in Brussels?', context1)
print('The session state is now: ' + str(context2))

