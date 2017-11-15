from pytg.sender import Sender
from utilities import info


class ForwardRule:
    # RULES

    def __init__(self, from_chat, to_chat, msg_contains=""):
        self._from_chat = from_chat
        self._to_chat = to_chat
        self._msg_contains = msg_contains

    def evaluate(self, telegram_msg):
        if 'text' in telegram_msg:
            if self._msg_contains in telegram_msg['text'] or self._msg_contains == "":
                # print("msg match")
                pass
            else:
                # print("not msg match")
                return False

        if 'receiver' in telegram_msg and 'id' in telegram_msg['receiver'] and telegram_msg['receiver'][
            'id'] == self._from_chat:
            return True

        return False

    def execute(self, telegram_msg):
        if self.evaluate(telegram_msg=telegram_msg):
            try:
                print("FORWARDED " + self.__repr__())
            except TypeError as ex:
                print("FORWARDED PRINT ERROR")
            # print(telegram_msg)
            if "text" in telegram_msg:
                sender.msg(self._to_chat, telegram_msg['text'])
            elif "media" in telegram_msg:
                sender.fwd_media(self._to_chat, telegram_msg['id'])
                if telegram_msg['media']['caption']:
                    sender.msg(self._to_chat, telegram_msg['media']['caption'])
            else:
                sender.fwd(self._to_chat, telegram_msg['id'])

    def __str__(self):
        id = "ERROR LOADING THIS RULE"
        try:
            from_info = info(self._from_chat)
            to_info = info(self._to_chat)
            # print(from_info)
            # print(to_info)
            id = from_info["print_name"] + " " + to_info["print_name"]
        except:
            pass
        return id

    def is_still_valid(self):
        try:
            from_info = info(self._from_chat)
            to_info = info(self._to_chat)
            return not(from_info is None or to_info is None)
        except:
            return False

    def __repr__(self):
        id = "ERROR LOADING THIS RULE"
        try:
            from_info = info(self._from_chat)
            to_info = info(self._to_chat)
            # print(from_info)
            # print(to_info)
            id = "De " + from_info["print_name"] + " a " + to_info["print_name"]
            # id = "De " + from_info + " a " + to_info
        except:
            pass
        return id

    def __eq__(self, other):
        return self._to_chat == other._to_chat and self._from_chat == other._from_chat


sender = Sender(host="localhost", port=4458)
admin = sender.get_self()
