encodings = ('utf8', 'gb18030', 'latin1', 'gbk')


class grace_open:

    def __init__(self, filename):
        self.filename = filename

    def write(self, string: str):
        for encoding in encodings:
            try:
                with open(self.filename, 'w', encoding=encoding) as f:
                    f.write(string)
                return self
            except UnicodeEncodeError:
                continue
        raise UnicodeEncodeError

    def read(self):
        for encoding in encodings:
            try:
                with open(self.filename, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeEncodeError:
                continue
        raise UnicodeEncodeError
