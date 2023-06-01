#!/usr/bin/env python3.6
import asyncio
from threading import Lock
import sys
import types

d = {}
mutex = Lock()

class ServerError(Exception):
    pass


def process_data(d: dict, s: str):
    error_msg = 'error\nwrong command\n\n'
    try:
        """
        request: <команда> <данные запроса><\n>
            put palm.cpu 23.7 1150864247\n
            get palm.cpu\n
            get *\n            

            В случаях:
                - когда в запросе на получение данных передан не существующий ключ
                - успешного выполнения команды сохранения данных put
                        ok\n\n
        response: <статус ответа><\n><данные ответа><\n\n>
            <статус ответа>: 'ok' | 'error'

            ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\n\n
        """
        i = s.index(' ')
        cmd = s[:i]
        if cmd not in ['get', 'put'] or s[-1] != '\n':
            raise Exception
        data = s[i + 1:-1]

        r = data.split(' ')
        metric = r[0]
        if cmd == 'get':
            if len(r) != 1:
                raise Exception

            res = 'ok'
            if metric == '*':
                for m, y in d.items():
                    for k, v in y.items():
                        res += f'\n{m} {v} {k}'
            elif d.get(metric):
                for k, v in d[metric].items():
                    res += f'\n{metric} {v} {k}'
            res += '\n\n'
            return res
        elif cmd == 'put':
            if len(r) != 3:
                raise Exception
            value = float(r[1])
            ts = int(r[2])

            if d.get(metric) == None:
                d[metric] = {}

            d[metric][ts] = value

            return 'ok\n\n'
        else:
            raise Exception
    except:
        return error_msg


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        mutex.acquire()
        resp = process_data(d, data.decode())
        mutex.release()
        self.transport.write(resp.encode())


def t2(host, port):
    d = {}
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


async def t3_aux(host, port):
    d = {}
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ClientServerProtocol,
        host, port)

    async with server:
        await server.serve_forever()


def run(host, port):
    d = {}
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    # print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


def t4(host, port):
    run(host, port)


def t3(host, port):
    asyncio.run(t3_aux(host, port))


def run_server(host, port):
    t4(host, port)


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
