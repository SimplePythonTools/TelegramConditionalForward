from pytg.sender import Sender
from ForwardRule import ForwardRule
from RuleManager import RuleManager
from utilities import info

sender = Sender(host="localhost", port=4458)


class AdminCommands:
    def __init__(self, admin):
        RuleManager.load_rules()
        self._admin = admin
        self._commands = {'canales': self._do_channels,
                          'contactos': self._do_contacts,
                          'dialogos': self._do_dialogs,
                          'añadir': self._do_add_rule,
                          'eliminar': self._do_remove_rule,
                          'reglas': self._do_rules,
                          'ayuda': self._do_help}

    def handle(self, telegram_msg):
        if 'sender' in telegram_msg and 'username' in telegram_msg['sender'] and telegram_msg['sender']['id'] == \
                self._admin['id']:
            for command, command_function in self._commands.items():
                if 'text' in telegram_msg and command.lower() == telegram_msg['text'].split(' ')[0].lower():
                    command_function(telegram_msg)

    def _do_channels(self, telegram_msg):
        channels = sender.channel_list()

        def get_name(data):
            return data['print_name']

        channles_names = sorted(map(get_name, channels))

        sender.msg(self._admin['id'], "\n".join(channles_names))

    def _do_contacts(self, telegram_msg):
        contacts = sender.contacts_list()

        def get_name(data):
            return data['print_name']

        contact_list = sorted(map(get_name, contacts))

        sender.msg(self._admin['id'], "\n".join(contact_list))

    def _do_dialogs(self, telegram_msg):
        contacts = sender.dialog_list()

        def get_name(data):
            return data['print_name']

        dialog_list = sorted(map(get_name, contacts))

        sender.msg(self._admin['id'], "\n".join(dialog_list))

    def _create_rule(self, from_chat, to_chat):
        info_from_chat = info(from_chat)
        if info_from_chat is None:
            sender.msg(self._admin['id'], from_chat + " no existe")
            sender.msg(self._admin['id'],
                       "Puedes obtener una lista de los chat disponibles diciendo \"dialogos\" \"canales\" o \"contactos\"")
            return

        info_to_chat = info(to_chat)
        if info_to_chat is None:
            sender.msg(self._admin['id'], to_chat + " no existe")
            sender.msg(self._admin['id'],
                       "Puedes obtener una lista de los chat disponibles diciendo \"dialogos\" \"canales\" o \"contactos\"")
            return
        return ForwardRule(info_from_chat['id'], info_to_chat['id'])

    def _do_add_rule(self, telegram_msg):
        params = telegram_msg['text'].split(' ')
        if len(params) != 3:
            sender.msg(self._admin['id'], "Introduce una nueva regla como \"añadir chat_origen chat_destino\" ")
            sender.msg(self._admin['id'],
                       "Puedes obtener una lista de los chat disponibles diciendo \"dialogos\" \"canales\" o \"contactos\"")
            return
        from_chat = params[1]
        to_chat = params[2]
        new_rule = self._create_rule(from_chat, to_chat)
        if new_rule:
            if new_rule in RuleManager.rules:
                sender.msg(self._admin['id'], "La Regla ya existe")
            else:
                RuleManager.rules.append(new_rule)
                sender.msg(self._admin['id'], "Regla creada con éxito")
                RuleManager.save_rules()

    def _do_remove_rule(self, telegram_msg):
        params = telegram_msg['text'].split(' ')
        if len(params) != 3:
            sender.msg(self._admin['id'], "Elimina una regla como \"eliminar chat_origen chat_destino\" ")
            sender.msg(self._admin['id'], "Puedes obtener una lista de las reglas diciendo \"reglas\" ")
            return
        from_chat = params[1]
        to_chat = params[2]
        new_rule = self._create_rule(from_chat, to_chat)
        if new_rule:
            if new_rule in RuleManager.rules:
                RuleManager.rules.remove(new_rule)
                sender.msg(self._admin['id'], "Regla eliminada con éxito")
                RuleManager.save_rules()
            else:
                sender.msg(self._admin['id'], "La Regla no existe")

    def _do_rules(self, telegram_msg):

        contains_invalid_channels = False
        for rule in list(RuleManager.rules):
            if not rule.is_still_valid():
                RuleManager.rules.remove(rule)
                sender.msg(self._admin['id'], "Eliminada regla inválida.")
                contains_invalid_channels = True
        if contains_invalid_channels:
            RuleManager.save_rules()

        msg = "\n".join(map(str, RuleManager.rules))
        if msg:
            sender.msg(self._admin['id'], "Estas son las Reglas actuales.")
            sender.msg(self._admin['id'], msg)
        else:
            sender.msg(self._admin['id'], "No hay reglas definidas.")

    def _do_help(self, telegram_msg):
        sender.msg(self._admin['id'], "\n".join(sorted(self._commands.keys())))
