import time
import socket


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.sock = None
        self.sock = socket.create_connection((host, port), timeout=timeout)

    def get(self, metric_name):
        try:
            code, data = self._send_and_get_res('get', metric_name)
            """
            [ok]\n[{data\n}]\n[]
            ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n
            ok\npalm.cpu 2.0 1150864247\n\n
            ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\n\n
            
            {
              'palm.cpu': [
                (1150864247, 0.5),
                (1150864248, 0.5)
              ]
            }
            """
            res = {}
            if not data:
                return {}

            for record in data.split('\n')[:-1]:
                aba = record.split(' ')
                if len(aba) != 3:
                    raise ClientError

                metric = aba[0]
                dat = float(aba[1])
                timest = int(aba[2])

                if res.get(metric) == None:
                    res[metric] = []
                res[metric].append((timest, dat))

            for key, value in res.items():
                value.sort(key=lambda tup: tup[0])

            return res
        except:
            raise ClientError

    def _send_and_get_res(self, command, request_data):
        request = f'{command} {request_data}\n'
        self.sock.sendall(request.encode('utf8'))

        data = self.sock.recv(4096)
        if not data:
            raise ClientError
        res = data.decode('utf8')
        d = res.index('\n')
        error_code = res[0: d]
        response = res[d + 1:-1]

        if error_code not in ['ok', 'error']:
            raise ClientError

        if error_code != 'ok':
            raise ClientError(response)

        return error_code, response

    def __del__(self):
        if self.sock:
            self.sock.close()

    def put(self, metric_name, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())

        try:
            to_send = f'{metric_name} {value} {timestamp}'
            code, data = self._send_and_get_res('put', to_send)

            # if data:
            #     raise ClientError
        except ConnectionError as err:
            raise ClientError(f"{err.errno}: {err.strerror}")


if __name__ == '__main__':
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))
    print(client.get("non_existing_data"))
