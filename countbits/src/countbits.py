#!/usr/bin/env python

"""

Brian Kernighan's method goes through as many iterations as there are set 
bits. So if we have a 32-bit word with only the high bit set, then it will 
only go once through the loop.

Published in 1988, the C Programming Language 2nd Ed. (by Brian W. Kernighan 
and Dennis M. Ritchie) mentions this in exercise 2-9. On April 19, 2006 Don Knuth 
pointed out to him that this method "was first published by Peter Wegner in CACM 3 (1960), 322. 
(Also discovered independently by Derrick Lehmer and published in 1964 in a book edited by Beckenbach.)"

long count_bits(long n) {     
  unsigned int c; // c accumulates the total bits set in v
  for (c = 0; n; c++) 
    n &= n - 1; // clear the least significant bit set
  return c;
}

Shamelessly stolen an implemented in python

"""
import os
import sys

def cnt_bits(v):
   c = 0
   n = int(v,0)
   while (n):
      n &= (n - 1)
      c += 1
   return c

if __name__ == '__main__':
   print cnt_bits(sys.argv[1])
   
      
