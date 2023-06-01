import argparse
import tempfile
import os
import json

def get_key(k):
    # filename = os.path.join(tempfile.gettempdir(), 'storage.data')
    filename = os.path.join('', 'storage.data')
    if not os.path.exists(filename):
        print('None')
        return
    with open(filename, 'r') as f:
        d = json.load(f)
        if d.get(k) == None:
            print('None')
            return

        l = d[k]
        res = str(l[0])
        for i in range(1, len(l)):
            res += ', ' + str(l[i])
        print(res)

def add_key(k, v):
    # filename = os.path.join(tempfile.gettempdir(), 'storage.data')
    filename = os.path.join('', 'storage.data')
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r+') as f:
        d = {}
        try:
            d = json.load(f)
        except json.JSONDecodeError:
            f.truncate(0)
            json.dump({}, f)
        finally:
            f.seek(0)

        if d.get(k) == None:
            d[k] = []
        d[k].append(v)
        json.dump(d, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='имя ключа')
    parser.add_argument('--val', help='значение')

    args = parser.parse_args()
    if args.val == None:
        get_key(args.key)
    else:
        add_key(args.key, args.val)