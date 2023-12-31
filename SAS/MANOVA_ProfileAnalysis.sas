/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*/*/*PROFILE ANALYSIS EXAMPLE;*/*/*/;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
data gui;
infile "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 6 through 8 MANOVA\T6_8_GUINEAPIGS2.txt";
INPUT group animal w1 w3 w4 w5 w6 w7;
run;

* Just to see what we have in our data set;
Proc Print data=gui; 
run;

/*Graph the profiles*/
proc means data=gui noprint;
class group;
var w1 w3 w4 w5 w6 w7;
output out=guim; run;

data guim; set guim (where=(_STAT_='MEAN' and _TYPE_=1)); 
drop _TYPE_ _FREQ_ _STAT_ ;
run;

proc transpose data=guim out=guimt; 
by group;
var w1 w3 w4 w5 w6 w7;
run;
proc print data=guimt; run;

proc sgplot data=guimt;
series x=_NAME_ y=COL1/group=group lineattrs=(thickness=5); run;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

Title 'Regular 1-Way MANOVA';
proc glm data=gui;
CLASS group;
  MODEL w1 w3 w4 w5 w6 w7 = group;
MANOVA H=group/PRINTH PRINTE SHORT;
run; 

*Parallel?;
TITLE 'Profile: Parallel?';
PROC GLM data=gui;
  CLASS group;
  MODEL w1 w3 w4 w5 w6 w7 = group;
  MANOVA H=group m=(1 -1 0 0 0 0, 
					0 1 -1 0 0 0, 
					0 0 1 -1 0 0,
					0 0 0 1 -1 0, 
					0 0 0 0 1 -1) prefix=diff/PRINTE PRINTH ;
RUN;
Quit;

	*Same Height?;
TITLE 'Profile: Height?';
PROC GLM data=gui;
  CLASS group;
  MODEL w1 w3 w4 w5 w6 w7 = group;
  MANOVA H=group m=(1 1 1 1 1 1) prefix=sum/PRINTE PRINTH ;
RUN;
Quit;

*Flat?;
TITLE 'Profile: Flat?';
PROC GLM data=gui;
  CLASS group;
  MODEL w1 w3 w4 w5 w6 w7 = group;
  MANOVA H=intercept
				 m=(1 -1 0 0 0 0, 
					0 1 -1 0 0 0, 
					0 0 1 -1 0 0,
					0 0 0 1 -1 0, 
					0 0 0 0 1 -1) prefix=flat/PRINTE PRINTH ;
RUN;
Quit;

/**/
/*Leisure example*/
/**/

data leisure;
input ID Group $ Read Dance TV Ski;
cards;
1   Bellydancers    7    10  6   5
2   Bellydancers    8     9  5   7
3   Bellydancers    5    10  5   8
4   Bellydancers    6    10  6   8
5   Bellydancers    7     8  7   9
6     Politicians    4     4  4   4
7     Politicians    6     4  5   3
8     Politicians    5     5  5   6
9     Politicians    6     6  6   7
10    Politicians    4     5  6   5
11 Administrators    3     1  1   2
12 Administrators    5     3  1   5
13 Administrators    4     2  2   5
14 Administrators    7     1  2   4
15 Administrators    6     3  3   3
;

proc contents data=leisure; run;

/*Graph the profiles*/
proc means data=leisure noprint;
class group;
var Read Dance TV Ski;
output out=leisurem mean=; 

data leisurem; set leisurem (where=(_TYPE_=1)); 

proc transpose data=leisurem out=leisuret; 
by group;
var Read Dance TV Ski;
run;

/*proc print data=leisuret; run;*/

proc sgplot data=leisuret;
series x=_NAME_ y=COL1/group=group lineattrs=(thickness=5); run;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

Title 'Regular 1-Way MANOVA';
proc glm data=leisure;
CLASS group;
  MODEL Read Dance TV Ski = group;
MANOVA H=group/PRINTH PRINTE;
run; 

*Parallel?;
TITLE 'Profile: Parallel?';
PROC GLM data=leisure;
  CLASS group;
  MODEL Read Dance TV Ski = group;
  MANOVA H=group m=(1 -1 0 0, 
					0 1 -1 0, 
					0 0 1 -1) prefix=diff/PRINTE PRINTH ;
RUN;
Quit;

*Same Height?;
TITLE 'Profile: Height?';
PROC GLM data=leisure;
  CLASS group;
  MODEL Read Dance TV Ski = group;
  MANOVA H=group m=(1 1 1 1) prefix=diff/PRINTE PRINTH ;
RUN;
Quit;

*Flat?;
TITLE 'Profile: Flat?';
PROC GLM data=leisure;
  CLASS group;
  MODEL Read Dance TV Ski = group;
  MANOVA H=intercept m=(1 -1 0 0, 
					0 1 -1 0, 
					0 0 1 -1) prefix=diff/PRINTE PRINTH ;
RUN;
Quit;


/*TEST of additional information*/
Title 'Additional Information';
proc glm data=leisure;
CLASS group;
  MODEL Read TV = group Dance Ski;
MANOVA H=group/PRINTH PRINTE;
run; 

/*Test of equal covariance matrix*/
Title 'Homogeneity test by Box M';
proc discrim data=leisure pool=test;
class group;
var Read Dance TV Ski;
run;

/*proc sort data=leisure; by group;*/
/*proc corr data=leisure CSSCP COV;*/
/*by group;*/
/*var Read Dance TV Ski;*/
/*run;*/




/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*************REVIEW: Climate Data******************/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


PROC IMPORT DATAFILE="C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 6 through 8 MANOVA\climate.xlsx"
OUT=CLIMATE DBMS=XLSX REPLACE;
RUN;

/*Use SAS built in function Proc GLM*/
PROC GLM DATA=CLIMATE;
CLASS GROUP;
MODEL Y1 Y2 Y3=GROUP;
MANOVA H=GROUP/PRINTE PRINTH;
RUN;


/*Use proc iml to program manova*/
data c1; set climate(where=(group=1));
data c2; set climate(where=(group=2));
data c3; set climate(where=(group=3));
data c4; set climate(where=(group=4));
run;

PROC IML;
use climate;
read all var {y1 y2 y3} into X;
N=NROW(X); 
XBAR=1/N*X`*J(N,1);   
xbar_m=repeat(XBAR`,N,1);
S=1/(N-1)*X`*(I(N)-1/N*J(N,1))*X;
T=(X-xbar_m)`*(X-xbar_m);

use c1;
read all var {y1 y2 y3} into X1;
N1=NROW(X1); 
XBAR1=1/N1*X1`*J(N1,1);   
xbar_m1=repeat(XBAR1`,N1,1);
S1=1/(N1-1)*X1`*(I(N1)-1/N1*J(N1,1))*X1;
T1=(X1-xbar_m1)`*(X1-xbar_m1);

use c2;
read all var {y1 y2 y3} into X2;
N2=NROW(X2); 
XBAR2=1/N2*X2`*J(N2,1);   
xbar_m2=repeat(XBAR2`,N2,1);
S2=1/(N2-1)*X2`*(I(N2)-1/N2*J(N2,1))*X2;
T2=(X2-xbar_m2)`*(X2-xbar_m2);

use c3;
read all var {y1 y2 y3} into X3;
N3=NROW(X3); 
XBAR3=1/N3*X3`*J(N3,1);   
xbar_m3=repeat(XBAR3`,N3,1);
S3=1/(N3-1)*X3`*(I(N3)-1/N3*J(N3,1))*X3;
T3=(X3-xbar_m3)`*(X3-xbar_m3);

use c4;
read all var {y1 y2 y3} into X4;
N4=NROW(X4); 
XBAR4=1/N4*X4`*J(N4,1);   
xbar_m4=repeat(XBAR4`,N4,1);
S4=1/(N4-1)*X4`*(I(N4)-1/N4*J(N4,1))*X4;
T4=(X4-xbar_m4)`*(X4-xbar_m4);

E=T1+T2+T3+T4;

H=T-E; 
print T, E, H;

detE=det(E);
detEH=det(E+H);
Wilks=detE/detEH;
print Wilks;

EiH=inv(E)*H;
eval=eigval(EiH)[1,1];
Roy=eval/(1+eval);
print eval, Roy;

Pillai=trace(inv(E+H)*H);
print Pillai;

LawHot=trace(EiH);
print LawHot;
quit;


