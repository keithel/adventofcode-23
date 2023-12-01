import sys
import functools as t
def pl(l): n=[c for c in l if c.isdigit()];return int(n[0]+n[-1])
a=sys.argv
if __name__=="__main__":
 if len(a)>1:
  with open(a[1],'r') as f:
   s=f.readlines()
 else:
  s=sys.stdin.readlines()
 print(t.reduce(lambda a,b:a+b,[pl(l) for l in s]))
