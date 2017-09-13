from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

from AdminCommands import AdminCommands
from RuleManager import RuleManager

receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)

admin = sender.get_self()
adminCommands = AdminCommands(admin)

print("Got: >%s<" % admin)
username = admin.username
print("my username is {user}".format(user=username))

sender.send_msg(admin['id'], "Reenvio de mensajes condicional activado")

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
            sender.send_msg(admin['id'], "Unexpected error " + str(ex))
            sender.send_msg(admin['id'], "Error type" + type(ex))
            sender.send_msg(admin['id'], "debug")
            sender.send_msg(admin['id'], ex.__repr__())
            sender.send_msg(admin['id'], "Envia esta información al desarrollador")
            ERROR_COUNT_LIMIT -= 1
            if ERROR_COUNT_LIMIT == 0:
                sender.send_msg(admin['id'], "El programa se apagará por motivos de seguridad.")
                raise ex
            else:
                sender.send_msg(admin['id'],
                                "Quedan " + ERROR_COUNT_LIMIT + " errores antes de que se apague el programa.")


receiver.message(example_function(receiver))

sender.send_msg(admin['id'], "El reenvio de mensajes condicional está desactivado")
