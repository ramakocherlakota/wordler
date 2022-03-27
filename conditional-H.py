# cat answers-and-scores-counts.txt | python condtitioal=H.py

from math import log
import sys

sums = {}
sumHs = {}

for line in sys.stdin.readlines():
    firsts = line.strip().split("|")[0]
    [numstr, word] = firsts.split()
    num = int(numstr)
    if not word in sums:
        sums[word] = 0
        sumHs[word] = 0
    sums[word] = sums[word] + num
    sumHs[word] = sumHs[word] + num * log(num) / log(2)

for word in sums:
    print(f"{word}\t{sumHs[word]/sums[word]}")
