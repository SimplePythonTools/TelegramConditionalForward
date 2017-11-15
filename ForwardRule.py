from pytg.sender import Sender
from utilities import info


class ForwardRule:
    # RULES

    def __init__(self, _from_chat, _to_chat, _msg_contains=""):
        self._from_chat = _from_chat
        self._to_chat = _to_chat
        self._msg_contains = _msg_contains
        self._from_chat_name = None
        self._to_chat_name = None

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

    def get_names_from_server(self):
        try:
            is_new = ("_from_chat_name" in self.__dict__)
            if not is_new:
                self._from_chat_name = "ERROR"
            is_new = ("_to_chat_name" in self.__dict__)
            if not is_new:
                self._to_chat_name = "ERROR"
            if "ERROR" in self._from_chat_name and \
                "ERROR" in self._to_chat_name:
                from_info = info(self._from_chat)
                to_info = info(self._to_chat)
                self._from_chat_name = from_info["print_name"]
                self._to_chat_name = to_info["print_name"]
                return True
            else:
                return True
        except:
            return False

    def __str__(self):
        id = "ERROR LOADING THIS RULE"
        self.get_names_from_server()
        if self._from_chat_name is None or self._to_chat_name is None:
            return id
        id = self._from_chat_name + " " + self._to_chat_name
        return id

    def __repr__(self):
        id = "ERROR LOADING THIS RULE"
        self.get_names_from_server()
        if self._from_chat_name is None or self._to_chat_name is None:
            return id
        id = "De " + self._from_chat_name + " a " + self._to_chat_name
        return id

    def __eq__(self, other):
        return self._to_chat == other._to_chat and self._from_chat == other._from_chat


sender = Sender(host="localhost", port=4458)
admin = sender.get_self()
