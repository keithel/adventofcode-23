import sys
import functools as t
def word_digits_to_digits(s):
 numMap = {
  "zero":"0",
  "one":"1",
  "two":"2",
  "three":"3",
  "four":"4",
  "five":"5",
  "six":"6",
  "seven":"7",
  "eight":"8",
  "nine":"9"
 }
 for n, s in numMap.items():
     s = s.replace(n,s)
 return s

def pl(l): n=[c for c in word_digits_to_digits(l) if c.isdigit()];return int(n[0]+n[-1])
a=sys.argv
if __name__=="__main__":
 if len(a)>1:
  with open(a[1],'r') as f:
   s=f.readlines()
 else:
  s=sys.stdin.readlines()
 print(t.reduce(lambda a,b:a+b,[pl(l) for l in s]))
