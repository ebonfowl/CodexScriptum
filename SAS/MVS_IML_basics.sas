
proc iml; 
/* Assigns a 3x2 matrix to A.*/
A={1 2, 3 4, 5 6};
Print A;

 /* Transpose: The ` is in the upper left hand corner of the keyboard not on the right. */
transpA = A`; 
 
/*Print A and the transpose of A*/
Print A transpA;
quit;

/*Diagonal of a matrix*/
proc iml; 
x={1 3 4,2 5 3,1 2 2};
dx=diag(x);
print dx;
quit;

/*Create an Identity Matrix*/
Proc iml;
I_3by3=I(3);
print I_3by3;
quit;

/*Example of Useful Commands*/
Proc iml; 
j3=j(3,1,1);
j3by3=j(3,3,1);
/*notice the difference in how thigs are printed*/
print j3 j3by3; 
print j3; 
print j3by3;
quit;



/*Import a .csv file, then "use" it in IML*/
Proc import 
datafile="F:\Survey 2012.csv"
out=survey dbms=csv replace;
getnames=yes; run;

Proc IML;
/*The USE statement opens a SAS data set for reading*/
USE survey;   
/*The READ statement reads observations from the current SAS data set. */
/*Below, I read all the numeric variables into a matrix called X.
I want to make the column names of my matrix the same as the variable names from the
SAS data set*/
READ ALL VAR _NUM_ INTO X[colname=varNames];   
Print X;
Xt=X`;
Print Xt;
quit;

DATA survey2;
INFILE "F:\Survey 2012.csv";
INPUT id item1 - item28;
RUN;

PROC IML;
USE survey2;
READ ALL VAR _NUM_ INTO X2;
print X2; 
quit;
                     

