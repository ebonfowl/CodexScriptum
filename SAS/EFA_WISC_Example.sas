
/** Wechsler Intelligence Scale for Children (WISC) **/
data wisc;
input client agemate info comp arith simil vocab digit pictcomp parang block object coding;
   label
       info     = 'Information'
       comp     = 'Comprehension'
       arith    = 'Arithmetic'
       simil    = 'Similarities'
       vocab    = 'Vocabulary'
       digit    = 'Digit Span'
       pictcomp = 'Picture Completion'
       parang   = 'Paragraph Arrangement'
       block    = 'Block Design'
       object   = 'Object Assembly'
       coding   = 'Coding';
datalines;
   3.000   3.000   8.000   7.000  13.000   9.000  12.000   9.000   6.000  11.000 12.000   7.000   9.000
   4.000   3.000   9.000   6.000   8.000   7.000  11.000  12.000   6.000   8.000  7.000  12.000  14.000
   5.000   3.000  13.000  18.000  11.000  16.000  15.000   6.000  18.000   8.000  11.000  12.000   9.000
   6.000   3.000   8.000  11.000   6.000  12.000   9.000   7.000  13.000   4.000   7.000  12.000  11.000
   7.000   2.000  10.000   3.000   8.000   9.000  12.000   9.000   7.000   7.000  11.000   4.000  10.000
   8.000   3.000  11.000   7.000  15.000  12.000  10.000  12.000   6.000  12.000  10.000   5.000  10.000
   9.000   3.000   6.000  13.000   7.000   8.000  11.000   6.000  14.000   9.000  14.000  14.000  10.000
  10.000   2.000   7.000  10.000  10.000  15.000  10.000   7.000   8.000  14.000  11.000  10.000  12.000
  12.000   3.000  10.000   8.000   8.000  14.000   9.000   9.000  10.000  11.000  10.000   9.000   6.000
  13.000   3.000   9.000  10.000   8.000  11.000   9.000  11.000  10.000  12.000   9.000  13.000  13.000
  14.000   3.000  11.000  15.000  13.000  14.000  12.000   7.000  15.000  12.000  10.000  10.000   4.000
  15.000   3.000  12.000  11.000   8.000  11.000  13.000  13.000  14.000   7.000  11.000   9.000  10.000
  16.000   2.000   8.000  12.000  12.000  15.000  13.000  13.000  14.000  17.000   9.000  12.000   7.000
  17.000   0.000   9.000   5.000   7.000  11.000  13.000   7.000  13.000  10.000  15.000  15.000  11.000
  18.000   3.000   9.000  15.000   8.000  15.000  13.000   8.000  11.000  13.000  11.000  11.000   7.000
  19.000   1.000  12.000  11.000   9.000  17.000  17.000   7.000  17.000  12.000  11.000  11.000   5.000
  20.000   2.000  12.000  10.000  12.000  12.000  12.000  12.000   7.000   7.000  10.000  14.000   8.000
  21.000   1.000   5.000   6.000   5.000   8.000   6.000   5.000  11.000   8.000  10.000  11.000   5.000
  22.000   2.000  12.000  12.000   9.000  14.000  13.000   8.000   6.000   7.000  11.000  11.000  12.000
  24.000   2.000  11.000  10.000   9.000  10.000   8.000   8.000   9.000   7.000  12.000   6.000   2.000
  25.000   3.000   7.000   6.000   8.000   9.000   8.000  12.000   7.000  10.000   9.000   8.000   7.000
  26.000   2.000  10.000   6.000   5.000  10.000   6.000   9.000  10.000  10.000   8.000  16.000  12.000
  27.000   2.000   9.000   7.000   8.000  14.000  12.000  12.000   6.000  12.000   8.000   8.000  14.000
  28.000   1.000   7.000   8.000   7.000   7.000   8.000   5.000   8.000   5.000   9.000  12.000   8.000
  29.000   3.000  12.000  13.000  12.000  11.000  15.000   9.000  11.000  11.000  11.000  14.000  15.000
  31.000   1.000   8.000   6.000   7.000   5.000   6.000   8.000   6.000   7.000   6.000   5.000  11.000
  33.000   3.000  13.000  16.000  10.000  15.000  14.000   5.000  10.000   9.000  13.000  14.000  10.000
  34.000   3.000   8.000   6.000   6.000   5.000   7.000   7.000  10.000   6.000   9.000   5.000  11.000
  35.000   0.000   8.000   4.000   8.000  13.000  10.000   7.000   9.000   8.000   4.000  11.000   5.000
  36.000   0.000  10.000  15.000  10.000  12.000  10.000  15.000   9.000  12.000   7.000  11.000  10.000
  38.000   3.000  10.000  10.000  10.000  12.000  13.000  14.000  14.000  15.000  12.000   9.000   6.000
  39.000   2.000   9.000  13.000  10.000  14.000  13.000  12.000  10.000   9.000  13.000  12.000  15.000
  40.000   3.000  13.000   9.000  11.000  12.000  11.000   8.000  11.000   9.000  11.000  11.000   7.000
  41.000   2.000  12.000   9.000   6.000  12.000  12.000   7.000  10.000   9.000   9.000  13.000   9.000
  42.000   3.000   8.000  10.000   9.000  11.000   8.000  11.000   8.000   6.000  12.000  11.000   4.000
  43.000   1.000  10.000   7.000  10.000   5.000  12.000  14.000  10.000   9.000   3.000   3.000  10.000
  44.000   3.000  11.000   9.000   8.000  11.000  12.000   6.000  10.000   5.000  11.000   8.000   8.000
  45.000   1.000  15.000   6.000  11.000  10.000  16.000   8.000  12.000  10.000  11.000  13.000  14.000
  47.000   2.000   9.000  11.000   9.000  12.000  10.000   8.000   7.000   7.000   6.000   8.000  11.000
  48.000   3.000  10.000  10.000  10.000  12.000  10.000   9.000  13.000  13.000  12.000  10.000  10.000
  51.000   2.000   5.000   8.000   6.000   8.000   7.000   8.000   8.000  10.000  10.000   9.000   5.000
  52.000   1.000   8.000  11.000   8.000   7.000   5.000   6.000  14.000  10.000   5.000   8.000   8.000
  54.000   3.000   5.000   8.000   6.000   3.000  11.000   9.000  10.000   5.000  10.000   9.000   5.000
  55.000   2.000   9.000  11.000   8.000  13.000  10.000   9.000   7.000  13.000  15.000  12.000  12.000
  56.000   2.000  13.000  14.000   6.000  12.000  16.000  16.000  17.000  10.000  10.000  14.000   6.000
  57.000   3.000  10.000  10.000  11.000  12.000   8.000   8.000  10.000  12.000  11.000   6.000  10.000
  59.000   2.000  14.000  14.000  10.000  10.000  15.000  10.000  14.000  15.000  14.000  12.000   8.000
  60.000   2.000   8.000  11.000   6.000  14.000  13.000   7.000   9.000  14.000  12.000   8.000   9.000
  64.000   3.000  11.000   8.000   5.000  11.000   8.000   5.000  12.000  10.000   5.000  13.000   5.000
  65.000   3.000  10.000   8.000   9.000  13.000  12.000   4.000  12.000   9.000  11.000  12.000   7.000
  66.000   3.000   9.000   8.000   5.000   8.000  10.000   7.000   7.000   5.000   7.000   8.000   4.000
  67.000   2.000   7.000   5.000   6.000  10.000   8.000   7.000  11.000  12.000  12.000  14.000   9.000
  68.000   1.000   7.000  10.000  11.000  10.000   9.000   8.000   8.000   7.000   7.000   6.000   9.000
  69.000   3.000   5.000   7.000   6.000  10.000   9.000   7.000   7.000   9.000   9.000  10.000   5.000
  70.000   0.000  10.000  11.000   8.000   8.000  10.000   7.000   8.000   5.000   9.000  15.000  11.000
  73.000   1.000   9.000   9.000   6.000   6.000  12.000   7.000   9.000  10.000  10.000   8.000   6.000
  74.000   0.000   8.000  15.000   9.000   9.000  11.000   8.000  10.000   9.000  11.000   7.000  12.000
  75.000   2.000  10.000  12.000  11.000  13.000  10.000   7.000  11.000  11.000  11.000  12.000   0.000
  76.000   2.000  13.000  14.000  11.000  15.000  17.000   7.000  11.000  16.000  15.000  11.000   9.000
  78.000   3.000   8.000   9.000   9.000   8.000  10.000  10.000   7.000   7.000   6.000   8.000   8.000
  79.000   3.000  10.000   9.000  10.000  10.000   8.000   9.000   8.000  11.000   8.000  10.000   9.000
  80.000   2.000  17.000  14.000  14.000  14.000  14.000  10.000  10.000  11.000  12.000  12.000  10.000
  82.000   1.000   5.000   6.000  11.000   6.000   8.000   7.000   6.000  10.000   9.000   7.000   8.000
  83.000   2.000   6.000  11.000  11.000  11.000   7.000  10.000  11.000   9.000   6.000  12.000  10.000
  84.000   1.000  10.000  10.000  11.000   8.000  12.000   6.000  13.000  10.000   9.000  12.000  10.000
  85.000   3.000  10.000   7.000  12.000  12.000  17.000   9.000  13.000  12.000   5.000  12.000   7.000
  86.000   2.000  11.000  10.000   6.000  11.000  14.000   9.000  10.000  10.000   9.000  14.000   6.000
  87.000   2.000   9.000  10.000   6.000  11.000  12.000   5.000  11.000  11.000   7.000  13.000   7.000
  90.000   3.000   5.000   7.000   7.000  10.000   8.000   8.000   9.000  11.000  12.000  11.000  12.000
  92.000   2.000  15.000  18.000  11.000  17.000  16.000  14.000  19.000  10.000  17.000  16.000   8.000
  93.000   1.000  12.000  10.000   9.000   6.000  15.000  12.000   9.000   7.000  13.000  11.000  12.000
  95.000   1.000  14.000  15.000  14.000  13.000  13.000   8.000  11.000  15.000  13.000  12.000   6.000
  99.000   2.000  14.000   9.000   9.000  10.000  13.000   8.000   2.000   8.000   2.000   3.000   7.000
 100.000   1.000   9.000   9.000   7.000   7.000   9.000   9.000   9.000   9.000  11.000  14.000  10.000
 101.000   2.000   3.000   8.000   8.000   9.000   8.000   4.000   9.000  10.000   8.000  11.000   3.000
 103.000   2.000  12.000  14.000  10.000   5.000  13.000   8.000   4.000  14.000  12.000  14.000   8.000
 104.000   2.000   9.000  14.000  12.000  10.000  10.000   5.000  11.000   9.000  14.000  16.000   9.000
 105.000   2.000   8.000   8.000   8.000   9.000  11.000   7.000  11.000   5.000   8.000   8.000  12.000
 107.000   1.000  12.000   8.000   9.000   9.000  10.000  11.000  10.000  11.000   8.000   9.000   5.000
 108.000   2.000   5.000   7.000   7.000   6.000   9.000   7.000   7.000  14.000   9.000   8.000  10.000
 109.000   1.000  10.000  10.000  11.000  15.000  12.000  10.000   7.000   9.000   4.000  10.000   4.000
 111.000   1.000  12.000   9.000  13.000  13.000  12.000  11.000  15.000  14.000  16.000  13.000   8.000
 112.000   2.000  13.000  11.000  12.000  10.000  11.000  13.000  11.000  15.000  13.000  10.000  11.000
 113.000   2.000  10.000  13.000  10.000   9.000   9.000  13.000  13.000  10.000  12.000  13.000  11.000
 115.000   3.000  12.000  11.000  14.000  14.000  15.000   9.000  13.000  14.000  16.000  12.000  13.000
 116.000   2.000  13.000  14.000  11.000  12.000  14.000   9.000   9.000  11.000  10.000  13.000   6.000
 117.000   1.000   8.000   8.000   9.000   7.000   9.000   4.000  10.000  10.000  10.000   6.000   6.000
 118.000   3.000   6.000  12.000   7.000   2.000  10.000  12.000   8.000   9.000  10.000   8.000   9.000
 119.000   3.000  12.000  14.000  11.000  18.000  16.000  11.000  13.000  14.000  10.000  13.000   8.000
 120.000   2.000  11.000   9.000   8.000   9.000   8.000   7.000   8.000  15.000  10.000  11.000  11.000
 122.000   2.000  10.000  10.000  11.000   8.000  13.000   6.000  10.000   9.000  11.000   9.000   9.000
 123.000   3.000  13.000  12.000  10.000  15.000  11.000  12.000  13.000  10.000  13.000  12.000   2.000
 127.000   0.000  10.000  14.000  11.000  15.000  14.000  16.000  13.000  11.000  15.000  13.000  12.000
 128.000   1.000   5.000   9.000   8.000  10.000  11.000   8.000  11.000  11.000  12.000  12.000   9.000
 130.000   3.000   4.000  10.000   8.000   9.000  10.000   4.000  10.000  11.000  11.000  13.000   9.000
 131.000   1.000  10.000  13.000  10.000  11.000  12.000   6.000  13.000  11.000  13.000  12.000   8.000
 133.000   1.000  10.000   9.000   8.000  13.000  11.000   8.000  13.000   7.000   7.000  14.000   5.000
 134.000   3.000   5.000   8.000   8.000   8.000   7.000   9.000  12.000   8.000  10.000  10.000   5.000
 136.000   2.000  19.000  13.000  13.000  18.000  19.000  10.000  11.000  13.000  11.000  12.000   4.000
 139.000   1.000   9.000   8.000   9.000   9.000   8.000  11.000  10.000  11.000   8.000  10.000   8.000
 140.000   3.000  10.000   6.000   8.000   7.000   3.000   6.000  10.000  15.000  10.000  17.000   4.000
 142.000   1.000   7.000   9.000   9.000   7.000   9.000   9.000  10.000  11.000   9.000   9.000  12.000
 144.000   2.000  10.000  12.000   8.000  11.000  13.000  10.000  11.000  13.000  13.000  15.000  10.000
 145.000   1.000   5.000   9.000  12.000   8.000  10.000  11.000  12.000   8.000  12.000  11.000   8.000
 146.000   3.000  13.000  14.000  14.000  16.000  10.000  14.000  14.000  12.000  13.000  11.000   9.000
 147.000   1.000   8.000   8.000   8.000  10.000   9.000   8.000  13.000  10.000  10.000  10.000   6.000
 148.000   1.000   5.000  11.000   7.000  12.000  10.000   7.000  13.000  14.000  12.000  14.000  13.000
 149.000   3.000   8.000  10.000  10.000   5.000  11.000   7.000   9.000   9.000   8.000  11.000   5.000
 150.000   2.000   6.000   6.000   8.000   7.000  10.000   8.000   7.000   2.000   3.000   8.000   7.000
 151.000   3.000  11.000  11.000   9.000  15.000  14.000   9.000  12.000   9.000  12.000  14.000  10.000
 154.000   3.000  11.000   9.000   8.000  12.000  14.000   8.000  13.000  10.000  13.000   9.000   6.000
 155.000   2.000   7.000   9.000   6.000   7.000   9.000   9.000  11.000  10.000   9.000  14.000   8.000
 156.000   2.000  12.000  14.000   9.000  14.000  14.000   8.000  12.000  12.000  10.000  10.000   6.000
 157.000   1.000  11.000  10.000  10.000   9.000  10.000   8.000  12.000  11.000  11.000  12.000  12.000
 158.000   1.000   9.000  12.000  11.000  11.000  10.000  11.000  14.000  13.000  12.000  12.000   9.000
 162.000   3.000  10.000  14.000  13.000  15.000  10.000   5.000  14.000  13.000  14.000  12.000  11.000
 163.000   2.000  14.000  14.000   6.000  17.000  12.000  11.000  13.000  15.000  13.000  11.000   4.000
 164.000   1.000   7.000  10.000  10.000  11.000  10.000   9.000  14.000   8.000  10.000  11.000   6.000
 165.000   1.000   8.000   6.000   5.000   9.000   6.000   8.000  10.000  10.000  11.000  10.000   8.000
 166.000   3.000  11.000  12.000   7.000  11.000  11.000   6.000  18.000  12.000   8.000  11.000   5.000
 167.000   1.000   6.000   8.000   8.000  16.000  11.000  11.000  12.000  10.000  10.000  14.000   9.000
 171.000   1.000  11.000   9.000  10.000   7.000   9.000   7.000  13.000   6.000  12.000   9.000  11.000
 173.000   3.000  13.000  16.000  11.000  18.000  13.000   6.000  12.000  11.000  13.000  10.000   6.000
 174.000   1.000  15.000  15.000  12.000  14.000  19.000   7.000  16.000   9.000  14.000  11.000   8.000
 176.000   3.000   7.000   9.000   7.000  11.000  12.000   9.000  14.000  10.000  11.000  13.000   7.000
 177.000   1.000  10.000   9.000   7.000  10.000   9.000   9.000  12.000  11.000   9.000  11.000   6.000
 179.000   1.000   4.000  11.000   7.000   4.000   9.000   0.000   8.000   6.000   8.000   8.000  13.000
 180.000   3.000   9.000   0.000   8.000   9.000   8.000   7.000  10.000  13.000   8.000  10.000  12.000
 181.000   3.000  10.000  10.000  13.000   9.000   9.000   8.000  11.000  11.000  13.000  13.000   7.000
 182.000   3.000   8.000   9.000   8.000   5.000   6.000   4.000   9.000   9.000   9.000   8.000   7.000
 183.000   2.000   7.000   7.000  10.000  11.000   9.000   7.000   8.000   9.000   9.000   8.000   9.000
 184.000   3.000   9.000  12.000  10.000  11.000  12.000  13.000  13.000  13.000  12.000  16.000  12.000
 185.000   3.000   3.000   6.000   6.000  12.000   6.000   7.000   8.000  12.000   6.000  11.000   4.000
 186.000   3.000   8.000  11.000   8.000  12.000  10.000   6.000  10.000   9.000  11.000  17.000   9.000
 187.000   2.000   5.000  11.000   9.000   8.000   9.000   8.000   8.000  10.000  11.000  12.000   9.000
 188.000   1.000   4.000  12.000   5.000   9.000  10.000  12.000  10.000   9.000   8.000  10.000  10.000
 189.000   2.000  14.000  10.000   8.000  11.000  16.000  14.000   4.000  12.000   7.000  10.000  14.000
 190.000   2.000  12.000   6.000  10.000   6.000   7.000  11.000   2.000  11.000  11.000  10.000   5.000
 191.000   2.000   8.000   9.000   8.000  10.000   9.000   8.000   8.000  11.000  11.000  14.000  13.000
 192.000   3.000   8.000   8.000   8.000   6.000   8.000   7.000  14.000  11.000  11.000  11.000   7.000
 193.000   2.000  12.000   9.000   9.000  14.000  11.000   7.000   7.000   8.000   8.000  10.000   7.000
 195.000   3.000   5.000   7.000   6.000   4.000   9.000   6.000  12.000  15.000  14.000  12.000   7.000
 196.000   2.000  10.000  13.000   6.000  15.000  14.000  11.000  12.000  11.000   9.000   7.000  12.000
 197.000   1.000   9.000  10.000   9.000  10.000   9.000   8.000  14.000  15.000   9.000  13.000   9.000
 198.000   3.000  10.000   9.000   8.000  10.000  11.000   7.000  12.000  11.000  12.000  15.000   6.000
 199.000   3.000  10.000  11.000   7.000  10.000  10.000  11.000  10.000  13.000  12.000  12.000   8.000
 201.000   2.000  11.000  10.000   9.000  15.000  13.000  11.000  14.000  12.000  10.000  12.000   5.000
 202.000   3.000   9.000   7.000   9.000   8.000   6.000  10.000   8.000  11.000  10.000  10.000   8.000
 204.000   0.000  10.000  11.000  10.000  11.000  12.000   6.000  12.000  13.000  14.000  15.000   6.000
 205.000   3.000   9.000  10.000   8.000   8.000   9.000  12.000  10.000  11.000   9.000   9.000   7.000
 206.000   3.000   7.000  11.000   7.000  12.000   9.000   9.000  15.000  12.000  15.000  14.000   6.000
 208.000   3.000  12.000  14.000   8.000  12.000   8.000  13.000  11.000  13.000   8.000  13.000  13.000
 209.000   3.000   9.000   7.000   9.000  10.000  11.000   8.000   8.000  10.000  11.000   9.000   9.000
 211.000   1.000  13.000  17.000  14.000  15.000  15.000  14.000  14.000   8.000  10.000  13.000  12.000
 214.000   3.000  15.000  16.000  16.000  14.000  16.000  12.000  11.000  11.000  18.000  18.000  12.000
 215.000   2.000  10.000  10.000   4.000  12.000  11.000   7.000  10.000  10.000  14.000  12.000   6.000
 216.000   1.000   6.000  10.000   7.000   9.000   9.000   8.000  12.000  14.000  15.000  11.000  11.000
 218.000   1.000  13.000  10.000  10.000  12.000  14.000  11.000  10.000  11.000   8.000   9.000  14.000
 220.000   3.000   9.000  12.000   7.000   8.000   9.000   8.000  13.000   6.000   9.000   8.000   7.000
 222.000   3.000   7.000   8.000   9.000  11.000   8.000  10.000  10.000  10.000  11.000  11.000   9.000
 223.000   0.000  12.000  10.000   9.000  11.000  11.000  12.000   9.000   8.000  11.000  16.000   5.000
 225.000   3.000  11.000  11.000   9.000   9.000   9.000   8.000  16.000  14.000  12.000  19.000  12.000
 226.000   2.000   5.000  10.000   7.000   9.000  10.000   5.000  14.000  12.000   9.000  10.000  12.000
 227.000   1.000  11.000   7.000   6.000   9.000   7.000   8.000  14.000  12.000  10.000  13.000  10.000
 228.000   2.000  15.000  12.000  12.000  13.000  12.000   8.000  15.000  14.000  11.000  10.000   6.000
 230.000   1.000   4.000   6.000   9.000   9.000   6.000   6.000  11.000   7.000  11.000   7.000   8.000
 231.000   3.000  13.000  12.000  13.000  17.000  12.000  13.000  15.000  14.000  11.000   9.000  11.000
 232.000   2.000   7.000   7.000   7.000   8.000  12.000   9.000  12.000   9.000  15.000   8.000  12.000
 233.000   1.000   4.000   3.000   9.000   5.000   2.000   3.000   8.000  14.000   8.000   7.000   7.000
 235.000   6.000  14.000  11.000  12.000  12.000  18.000  13.000  12.000  12.000  11.000   8.000   7.000
 237.000   1.000   6.000  11.000   5.000  11.000   8.000   9.000   5.000   9.000   7.000   9.000  10.000
 238.000   3.000  10.000   8.000  11.000  11.000   6.000  12.000  12.000  10.000  10.000   6.000  10.000
 239.000   1.000  10.000  10.000  10.000  10.000   9.000   5.000  10.000  11.000  10.000  13.000   9.000
 240.000   2.000  13.000  12.000  11.000  11.000  12.000  12.000  13.000  11.000  10.000  12.000  12.000
 241.000   2.000   9.000   9.000  10.000   8.000   8.000   9.000  10.000   6.000   6.000   7.000   7.000
;

proc corr data=wisc noprob;
var info vocab simil arith comp digit coding block object pictcomp parang;
run;

proc means data=wisc n min max mean std skew kurt maxdec=3;
var info vocab simil arith comp digit coding block object pictcomp parang;
run;

proc sgscatter data=wisc;
matrix info vocab simil arith comp digit coding block object pictcomp parang / diagonal=(histogram);
run;

/** Unrotated PAF Solution **/
proc factor data=wisc 
  method=prinit  
  nfactors = 2 
  priors = smc msa 
  reorder
  plot=(scree);
var info comp arith simil vocab digit pictcomp parang block object coding;
run;

/*proc princomp data=wisc out=prin cov plots=score plots=pattern;*/
/*  var info comp arith simil vocab digit pictcomp parang block object coding;*/
/*run;*/

/** Compare R^2 value to Prior Communality Estimate (SMC) **/
proc glm data=wisc;
model info=comp arith simil vocab digit pictcomp parang block object coding;
run;
quit;

/** Varimax (Orthogonal) Rotated PAF Solution **/
proc factor data=wisc 
  method=prinit  
  nfactors = 2 
  priors = smc msa 
  rotate=varimax
  reorder
  plot=(scree);
var info comp arith simil vocab digit pictcomp parang block object coding;
run;

/** Promax (Oblique) Rotated PAF Solution **/
proc factor data=wisc 
  method=prinit  
  nfactors = 2 
  priors = smc msa 
  rotate=promax
  reorder
  plot=(scree);
var info comp arith simil vocab digit pictcomp parang block object coding;
run;

/** Plotting Unrotated PAF Solution **/
data plot1;
input item $8. f1 f2 factor factor2;
label f1="Factor 1" f2="Factor 2" factor="Factor";
datalines;
info	0.72166	-0.33922	1	1
vocab	0.71761	-0.24146	1	1
comp	0.70892	0.03008	1	1
simil	0.69687	-0.05032	1	1
arith	0.54241	-0.23191	1	1
block	0.52001	0.38227	1	2
pictcomp	0.50399	0.36154	1	2
parang	0.37784	0.21585	1	2
digit	0.35952	-0.25437	1	1
coding	0.07868	-0.04884	1	1
object	0.41516	0.45848	2	2
;
title;
ods graphics on / attrpriority=none noborder;
proc sgplot data=plot1;
scatter x=f1 y=f2 / group=factor markerattrs=(size=10);
styleattrs datacontrastcolors=(crimson blue) datasymbols=(squarefilled circlefilled);
refline 0 / axis=x label="Factor 2" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=blue); 
refline 0 / axis=y label="Factor 1" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=crimson); 
xaxis min=-1.345 max=1.345 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
yaxis min=-1 max=1 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
/*title "Unrotated EFA Solution";*/
keylegend / title="Factor" titleattrs=(size=12 weight=bold) valueattrs=(size=12);
run;

/** Plotting Rotated PAF Solution (Orthogonal) **/
data plot2;
input item $8. f1 f2 factor;
label f1="Factor 1" f2="Factor 2" factor="Factor";
datalines;
info	0.77325	0.19476	1
vocab	0.70818	0.26784	1
simil	0.57104	0.40257	1
arith	0.56658	0.16423	1
comp	0.52943	0.47242	1
digit	0.43931	0.03098	1
coding	0.09182	0.01206	1
block	0.16013	0.62522	2
object	0.03072	0.61775	2
pictcomp	0.16088	0.59903	2
parang	0.15558	0.40638	2
;
title;
ods graphics on / attrpriority=none noborder;
proc sgplot data=plot2;
scatter x=f1 y=f2 / group=factor markerattrs=(size=10);
styleattrs datacontrastcolors=(crimson blue) datasymbols=(squarefilled circlefilled);
lineparm x=0 y=0 slope=-1.2212 / curvelabel="X-Axis (Rotated)" curvelabelattrs=(size=12 weight=bold) lineattrs=(thickness=1 color=black); 
lineparm x=0 y=0 slope=.8189 / curvelabel="Y-Axis (Rotated)" curvelabelattrs=(size=12 weight=bold) lineattrs=(thickness=1 color=black); 
refline 0 / axis=x label="Factor 2" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=blue);  
refline 0 / axis=y label="Factor 1" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=crimson); 
xaxis min=-1.345 max=1.345 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
yaxis min=-1 max=1 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
keylegend / title="Factor" titleattrs=(size=12 weight=bold) valueattrs=(size=12);
/*title "Rotated (Orthogonal) EFA Solution";*/
run;

/** Plotting Rotated PAF Solution (Oblique) **/
data plot3;
input item $8. f1 f2 factor;
label f1="Factor 1" f2="Factor 2" factor="Factor";
datalines;
info	0.7961	0.38734	1
vocab	0.75588	0.44119	1
arith	0.58976	0.3046	1
simil	0.66535	0.53606	1
digit	0.42845	0.14307	1
comp	0.64655	0.59283	1
coding	0.09122	0.0353	1
object	0.2142	0.60483	2
block	0.33991	0.64537	2
pictcomp	0.33278	0.62026	2
parang	0.27007	0.43274	2
;
title;
ods graphics on / attrpriority=none noborder;
proc sgplot data=plot3;
scatter x=f1 y=f2 / group=factor markerattrs=(size=10);
styleattrs datacontrastcolors=(crimson blue) datasymbols=(circlefilled squarefilled);
/*lineparm x=0 y=0 slope=2.0327 / curvelabel="Y-Axis (Rotated)" curvelabelattrs=(size=12 weight=bold) lineattrs=(thickness=1 color=black); */
lineparm x=0 y=0 slope=-4.042 / curvelabel="Y-Axis (Rotated)" curvelabelattrs=(size=12 weight=bold) lineattrs=(thickness=1 color=black); 
lineparm x=0 y=0 slope=1.044 / curvelabel="X-Axis (Rotated)" curvelabelattrs=(size=12 weight=bold) lineattrs=(thickness=1 color=black); 
refline 0 / axis=x label="Factor 2" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=blue);  
refline 0 / axis=y label="Factor 1" labelattrs=(size=12 weight=bold) lineattrs=(thickness=2 color=crimson); 
xaxis min=-1.345 max=1.345 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
yaxis min=-1 max=1 labelattrs=(size=12 weight=bold) valueattrs=(size=11) display=(nolabel);
keylegend / title="Factor" titleattrs=(size=12 weight=bold) valueattrs=(size=12);
/*title "Rotated (Oblique) EFA Solution";*/
run;