
data wine;
  infile "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 13 PCA\wine.csv" dlm=",";
  input gender rw ds age char mer cab gewur red blanc reis berry cab2 red2;
run;

proc corr data=wine;
var char mer cab gewur red blanc reis berry cab2 red2;
run;


/**Run with covariance matrix;*/

* So you get plots;
ods graphics on;
proc princomp data=wine out=prin cov plots=score plots=pattern;
  var char mer cab gewur red blanc reis berry cab2 red2;
run;
ods graphics off; * good to close when done;

* So you get plots;
ods graphics on;
*Run with covariance matrix;
proc factor data=wine cov plots=all method=prin;
  var char mer cab gewur red blanc reis berry cab2 red2;
run;
ods graphics off; * good to close when done;

* force to retain the fourth factor;
ods graphics on;
*Run with covariance matrix;
proc factor data=wine cov plots=all method=prin nfactors=4  out=winepca;
  var char mer cab gewur red blanc reis berry cab2 red2;
run;
ods graphics off; * good to close when done;


/**Run with correlation matrix;*/

ods graphics on;
proc princomp data=wine out=princorr;
var char mer cab gewur red blanc reis berry cab2 red2;
run;
ods graphics on;

* force to retain the fourth factor;
ods graphics on;
*Run with correlation matrix;
proc factor data=wine plots=all method=prin nfactors=4  out=winepca;
  var char mer cab gewur red blanc reis berry cab2 red2;
run;
ods graphics off; * good to close when done;


proc corr data=princorr;
var prin:;
run;

proc corr data=winepca;
var factor:;
run;


proc means data=princorr; var prin:; run;
proc means data=winepca; var factor:; run;

proc sgplot data=princorr;
scatter x=prin1 y=prin2; 
run;


******************************************;
* Gambling;
******************************************;

data gamb;
infile 
"C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 13 PCA\gambling.csv" dlm=",";
input pre tol lose withd escape chase conceal illegal jeop bail impulse agree conscie extro open emotion;
run;

proc corr data=gamb;
var pre tol lose withd escape chase conceal illegal jeop bail impulse;
run;

* So you get plots;
ods graphics on;

*Run with correlation matrix;
proc princomp data=gamb out=pringamb plots=all;
var pre tol lose withd escape chase conceal illegal jeop bail;
run;
quit;
ods graphics off; * good to close when done;


ods graphics on;
*Run with correlation matrix and promax rotation;
proc factor data=gamb plots=all method=prin rotate=promax;
  var pre tol lose withd escape chase conceal illegal jeop bail;
run;
ods graphics off; * good to close when done;
