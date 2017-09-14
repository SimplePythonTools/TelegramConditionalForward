from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

from AdminCommands import AdminCommands
from RuleManager import RuleManager

import logging

logging.basicConfig(filename='runtime_log.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.info("Running start")

receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)

admin = sender.get_self()
adminCommands = AdminCommands(admin)

print("Got: >%s<" % admin)
username = admin.username
print("my username is {user}".format(user=username))

sender.send_msg(admin['id'], "Reenvio de mensajes condicional activado", enable_preview=True)

receiver.start()

ERROR_COUNT_LIMIT = 10


@coroutine
def example_function(receiver):
    while True:
        try:
            telegram_msg = (yield)
            # print('Full dump: {array}'.format(array=str(telegram_msg)))
            # check for admin
            if adminCommands.handle(telegram_msg):
                continue

            for rule in RuleManager.rules:
                rule.evaluate(telegram_msg)

        except KeyboardInterrupt:
            receiver.stop()
            break
        except Exception as ex:
            global ERROR_COUNT_LIMIT
            logging.error(ex, exc_info=True)
            ERROR_COUNT_LIMIT -= 1
            if ERROR_COUNT_LIMIT == 0:
                sender.send_msg(admin['id'], "El programa se apagará por motivos de seguridad.")
                raise ex
            else:
                sender.send_msg(admin['id'],
                                "Quedan " + ERROR_COUNT_LIMIT + " errores antes de que se apague el programa.")


receiver.message(example_function(receiver))

sender.send_msg(admin['id'], "El reenvio de mensajes condicional está desactivado")
