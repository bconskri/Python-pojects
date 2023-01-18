"""

"""
class FileReader():
    """

    """
    def __init__(self, file_to_open):
        """
        :type file_to_open: str
        """
        self._file_to_open = file_to_open

    def read(self):
        try:
            with open(self._file_to_open) as f:
                data = f.read()
                return data
        except FileNotFoundError:
            return ''

def main():
    reader = FileReader('not_exist_file.txt')
    print(reader.read())


if __name__ == "__main__":
    main()
