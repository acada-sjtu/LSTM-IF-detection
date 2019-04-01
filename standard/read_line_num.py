import sys
CYCLE = 50

filename = sys.argv[1]
file = open(filename)
lines = len(file.readlines())
print '# of lines:', lines
print '# of cycles:', CYCLE
print '# of samples:', int(lines / CYCLE)
