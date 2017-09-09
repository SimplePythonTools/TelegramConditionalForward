
from pytg.sender import Sender


class ForwardRule:
    def __init__(self, from_chat, to_chat, msg_contains  = ""):
        self._from_chat = from_chat
        self._to_chat = to_chat
        self._msg_contains = msg_contains
        
    def evauluate(self, telegram_msg):
        if 'test' in telegram_msg and self._msg_contains in telegram_msg['text']:
            if 'sender' in telegram_msg and 'username' in telegram_msg['sender'] and telegram_msg['sender']['id'] == self._from_chat:
                sender = Sender(host="localhost", port=4458)
                sender.send_msg(self._to_chat, telegram_msg['id'])

