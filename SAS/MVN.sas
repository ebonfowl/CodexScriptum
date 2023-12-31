data nutrient;
  infile "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 4 MVN\usda.txt";
  input id calcium iron protein a c;
  run;

/*create box plot*/
Proc sgplot data=nutrient; 
vbox protein/labelfar datalabel=id; 
run;

/*create z-scores*/
proc standard data=nutrient mean=0 std=1 out=stndtest;
var protein;
run;

/*Flag outliers then print them*/
data stndtest; set stndtest;
outlier=0;
if protein GT 3.29 then outlier=1;
run;

proc print data=stndtest (where=(protein GT 3.29));
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Scatter plot matrices*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
Proc sgscatter data=nutrient; 
matrix calcium iron protein a c/diagonal=(histogram kernel); 
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Multivariate Outliers  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*USING PROC IML TO GET Mahalanobis Distances and identify outliers*/
PROC IML;
/* UPDATE these 3 lines to get a different datasets or vars into the code */
USE nutrient;
READ ALL VAR{calcium iron protein a c} INTO X;
CritVal= 25.21;

/*No need to change anything below this line!*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
N=NROW(X);
print N; 
XBAR=mean(X);   
print XBAR;
COVX=cov(X);
print COVX;
p=ncol(X);
out=p+1;

/*Mahalanobis distance*/
maha = mahalanobis(X, XBAR, COVX);
/*Square Mahanalanobis to compare to Table A.6*/
d2=maha*maha`;
dsq=vecdiag(d2);

/*print (maha[1:5,]), (d2[1:5,]), (dsq[1:5,]);  */

/*Examine just the first 10 rows*/
/*Concatenate the data with squared Mahalanobis distances*/
XandD2=X||dsq;

/*print (XandD2[1:5,]);*/

/*Determine the number of outliers according to critical value in Table A.6*/
outlier=loc(XandD2[,out]>CritVal);
print (XandD2[outlier,]);

/*If you want to read out the data for use with other PROCs, provide the column
names and create the SAS data set.*/
names={calcium iron protein a c Di2};
create nutrient2 from XandD2[colname=names]; 
append from XandD2;
close nutrient2;
quit;

data nutrient2;
set nutrient2;
outlier=0;
if Di2 > 25.21 then outlier=1;
run;

Proc sgscatter data=nutrient2; 
matrix calcium iron protein a c/diagonal=(histogram kernel) group=outlier
markerattrs=(size=13 symbol=circlefilled); 
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Univariate Q-Q plots ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
symbol1 value=circle height=2 color=blue;
proc univariate data=nutrient noprint;
var calcium iron protein a c;
qqplot;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Multivariate Skew/Kurtosis & Q-Q  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
PROC IML;
/* UPDATE these 2 lines to get a different datasets or vars into the code */
USE nutrient;
READ ALL VAR{calcium iron protein a c} INTO X;

/*No need to change anything below this line!*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
P=NCOL(X);
N=NROW(X);
XBAR=mean(X);   
COVX=cov(X);
maha = mahalanobis(X, XBAR, COVX);
d2=maha*maha`;
dsq=vecdiag(d2);

/*Multivariate Q-Q PLots ~~~~~~~~~~~~~~~~~*/
	U = N*Dsq/(N-1)##2;						/* Variable for multivariate Q-Q plot */
	call sort(U,1);
	s=(T(1:N)-.375)/(N+.25);
	chisqQuant=quantile("Chisqaure", s, p);
	call scatter(chisqQuant,U); 

/*Multivariate Skew/Kurtosos ~~~~~~~~~~~~~~*/
  XBARM = REPEAT(XBAR,N,1);
  /* NxN MATRIX OF XBAR VALUES */
	  G = (X-XBARM)*INV(COVX)*(X-XBARM)`;    /* ML based distance */
	  b1p = SUM(G##3)/N##2;						 /* See page 107 */
	  b2p = TRACE(G##2)/N;					     /* See page 107 */

	PRINT p, b1p, b2p;						 /* b1p and b2p exceed critical values (see Table A5) */

    small_sample_correction=((p+1)*(N+1)*(N+3))/(6*(N*((N+1)*(p+1)-6))); 
    sk=b1p*n*small_sample_correction; 
    DF=p*(p+1)*(p+2)/6; 
    sk_pvalue=1-probchi(sk,DF); 
	print "Multivariate Skewness test" sk " " sk_pvalue;
    ku=(b2p-p*(p+2))/sqrt(8*p*(p+2)/N); 
    ku_pvalue=1-probnorm(abs(ku)); 
	print "Multivariate Kurtosis Test" ku " " ku_pvalue;
    
quit;

/*Alternative method using SAS macro:*/
%inc "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 4 MVN\multnorm.sas.txt";
%multnorm(data=nutrient, var=calcium iron protein a c, plot=MULT);






/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*EXAMPLE TWO: Ex 4.6.2  in Rencher  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
data bone; 
infile "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 4 MVN\T3_6_BONE.DAT";
input obs	Age8	Age85	Age9	Age95;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Univariate Q-Q & Bivariate Scatter plots ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
symbol1 value=circle height=2 color=red;
proc univariate data=bone;
var Age8	Age85	Age9	Age95;
qqplot;
run;

Proc sgscatter data=bone; 
matrix Age8	Age85	Age9	Age95/diagonal=(histogram kernel); run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  /*Multivariate Skew/Kurtosis & Q-Q  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
PROC IML;
/* UPDATE these 2 lines to get a different datasets or vars into the code */
USE bone;
READ ALL VAR{Age8	Age85	Age9	Age95} INTO X;

  N = NROW(X);
  P = NCOL(X);
  XBAR = 1/N*X`*J(N,1);
  XBARM = REPEAT(XBAR,1,N);                  /* NxN MATRIX OF XBAR VALUES */
  S = 1/(N-1)*X`*(I(N)-1/N*J(N))*X;		     /* Sample Based Covariance Matrix */
  D = (X`-XBARM)`*INV(S)*(X`-XBARM);         /* Standardized Squared Distance */
  Di2 = VECDIAG(D);							 /* We are only interested in the values on the diagonal */
print XBAR, Di2;

/*Multivariate Q-Q PLots ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
	U = N*Di2/(N-1)##2;						/* Variable for multivariate Q-Q plot */
	call sort(U,1);
	s=(T(1:N)-.375)/(N+.25);
	chisqQuant=quantile("Chisqaure", s, p);
	call scatter(chisqQuant, U); 

/*Multivariate Skew/Kurtosos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
	  SIGHAT = 1/N*X`*(I(N)-1/N*J(N))*X;		 /* ML (population) Based Covariance Matrix, notice dividing by N */
	  G = (X`-XBARM)`*INV(SIGHAT)*(X`-XBARM);    /* ML based distance */
	  b1p = SUM(G##3)/N##2;						 /* See page 107 */
	  b2p = TRACE(G##2)/N;					     /* See page 107 */

	PRINT p, b1p, b2p;						 /* b1p and b2p exceed critical values (see Table A5) */

/*Multivariate Outliers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
  obs=j(N,1);
  do i=2 to N;
  obs[i]=obs[i-1]+1;
  end;
  XD=X||Di2||obs; *Put the X and Mahalanobis distances together;
  names={Age8	Age85	Age9	Age95 Di2 obs};
  print (XD[1:10,])[colname=names];

  call sort(XD,{5}); *Sort on the Mahalanobis distance; 
  outliers=loc(XD[,5]>11.63);
  print XD [colname=names];
  print (XD[outliers,]);
quit;

data bone; set bone;
outlier=0; 
if obs=9 then outlier=1; 
if obs=12 then outlier=1; 
if obs=20 then outlier=1; 
length color shape $8.;
if outlier=1 then do; shape="diamond"; color="red"; end;
if outlier=0 then do; shape="balloon"; color="black"; end;
run; 

/*Alternative method using SAS macro:*/
%inc "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 4 MVN\multnorm.sas.txt";
%multnorm(data=bone, var=Age8	Age85	Age9	Age95, plot=MULT);


  *The rest is optional - for creating the graph;
proc g3d data=bone;
scatter Age8*Age9=Age95/color=color shape=shape noneedle grid;
run;
