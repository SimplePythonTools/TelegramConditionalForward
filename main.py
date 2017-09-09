from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine
import sys

receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)

res = sender.get_self()
print("Got: >%s<" % res)
username = res.username
print("my username is {user}".format(user=username))

sender.send_msg(res['id'], "Reenvio de mensajes condicional activado")

receiver.start()

@coroutine
def example_function(receiver):
    try:
        while True:
            msg = (yield)
            print('Full dump: {array}'.format(array=str(msg)))
            if 'sender' in msg and 'username' in msg['sender'] and msg['sender']['username'] == 'MetalBlueberry':
                sender.fwd("$05000000015e714367c8a72dc125afb1", msg['id'])
    except KeyboardInterrupt:
        receiver.stop()


receiver.message(example_function(
    receiver))

sender.send_msg(res['id'], "Telegram Conditional Forward is Dis")
