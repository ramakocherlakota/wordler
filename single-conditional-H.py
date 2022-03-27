# do somthing like;
# grep '|thane|' scores.txt | cut -d '|' -f 3 | sort | uniq -c | python3 single-conditional-H.py
# returns 5.69 bits of entropy (expected value after a guess of thane)

from math import log
import sys

sum = 0
sumH = 0

for line in sys.stdin.readlines():
    numstr = line.split()[0]
    num = int(numstr)
    sum = sum + num
    sumH = sumH + num * log(num) / log(2)

print(sumH / sum)
