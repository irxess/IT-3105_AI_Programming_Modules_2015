import subprocess
from copy import copy


def testrange(index, h):
    while h[index] > 0.05:
        h[index] -= 0.05
        h[index+1] += 0.05
        # print h[0], h[1], h[2], h[3], h[4], h[5]
        for i in range(3):
            subprocess.call(['python', 'main.py', str(h[0]), str(h[1]), str(h[2]), str(h[3]), str(h[4]), str(h[5])])
        if index+2<len(h):
            testrange(index+1, copy(h))


def test(index, h):
    h[index] -= 0.05
    h[index+1] += 0.05
    # print h[0], h[1], h[2], h[3], h[4], h[5]
    for i in range(3):
        subprocess.call(['python', 'main.py', str(h[0]), str(h[1]), str(h[2]), str(h[3]), str(h[4]), str(h[5])])
    if index+2<len(h):
        testrange(index+1, copy(h))


l = [0.30, 0.0, 0.2, 0.2, 0.15, 0.15]
test(0, l)
