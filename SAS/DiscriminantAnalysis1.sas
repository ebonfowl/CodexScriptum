
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXAMPLE ONE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
* Reads in an example data set. Not a Rencher data set;
data school;
   	INFILE 
"C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 9 and 10 discrim\t11-6.dat";
INPUT GPA SAT group ;
run;

*ONLY USING GROUPS 1 AND 2 FOR THIS EXAMPLE. 
Subset the data for groups less than 3 (so, 1 and 2).;
data example1;
set school;
where group<3;
run; 

proc print data=example1 (obs=10);
run;

Proc means data=example1;
class group; 
run;

* Shows a scatter plot with groups identified;
proc sgplot data=example1;
scatter y=GPA x=SAT/group=group markerattrs=(symbol=circlefilled size=10);
run;

*Add centroid to scatterplots;
Data example1; set example1;
GPA_mean=3.4038710;
if group=2 then GPA_mean=2.4825;
SAT_mean=561.2258065;
if group=2 then SAT_mean=447.0714286;
run;

* Shows a scatter plot with groups identified and centroids added;
proc sgplot data=example1;
scatter y=GPA x=SAT/group=group markerattrs=(symbol=circlefilled size=10);
scatter y=GPA_mean x=SAT_mean/group=group markerattrs=(symbol=squarefilled size=12);
run;

/* makes the histograms in the class slides */
proc univariate data=example1 noprint;
histogram GPA;* /midpoints=2.2 to 3.8 by .2 ;
run;

* Shows histogram subset by group;
proc univariate data=example1 noprint;
class group;
histogram GPA;
run;

* Shows histogram subset by group;
proc univariate data=example1 noprint;
histogram SAT/midpoints=300 to 700 by 100;
run;

* Shows histogram subset by group;
proc univariate data=example1 noprint;
class group;
histogram SAT;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2-group DISCRIM EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
* First run a MANOVA to test that they are significantly different;
title "MANOVA";
proc glm data=example1;
class group;
model GPA SAT=group / nouni;
MANOVA H=group/printe printh;
/*means group;*/
run;


* The canonical command gives the output (e.g., structure coefficients) that will be similar to Chapter 8;
* POOL=TEST gives us Box's M test for equal variances;
* out= gives a output dataset that has the predicted group membership;
title "Discriminant Analysis";
proc discrim data=example1 canonical pool=test manova out=discrim_out;
class group;
var GPA SAT;
run;

proc sgplot data=example1;
scatter x=GPA y=SAT/group=group;
run;







/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Extra/Bonus material: IML EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
data school1; set example1;
where group=1;

data school2; set example1;
where group=2;
run;

proc iml;
use school1;
read all var{GPA SAT} into sch1;
use school2;
read all var{GPA SAT} into sch2;

n1=nrow(sch1);
n2=nrow(sch2);

j1=j(n1, 1, 1);
j2=j(n2, 1, 1);

meanvec1=(1/n1)*j1`*sch1;
meanvec2=(1/n2)*j2`*sch2;

S1=(1/(n1-1))*(sch1-j1*meanvec1)`*(sch1-j1*meanvec1);
S2=(1/(n2-1))*(sch2-j2*meanvec2)`*(sch2-j2*meanvec2);

Spl=((n1-1)*S1+(n2-1)*S2)/(n1+n2-2);

print meanvec1, meanvec2;
print S1, S2, Spl;

a=inv(Spl)*(meanvec1`-meanvec2`);  * Equation 8.2;
print a;

use example1;
read all var{GPA SAT} into schall;
print schall;
z=schall*a; *creates new variable from disciminant function;

create zscore from z;
append from z; 
print z;
quit;

proc iml;
use school1;
read all var{GPA SAT} into sch1;
use school2;
read all var{GPA SAT} into sch2;

n1=nrow(sch1);
n2=nrow(sch2);

j1=j(n1, 1, 1);
j2=j(n2, 1, 1);
print j1, j2;

meanvec1=(1/n1)*sch1`*j1;
meanvec2=(1/n2)*sch2`*j2;
print meanvec1, meanvec2;

S1=(1/(n1-1))*(sch1-j1*meanvec1`)`*(sch1-j1*meanvec1`);
S2=(1/(n2-1))*(sch2-j2*meanvec2`)`*(sch2-j2*meanvec2`);

Spl=((n1-1)*S1+(n2-1)*S2)/(n1+n2-2);
print Spl;

A=(meanvec1-meanvec2)`*inv(Spl);
print A;

b=(1/2)*(meanvec2`*inv(Spl)*meanvec2 - meanvec1`*inv(Spl)*meanvec1);
print b;

p1=.5;p2=.5;
p=log(p1/p2);
print p;

X={3.4,
   560};
print X;

L=A*X+b+p;
print L;
quit;


proc iml;
start classify(X1,X2,Xnew,p1,p2);
	n1=nrow(X1);
	n2=nrow(X2);

	j1=j(n1, 1, 1);
	j2=j(n2, 1, 1);

	meanvec1=(1/n1)*X1`*j1;
	meanvec2=(1/n2)*X2`*j2;


	S1=(1/(n1-1))*(X1-j1*meanvec1`)`*(X1-j1*meanvec1`);
	S2=(1/(n2-1))*(X2-j2*meanvec2`)`*(X2-j2*meanvec2`);

	Spl=((n1-1)*S1+(n2-1)*S2)/(n1+n2-2);
	print "Pooled Sigma";
	print Spl;

	a=(meanvec1-meanvec2)`*inv(Spl);

	b=(1/2)*(meanvec2`*inv(Spl)*meanvec2 - meanvec1`*inv(Spl)*meanvec1);

	print "Prior for group 1" p1;
	print "Prior for group 2" p2;
	logp=log(p1/p2);

	L=a*Xnew+b+logp;

	print meanvec1 meanvec2 Xnew;
	print a, b;
	print "Prior log odds" logp;
	print "L > 1 favors Group 1 and < 1 favors Group 2" L;
finish;

use school1;
read all var{GPA SAT} into X1;
use school2;
read all var{GPA SAT} into X2;

Xnew={2.95,
      500};
prior1=.5;
prior2=.5;
      
call classify(X1,X2,Xnew,prior1,prior2);

quit;




* COL1 was calculated in proc IML;
* It is z based on dscriminant function;
* Notice the separation;
proc univariate data=zscore;
histogram COL1/midpoints=65 to 110 by 5;
run;

* Creates a data set that merges z onto the original data set;
data disc; 
merge example1 zscore;
run;

* COL1 was calculated in proc IML;
* It is z based on dscriminant function;
* Notice the separation;
proc univariate data=disc;
class group;
histogram COL1;
run;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END IML EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
