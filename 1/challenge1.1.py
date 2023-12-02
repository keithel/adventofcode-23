import sys
import functools as t
def pl(l): n=[c for c in l if c.isdigit()];return int(n[0]+n[-1])
a=sys.argv
print(t.reduce(lambda a,b:a+b,[pl(l) for l in sys.stdin.readlines()]))
