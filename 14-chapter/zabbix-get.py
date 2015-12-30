#!/usr/bin/python

import socket
import optparse
import sys
import struct


class ZBXDProtocol():
    MAX_KEY_LENGTH = 65536
    HEADER = b'ZBXD\1'
    HEADER_LENGTH = 5
    EXPECTED_LENGTH_SIZE = 8
    RESPONSE_FORMAT = "<5sq{data_length}s"

    def receive_value(self, client):
        """
        Receives key and returns it

        Expects to receive header followed by the length of the key
        followed by the key.
        """
        received = client.recv(self.HEADER_LENGTH)
        if received == self.HEADER:
            expected_length = struct.unpack(
                'q', client.recv(self.EXPECTED_LENGTH_SIZE)
            )[0]
            key = client.recv(expected_length)
        else:
            if '\n' in received:
                key = received
            else:
                key = received + client.recv(self.MAX_KEY_LENGTH)
        return key.decode('utf-8')

    def send_value(self, client, value):
        """
        Formats value according to protocol and sends it to client
        """
        message = self._calculate_message(value)
        client.sendall(message)

    def _calculate_message(self, value):
        formatted_value = self._format(value)
        data_length = len(formatted_value)
        response = struct.pack(
            self.RESPONSE_FORMAT.format(data_length=data_length),
            self.HEADER,
            data_length,
            formatted_value
        )
        return response

    def _format(self, value):
        if isinstance(value, float):
            formatted_value = '{0:.4f}'.format(value)
        else:
            formatted_value = str(value)
        return formatted_value


option_parser = optparse.OptionParser()
option_parser.add_option('-s', '--host', default='127.0.0.1',
                         help='host name or IP address of a host')
option_parser.add_option('-p', '--port', type=int, default=10052,
                         help='port number of agent running on the host')
option_parser.add_option('-t', '--timeout', type=float, default=1.0,
                         help='socket timeout')

options, arguments = option_parser.parse_args()

if len(arguments) == 0:
    print("You must provide key")
    sys.exit()

key = arguments[0]

client_socket = None
try:
    client_socket = socket.create_connection((options.host, options.port),
                                             options.timeout)

    protocol = ZBXDProtocol()
    protocol.send_value(client_socket, key)

    print(protocol.receive_value(client_socket))
except Exception as e:
    print("Unable to receive data from agent: {0}".format(e))

finally:
    if client_socket is not None:
        client_socket.close()
