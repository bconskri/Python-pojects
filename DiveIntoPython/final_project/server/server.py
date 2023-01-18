"""Как обычно, вам необходимо разработать программу в одном файле-модуле, который вы загрузите на проверку обычным
способом. Сервер должен соответствовать протоколу, который был описан в задании к предыдущей неделе. Он должен уметь
принимать от клиентов команды put и get, разбирать их, и формировать ответ согласно протоколу. По запросу put
требуется сохранять метрики в структурах данных в памяти процесса. По запросу get сервер обязан отдавать данные в
правильной последовательности. При работе с клиентом сервер должен поддерживать сессии, соединение с клиентом между
запросами не должно "разрываться".

На верхнем уровне вашего модуля должна быть объявлена функция run_server(host, port) — она принимает адрес и порт,
на которых должен быть запущен сервер.

Для проверки правильности решения мы воспользуемся своей реализацией клиента и будем отправлять на ваш сервер put и
get запросы, ожидая в ответ правильные данные от сервера (согласно объявленному протоколу). Все запросы будут
выполняться с таймаутом — сервер должен отвечать за приемлемое время.

Сервер должен быть готов к неправильным командам со стороны клиента и отдавать клиенту ошибку в формате, оговоренном
в протоколе. В этих случаях работа сервера не должна завершаться аварийно. """
import asyncio

class ProcessDataError(Exception):
    pass

class ClientServerProtocol(asyncio.Protocol):

    _storage = {}

    def __init__(self):
        self._recieve = b''
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, data):

        method = ''
        for command in data.split("\n"):
            if not command:
                continue

            try:
                method, params = command.strip().split(" ", 1)
                if method == "put":
                    if len(params.split()) > 3:
                        raise ProcessDataError("wrong command")

                    key, value, timestamp = params.split()

                elif method == "get":
                    if len(params.split()) >=2:
                        raise ProcessDataError("wrong command")

                    key = params
                else:
                    raise ValueError("error")
            except ValueError:
                raise ProcessDataError("wrong command")

        if method == "put":
            if key not in self._storage:
                self._storage[key] = {}
            try:
                self._storage[key][int(timestamp)] = float(value)
            except:
                raise ProcessDataError("wrong command")

        elif method == "get":
            responses = {}
            if key != "*":
                responses = {
                    key: self._storage.get(key, {})
                }
            else:
                for key, timestamp_data in self._storage.items():
                    responses[key] = timestamp_data

            rows = []

            for key, values in responses.items():
                if values:
                    for timestamp, value in values.items():
                        rows.append(f"{key} {value} {timestamp}")

            if rows:
                return "ok\n" + "\n".join(rows) + "\n\n"
            else:
                return "ok\n\n"

        else:
            raise ProcessDataError("wrong command")

        return 'ok\n\n'

    def data_received(self, data):

        self._recieve += data
        try:
            data_decode = self._recieve.decode()
        except UnicodeDecodeError:
            print('UnicodeDecodeError\n\n');
            return

        if not data_decode.endswith('\n'):
            return

        self._recieve = b''

        try:
            resp = self.process_data(data_decode)
        except ProcessDataError as err:
            self.transport.write(f"error\n{err}\n\n".encode())
            return

        self.transport.write(resp.encode())

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    # запуск сервера для тестирования
    run_server('127.0.0.1', 8888)
