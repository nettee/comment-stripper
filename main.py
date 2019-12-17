import sys
from enum import Enum, auto

class FileReader:
    def __init__(self, f):
        self.f = f
        self.next = self._read1()
        self.next2 = self._read1()

    def _read1(self):
        c = self.f.read(1)
        return c

    def eof(self):
        return self.next == '' and self.next2 == ''

    def get(self):
        return self.next

    def get2(self):
        return self.next2

    def consume(self):
        self.next = self.next2
        self.next2 = self._read1()

    def print(self):
        print(self.next, end='')
        self.consume()

    def ignore(self):
        replaced = '\n' if self.next == '\n' else ' '
        print(replaced, end='')
        self.consume()

    def ignore2(self):
        self.ignore()
        self.ignore()

class State(Enum):
    NORMAL = auto()
    IN_LINE_COMMENT = auto()
    IN_MULTI_LINE_COMMENT = auto()
    IN_STRING = auto()

def strip_comment(source):
    state = State.NORMAL
    while not source.eof():
        c = source.get()

        if state == State.IN_LINE_COMMENT:
            if c == '\n':
                state = State.NORMAL
                source.ignore()
            else:
                source.ignore()

        elif state == State.IN_MULTI_LINE_COMMENT:
            if c == '*':
                c2 = source.get2()
                if c2 == '/':
                    state = State.NORMAL
                    source.ignore2()
                else:
                    source.ignore()
            else:
                source.ignore()

        elif state == State.NORMAL:
            if c == '/':
                c2 = source.get2()
                if c2 == '/':
                    state = State.IN_LINE_COMMENT
                    source.ignore2()
                elif c2 == '*':
                    state = State.IN_MULTI_LINE_COMMENT
                    source.ignore2()
                else:
                    source.print()
            else:
                source.print()

        else:
            raise RuntimeError('Illegal state: ' + str(state))


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Error: no input file specified', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        strip_comment(FileReader(f))