proc iml; *Proc IML, A calculator?;

/* Assigns a matrix below.*/
x=5+2;
Print x;
quit;


proc iml; *Proc IML lets you define a matrix;

/* Assigns a matrix below.*/
A={1 2, 3 4, 5 6};
Print A;

/* You can make it easier to see matrix structure in your code*/

A={11 12,
   21 22,
   31 32};
Print A;


proc iml; *Proc IML lets you do matrix algebra;

/* Assigns a matrix below.*/
A={1 2, 3 4, 5 6};
Print A;

 /* Transpose Below.
   The ` is in the upper left hand corner of the keyboard not on the right. */
tranA = A`;

Print A tranA;
quit;

proc iml; *Diagonal of a matrix;
x={1 3 4,2 5 3,1 2 2};
dx=diag(x);
print dx;

dx=diag({10,50,20});
print dx;

quit;


proc iml; *Shows Identity matrix short cut;

I3x3 = I(3);
I5x5 = I(5);

print I3x3 I5x5;

quit;

proc iml; * Shows J matrix shortcut;

j3 = j(3,1,1);
print j3;

j3x3=j(3,3,1);
print j3x3;

* You can do sums of vectors using a j matrix;

a = {1, 2, 3};

aTj = a`*j3 ;* Notice order of multiplication doesn't change the result for getting sum;
jTa = j3`*a ;* Generally with matrix multiplication it DOES matter;
print a j3 aTj jTa;
quit;


proc iml; * Shows 0 matrix shortcut;

zero3 = j(3,1,0);
print zero3;

zero3x3=j(3,3,0);
print zero3x3;

quit;

/*************************************************************
Class 2 Starts Here
*************************************************************/

proc iml; *addition and subtraction;
A={1 4,   2 5,   3 6};
B={6 5,   4 3,   2 1};
C=A + B;
print A B C;

A_check = C - B;
print A B C A_check;
quit;

*Multiplication does not work;
proc iml;
A={1 4,   2 5,   3 6};
B={6 5,   4 3,   2 1};
C=A*B;
print A B C;
quit;


proc iml; *Multiplication does work;
A={1 4,
   2 5,
   3 6};
transA=A`;
B={6 5,
   4 3,
   2 1};
C=transA*B;
print transA, B, C;
quit;


proc iml; *Multiplication does work;
A={1 2,
   3 4,
   5 6};
B={7 8 9,
   11 12 14};
C=A*B;
print A, B, C;
quit;

proc iml; *Multiplication;
A={1 4, 2 5, 3 6};
B={3 2 1, 6 5 4};
AB=A*B;
BA=B*A;
print A, B, AB, BA;
C={11 12 13, 9 8 7};
dist1=A*(B+C);
dist2=A*B+A*C;
print dist1, dist2;
quit;

proc iml; *Multiplication;
A={1 4, 2 5, 3 6};
B={3 2 1, 6 5 4};
AB=A*B;
print A, B, AB;

/* Notice that we get an error if the matrices are not conformable.
   Look in the .log file to see what happens if the # columns in A is
   not equal to the # of rows in B. Notice that for this next example
   AB is not conformable but BA is conformable.*/

AB=A*B;
A={1 4 1, 2 5 1, 3 6 1};
B={3 2 1, 6 5 4};
AB_bad=A*B;
BA_good=B*A;
print A B BA_good;
quit;

proc iml; *Shows that you can get a sum with j matrix;
a = {1, 2, 3};
j = {1, 1, 1};
aTj = a`*j ;* Notice order of multiplication doesn't change the result for getting sum;
jTa = j`*a ;* Generally with matrix multiplication it DOES matter;
print a j aTj jTa;
quit;

Proc iml; *Rank; 
A={1 1 -3 4,
   2 5  1 13,
   1 3  2 11,
   11 13  15 9};
rank_A=round(trace(ginv(A)*A)); 
print rank_A; 
B={1 2 3 2,
   2 3 5 6,
   4 6 10 12,
   3 4 5 10};
rank_B=round(trace(ginv(B)*B)); 
print rank_B; 
quit;

proc iml; *Shows that you can get a sum with j matrix;
a = {1, 2, 3};
j = {1, 1, 1};
aTj = a`*j ;* Notice order of multiplication doesn't change the result for getting sum;
jTa = j`*a ;* Generally with matrix multiplication it DOES matter;
print a j aTj jTa;
quit;

proc iml; *Inverse Matrix;
A={1 1 -3,
   2 5  1,
   1 3  2};
inverse_A=inv(A);
I1=A*inverse_A; *Shows that A*inv(A) equals I;
I2=inverse_A*A; *Shows that inv(A)*A equals I;
print inverse_A, I1, I2;
quit;

proc iml; *Determinants of a matrix;
x={1 3 4,2 5 3,1 2 2};
y={6 8, -7 9};
determinantx_notpos=det(x);
determinanty_pos=det(y);
print x, determinantx_notpos, y, determinanty_pos;
quit;

proc iml; *Trace of a matrix;
x={1 3 4,2 5 3,1 2 2};
trace=trace(x);
print trace;

A={1 2, 3 1}; *notice the result below is the square of all elements;
traceAtA = trace(A`*A);
AtA = A`*A;
print A, AtA, traceAtA;
quit;

proc iml; *normalized vector;
x={1,5};
xtx=x`*x;
sqrt_xtx=(xtx)**.5;
print xtx, sqrt_xtx; 
norm_x=(1/sqrt_xtx)*x; *c;
Sum_sq=norm_x`*norm_x;
print norm_x, sum_sq;
quit;

*Vector Plot Code to demo orthogonal vectors;
data vector; 
input x y;
cards;
.96 -.28
.28 .96
; 

ods graphics on / width=5in height=5in;
proc sgplot data=vector;
title 'Example of Orthogonal';
vector x=x y=y/LINEATTRS= (thickness=2 color=red);
xaxis min=-.5 max=1;
yaxis min=-.5 max=1;
run; 
ods graphics close;
