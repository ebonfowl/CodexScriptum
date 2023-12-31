Proc import datafile="C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 5 Hotellings T\lab activity math.xlsx"
out=math replace dbms=xlsx;
run;

proc iml;
/*This is a function that will compute T2 for a one sample T-test.
This just defines the function, you can add this at the beginning 
of your program and then call the function and it will compute the 
mean vector, variance/covariance matrix, and T2*/;
/*~~~~~~~~~~~~~~~DO NOT CHANGE ANYTHING BETWEEN THESE LINES  ~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
start onettest(x, Ho);
	*Compute n and p*/;
	n=nrow(x);
	p=ncol(x);
	title "One sample T-Test";
	print n;
	*make j vectors*/;
	jn=j(n, 1, 1);
	jp=j(p, 1, 1);
	*compute yvar*/; 
	ybart=(1/n)*jn`*x;
	ybar=ybart`;
	*Another way to make a (31 x 3) matrix with each mean in the correct col*/;
	dmean=diag(ybart);
	print ybart;
	jnp=jn*jp`;
	meanmat=jnp*dmean;
	*Compute covariance and correlation matrix of Time, Year, and Happy;
	S=(1/(n-1))*(x-meanmat)`*(x-meanmat);
	print S;
	*Compute T2;
	T2=n*(ybar-Ho)`*inv(S)*(ybar-Ho);
	print T2;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" p;
	nu=n-1;
	print "Degrees of freedom=" nu ;

	*Transform T2 to F;
	F=((nu-p+1)/((nu)*p))*T2;
	Fcritical=quantile('F',.95,p,nu-p+1);
	print "T2 transformed to an F" F;
	print "F-critical (reject null if F > F critical)" Fcritical; 
finish;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
*This is the part you need to change!;
use math;
read all var{stdread mathse2 t1math} into X;
Ho={510, 3.5, 51};
call onettest(X, Ho);
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

proc iml;
/*This is a function that will compute T2 for a one sample T-test (for paired data).
This just defines the function, you can add this at the beginning 
of your program (in proc iml) and then call the function and it will compute the 
mean vector of D, variance/covariance matrix of D, and T2*/;
/*~~~~~~~~~~~~~~~DO NOT CHANGE ANYTHING BETWEEN THESE LINES  ~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
start pairttest(y, x);
	*Compute n and p*/;
	title "Test for paired differences";
	n=nrow(x);
	p=ncol(x);
	*make j vectors*/;
	jn=j(n, 1, 1);
	jp=j(p, 1, 1);
	*compute d*/;
	D=y-x; 
	*compute yvar*/; 
	dbart=(1/n)*jn`*D;
	dbar=dbart`;
	*Another way to make a (31 x 3) matrix with each mean in the correct col*/;
	dmean=diag(dbart);
	print n;
	print dbart;
	jnp=jn*jp`;
	meanmat=jnp*dmean;
	*Compute covariance and correlation matrix of y1 y2 y3;
	Sd=(1/(n-1))*(d-meanmat)`*(d-meanmat);
	print Sd;
	*Compute T2;
	T2=n*(dbar)`*inv(Sd)*(dbar);
	print T2;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" p;
	nu=n-1;
	print "Degrees of freedom" nu ;
		*Transform T2 to F;
	F=((nu-p+1)/((nu)*p))*T2;
	Fcritical=quantile('F',.95,p,nu-p+1);
	print "T2 transformed to an F" F;
	print "F-critical (reject null if F > F critical)" Fcritical; 
finish;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

*EXAMPLES;
*This is the part you need to change!;
use math;
read all var{mathse1 t1math} into y1;
use math;
read all var{mathse2 t2math} into y2;
call pairttest(y1, y2);



data male; set math (where=(male=1));
data female; set math (where=(male=0));
run;

proc iml;
/*This is a function that will compute T2 for a two sample T-test.
This just defines the function, you can add this at the beginning 
of your program (in proc iml) and then call the function and it will compute the 
mean vector, Pooled variance/covariance matrix, and T2*/;
/*~~~~~~~~~~~~~~~DO NOT CHANGE ANYTHING BETWEEN THESE LINES  ~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
start twottest(y1, y2);
	*Compute n and p*/;
	n1=nrow(y1);
	n2=nrow(y2);
	p=ncol(y1);
	title "Two Sample TTest";
	*make j vectors*/;
	jn1=j(n1, 1, 1);
	jn2=j(n2, 1, 1);
	jp=j(p, 1, 1);
	*compute yvar*/; 
	ybart1=(1/n1)*jn1`*y1;
	ybar1=ybart1`;
	ybart2=(1/n2)*jn2`*y2;
	ybar2=ybart2`;
	*Another way to make a (31 x 3) matrix with each mean in the correct col*/;
	dmean1=diag(ybart1);
	jn1p=jn1*jp`;
	meanmat1=jn1p*dmean1;
	dmean2=diag(ybart2);
	jn2p=jn2*jp`;
	meanmat2=jn2p*dmean2;
	*Compute Pooled covariance and correlation matrix of Time, Year, and Happy;
	S1=(1/(n1-1))*(y1-meanmat1)`*(y1-meanmat1);
	S2=(1/(n2-1))*(y2-meanmat2)`*(y2-meanmat2);
	Spl=(1/(n1+n2-2))*((n1-1)*S1+(n2-1)*S2);
	*Compute T2;
	T2=(n1*n2)/(n1+n2)*(ybar1-ybar2)`*inv(Spl)*(ybar1-ybar2);
	print n1 "     " n2;
	print ybar1 "     " ybar2;
	print S1 "     " S2;
	print Spl;
	print T2;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" p;
	nu=n1+n2-2;
	print "Degrees of freedom=" nu ;
		*Transform T2 to F;
	F=((nu-p+1)/((nu)*p))*T2;
	Fcritical=quantile('F',.95,p,nu-p+1);
	print "T2 transformed to an F" F;
	print "F-critical (reject null if F > F critical)" Fcritical; 
finish;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


*EXAMPLES;
*This is the part you need to change!;
use male;
read all var{STDREAD MATHSE1 T1MATH} into y1;
use female;
read all var{STDREAD MATHSE1 T1MATH} into y2;
call twottest(y1, y2);  


proc iml;
/*~~~~~~~~~~~~~~~DO NOT CHANGE ANYTHING BETWEEN THESE LINES  ~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

start addttest(y1, x1, y2, x2);
	*Compute n and p*/;
	title "Test for Additional Information";
	p=ncol(y1);
	q=ncol(x1);
	n1=nrow(y1);
	n2=nrow(y2);
	pq=p+q;
	allpq1=y1||x1;
	allpq2=y2||x2;
	*make j vectors*/;
	jn1=j(n1, 1, 1);
	jn2=j(n2, 1, 1);
	jpq=j(pq, 1, 1);
	*compute yvar*/; 
	pqbart1=(1/n1)*jn1`*allpq1;
	pqbart2=(1/n2)*jn2`*allpq2;
	pqbar1=pqbart1`;
	pqbar2=pqbart2`;
	*Another way to make a (31 x 3) matrix with each mean in the correct col*/;
	dmean1=diag(pqbart1);
	jnpq1=jn1*jpq`;
	meanmat1=jnpq1*dmean1;
	dmean2=diag(pqbart2);
	jnpq2=jn2*jpq`;
	meanmat2=jnpq2*dmean2;
	*Compute covariance and correlation matrix of y1 y2 y3;
	Spq1=(1/(n1-1))*(allpq1-meanmat1)`*(allpq1-meanmat1);
	Spq2=(1/(n2-1))*(allpq2-meanmat2)`*(allpq2-meanmat2);
	Splpq=(1/(n1+n2-2))*((n1-1)*Spq1+(n2-1)*Spq2);
	*Compute T2;
	T2pq=(n1*n2)/(n1+n2)*(pqbar1-pqbar2)`*inv(Splpq)*(pqbar1-pqbar2);
	Print "*****************Two Sample TTest for group differences using all variables*****************";
	print T2pq;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" pq;
	nu=n1+n2-2;
	print "Degrees of freedom" nu ;
	ybar1=pqbar1[1:p,];
	ybar2=pqbar2[1:p,];
	Sply=Splpq[1:p,1:p];
	T2p=(n1*n2)/(n1+n2)*(ybar1-ybar2)`*inv(Sply)*(ybar1-ybar2);
	Print "*****************Two Sample TTest for group differences using Only Y*****************";
	print T2p;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" p;
	nu=n1+n2-2;
	print "Degrees of freedom" nu ;
	Txgiveny=(nu-p)*(T2pq-T2p)/(nu+T2p);
	Print "*****************Two Sample TTest for group differences of X given Y*****************";
	print Txgiveny;
	print "compare T2 to a T2 Distribution (Table A.7) with:";
	print "Number of Variables (p)=" q;
	nu=n1+n2-2-p;
	print "Degrees of freedom" nu ;
		*Transform T2 to F;
    F=(nu-p)*((T2pq-T2p)/(nu+T2pq));
    Fcritical=quantile('F',.95,q,nu-p-q+1);
	print "Txgiveny transformed to an F" F;
	print "F-critical (reject null if Fxgiveny > F critical)" Fcritical; 
finish;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

*EXAMPLES;
*This is the part you need to change!;

use male;
read all var{STDREAD MATHSE1} into y1;
use female;
read all var{STDREAD MATHSE1} into y2;

use male;
read all var{T1MATH} into x1;
use female;
read all var{T1MATH} into x2;

* This statement calls the function defined in the IML code above;
* This statement should produce the output needed to interpret your findings;
call addttest(y1, x1, y2, x2);

quit;
