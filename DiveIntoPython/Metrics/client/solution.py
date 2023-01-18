"""

"""
import bisect
import socket
import time

class ClientError(Exception):
    pass #TODO

class Client():
    """"""

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as error:
            raise ClientError("create connection error", error)

    def _read_answer(self):

        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as error:
                raise ClientError("receive data error", error)

        if data == 'ok\n\n':
            return ""

        status, answer = data.decode('utf-8').split("\n", 1)

        if status != 'ok':
            raise ClientError('Server returns an error', answer)

        if answer == "":
            return ""

        return answer.strip()

    def put(self, key, value, timestamp=None):

        try:
            timestamp = timestamp or int(time.time())
            self.connection.sendall(
                f"put {key} {value} {timestamp}\n".encode()
            )
        except socket.error as error:
            raise ClientError("send data error", error)

        server_answer = self._read_answer()

        if server_answer != "":
            raise ClientError('server returns error', server_answer)

    def get(self, key):

        try:
            self.connection.sendall(
                f"get {key}\n".encode()
            )
        except socket.error as error:
            raise ClientError("error send data", error)

        server_answer = self._read_answer()

        response = dict()
        if server_answer != "":
            try:
                for row in server_answer.split("\n"):
                    key, value, timestamp = row.split()
                    if key not in response:
                        response[key] = []
                    #response[key].append((int(timestamp), float(value)))
                    bisect.insort(response[key], ((int(timestamp), float(value))))
            except Exception as error:
                raise ClientError('server returns invalid data', error)

        return response

    def close(self):
        try:
            self.connection.close()
        except socket.error as error:
            raise ClientError("error close connection", error)