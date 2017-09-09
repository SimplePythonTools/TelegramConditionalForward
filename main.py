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


@coroutine
def example_function(receiver):
    try:
        while True:
            telegram_msg = (yield)
            print('Full dump: {array}'.format(array=str(telegram_msg)))
            # check for admin
            if adminCommands.handle(telegram_msg):
                continue

            for rule in RuleManager.rules:
                rule.evaluate(telegram_msg)

    except KeyboardInterrupt:
        receiver.stop()
    # except Exception as ex:
    #     sender.send_msg(admin['id'], "Unexpected error " + str(ex))
    #     receiver.stop()
    #     raise ex


receiver.message(example_function(
    receiver))

sender.send_msg(admin['id'], "Telegram Conditional Forward is Disabled")
