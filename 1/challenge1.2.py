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
 last_replace_str = s
 for n, d in numMap.items():
     s = s.replace(n,n+d+n)
 return s

def pl(l): n=[c for c in word_digits_to_digits(l) if c.isdigit()];return int(n[0]+n[-1])
a=sys.argv
if __name__=="__main__":
 if len(a)>1:
  with open(a[1],'r') as f:
   s=f.readlines()
 else:
  s=sys.stdin.readlines()
 #for l in s:
 # l = l.strip()
 # print(f"{pl(l)} line: {l}, replacement: {word_digits_to_digits(l)}")
 print(t.reduce(lambda a,b:a+b,[pl(l) for l in s]))
