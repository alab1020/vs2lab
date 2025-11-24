import constRPC
import threading
import time

from context import lab_channel


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None
        self.callback = None
        self.callback_thread = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        if self.callback_thread and self.callback_thread.is_alive():
            self.callback_thread.join()
        self.chan.leave("client")

    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)
        self.callback = callback

        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server

        sender, ack = self.chan.receive_from(self.server)
        if ack == "ACK":
            print("ACK received")
        else:
            raise RuntimeError("ACK expected")
        
        self.callback_thread = threading.Thread(target=self._wait_for_result)
        self.callback_thread.start()
        
    def _wait_for_result(self):
        sender, result = self.chan.receive_from(self.server)
        self.callback(result)


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call

                    i = 0
                    while i < 10:
                        print("Working")
                        time.sleep(1)
                        i += 1

                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore
