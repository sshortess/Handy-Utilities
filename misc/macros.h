/*
  macros.h

  handy macros

   no error or type checking done  -- be forwarned.

 */

#define BIT(b) ((1) << (b))   // return bit set

#define ABS(a) (((a) < 0) ? -(a) : (a))   // absolute value
#define MIN(x,y) (((x) < (y)) ? (x) : (y))   // minimum
#define MAX(x,y) (((x) > (y)) ? (x) : (y))   // maximum
#define CLAMP(n,low,high) (((x) > (high)) ? (high) : (((x) < (low)) ? (low) : (x)))    // limit between low and high
#define BOUND(n,low,high) (((x) > (high)) ? (high) : (((x) < (low)) ? (low) : (x)))    // limit between low and high


