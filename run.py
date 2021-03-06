# -*- coding: utf-8 -*-
# @Date:   2017-03-20 10:52:39
# @Last Modified time: 2017-11-21 11:07:43
import select
from threading import Thread
from server import app, PORT, SELECT_TIMEOUT


class AcceptClient(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        """
        登录（免注册，但是要求用户计算机名不能重复）
        当有客户端连接时，把它加进 store
        """
        while True:
            client_socket, client_address = app.server_socket.accept()
            client_ip = client_address[0]
            app.logger.info("{client_ip} is connected".format(client_ip=client_ip))
            message_dict = app.parser(client_socket)
            if message_dict:
                view = app.find_view(message_dict.get("title"))
                if not view:
                    app.logger.error("message title error")
                    app.send_message(
                        app.error_msg(ext_data="message title error!"),
                        client_socket,
                        receiver="loginer"
                    )
                else:
                    view(message_dict, client_socket)


class TransmitData(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            # 阻塞，等待数据输入
            r_list, w_list, x_list = select.select(app.socket_iterator, [], [], SELECT_TIMEOUT)
            for client_socket in r_list:
                message_dict = app.parser(client_socket)
                if message_dict:
                    sender = app.get_user(client_socket)
                    if not sender:
                        app.logger.error("{sender} is not online".format(sender=sender))
                        app.send_message(
                            app.error_msg(ext_data="you are offline, please restart client!"),
                            client_socket
                        )
                    else:
                        view = app.find_view(message_dict.get("title"))
                        if not view:
                            app.logger.error("message title error")
                            app.send_message(
                                app.error_msg(ext_data="message title error!"),
                                client_socket
                            )
                        else:
                            view(message_dict, client_socket)


def main():
    accept_client = AcceptClient()
    transmit_data = TransmitData()
    accept_client.daemon = True
    transmit_data.daemon = True
    accept_client.start()
    transmit_data.start()
    jobs = [accept_client, transmit_data]
    for j in jobs:
        j.join()


if __name__ == '__main__':
    print("simple chat server listening 0.0.0.0:%s" % PORT)
    main()
