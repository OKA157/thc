import sys

def T (missed, detected, r):
    total = missed + detected
    p_missed = 1 / r
    p_detected = 1 - p_missed
    Npm = total * p_missed
    Npd = total * p_detected
    return ((missed - Npm) ** 2) / Npm + ((detected - Npd) ** 2) / Npd

with open(sys.argv[1], 'r') as f:
    d = [l.strip().split(' ') for l in f.readlines()]

print(sys.argv[1] + ':')

for l in d:
    print('T' + l[1] + ' = ' + str(T(int(l[7]), int(l[9]), int(l[3]))))
