import os
import tempfile
from io import TextIOBase


class File:
    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, 'w'): pass
        self.f: TextIOBase = None

    def __iter__(self):
        self.f = open(self.filepath)
        return self

    def __next__(self):
        try:
            return self.f.__next__()
        except:
            self.f.close()
            raise StopIteration

    def __add__(self, other):
        _, newpath = tempfile.mkstemp(dir=tempfile.gettempdir(), text=True)
        res = File(newpath)
        res.write(self.read() + other.read())
        return res

    def __str__(self):
        return os.path.abspath(self.filepath)

    def write(self, content: str):
        with open(self.filepath, 'w') as f:
            f.write(content)

    def read(self):
        with open(self.filepath, 'r') as f:
            return f.read()


if __name__ == '__main__':
    path_to_file = 'some_filename'
    print(os.path.exists(path_to_file))
    # False
    file_obj = File(path_to_file)
    print(os.path.exists(path_to_file))
    # True
    print(file_obj.read())
    # ''
    file_obj.write('some text')
    # 9
    print(file_obj.read())
    'some text'
    file_obj.write('other text')
    # 10
    print(file_obj.read())
    # 'other text'
    file_obj_1 = File(path_to_file + '_1')
    file_obj_2 = File(path_to_file + '_2')
    file_obj_1.write('line 1\n')
    # 7
    file_obj_2.write('line 2\n')
    # 7
    new_file_obj = file_obj_1 + file_obj_2
    print(isinstance(new_file_obj, File))
    # True
    print(new_file_obj)
    # C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
    for line in new_file_obj:
        print(ascii(line))
    # 'line 1\n'
    # 'line 2\n'
