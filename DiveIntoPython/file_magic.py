"""

"""
import os.path
import uuid
import tempfile


class File:
    def __init__(self, path):
        self.path = path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def write(self, content):
        with open(self.path, 'w') as f:
            return f.write(content)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def __add__(self, obj):
        new_file = File(os.path.join(tempfile.gettempdir(), str(uuid.uuid4())))
        new_file.write(self.read() + obj.read())

        return new_file

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)

            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration('EOF')

            self.current_position = f.tell()

            return line


def main():


     path_to_file = 'some_filename'

     file_obj = File(path_to_file)
     os.path.exists(path_to_file)

     print(file_obj)

     file_obj.read()

     file_obj.write('some text')

     file_obj.read()

     file_obj.write('other text')

     file_obj.read()

     file_obj_1 = File(path_to_file + '_1')
     file_obj_2 = File(path_to_file + '_2')
     file_obj_1.write('line 1\n')

     file_obj_2.write('line 2\n')

     new_file_obj = file_obj_1 + file_obj_2
     isinstance(new_file_obj, File)

     print(new_file_obj)

     for line in new_file_obj:
        print(ascii(line))

     new_path_to_file = str(new_file_obj)
     os.path.exists(new_path_to_file)

     file_obj_3 = File(new_path_to_file)
     print(file_obj_3)

    


if __name__ == "__main__":
    main()
