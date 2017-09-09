from pytg.sender import Sender

sender = Sender(host="localhost", port=4458)


def info(id):
    info = sender.chat_info(id)
    if not 'error_code' in info:
        return info

    info = sender.user_info(id)
    if not 'error_code' in info:
        return info

    info = sender.channel_info(id)
    if not 'error_code' in info:
        return info
