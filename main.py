import sys

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Error: no input file specified', file=sys.stderr)
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            print(line)
