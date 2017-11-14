import os
import pickle


class RuleManager:
    rules = list()

    @classmethod
    def save_rules(cls):
        with open(os.path.join(os.path.expanduser('~'), '.telegram-cli/rules.json'), "wb+") as fd:
            pickle.dump(cls.rules, fd)

    @classmethod
    def load_rules(cls):
        try:
            with open(os.path.join(os.path.expanduser('~'), '.telegram-cli/rules.json'), "rb") as fd:
                cls.rules = pickle.load(fd)

        except Exception  as ex:
            print("Error loading rules: " + str(ex))
