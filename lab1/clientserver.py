"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self._logger.info("Creating server socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

        # Telefonbuch
        self.telefonbuch = {
            "Korn": 13245,
            "Weber": 54321,
            "Hofmann": 15643,
            "Björn": 645646 
        }

    def handle_request(self, request):
        if request.startswith("GETALL"):
            entries = []
            for name, number in self.telefonbuch.items():
                entry = name + ":" + str(number)
                entries.append(entry)
            return "\n".join(entries)
        elif request.startswith("GET"):
            name_list = request.split(" ")
            name = name_list[1]
            number = self.telefonbuch.get(name)
            if number:
                return f"{name}: {number}\n"
            else:
                return f"{name} not found\n"

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        self._logger.info("Server is now listening")
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                self._logger.info(f"Accepted connection from {address}")
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    response = self.handle_request(data.decode('utf-8'))
                    connection.send(response.encode('utf-8'))  # return sent data plus an "*"
                    self._logger.info("Sending response")
                connection.close()  # close the connection
                self._logger.info("Closing connection")
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.logger.info("Creating client socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def send_request(self, request):
        """ Call server """
        self.logger.info("Sending request")
        self.sock.send(request.encode('utf-8'))  # send encoded string as data

        data = self.sock.recv(1024)  # receive the response
        response = data.decode('utf-8')
        self.logger.info("Response received")

        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return response

    def GET(self, name):
        self.logger.info("Sending GET request")
        response = self.send_request(f"GET {name}")
        print(response)
        return response
    
    def GETALL(self):
        self.logger.info("Sending GETALL request")
        response = self.send_request("GETALL")
        print(response)
        return response

    def close(self):
        """ Close socket """
        self.sock.close()
