import sys

filename = sys.argv[1]
file = open(filename)
lines = len(file.readlines())
print lines
