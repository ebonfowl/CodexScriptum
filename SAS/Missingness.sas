/*Read in the data set*/
PROC IMPORT datafile="C:\Users\xl014\Box\ESRM6453\Week3\exampledata1.csv"
dbms=csv out=ex1 replace;
run;

proc print data=ex1 (obs=10);
run;

/*look at the data's univariate stats to start*/
proc means data=ex1;
var v1-v7;
run;

/*one way to find out how much data is missing is to use nmiss*/
proc means data=ex1 nmiss;
var v1-v7;
run;

/*with the code below, frequencies are only computed from available data*/
proc freq data=ex1;
tables v1;
run;

/*using the missing statement computes the % missing*/
proc freq data=ex1;
tables v1/missing;
run;

/*PROC MI has an ods option called misspattern that will output 
a table of the missing data patterns present in your data file.*/ 
proc mi data=ex1 nimpute=0 ;
var v1-v7;
ods select misspattern;
run;

/*Correlate missingness with other vars*/
Data ex1_miss;
set ex1;
v1miss=0; if v1=. then v1miss=1;
v2miss=0; if v2=. then v2miss=1;
v3miss=0; if v3=. then v3miss=1;
v4miss=0; if v4=. then v4miss=1;
v5miss=0; if v5=. then v5miss=1;
v6miss=0; if v6=. then v6miss=1;
v7miss=0; if v7=. then v7miss=1;
run;

proc corr data=ex1_miss;
var v1-v7; 
with v3miss;
run;

/*Mean Imputation/replacement*/
Data ex1_miss2;
set ex1;
v1new=v1; if v1=. then v1new=2.15558;
v2new=v2; if v2=. then v2new=.57742;
v3new=v3; if v3=. then v3new=500.09091;
v4new=v4; if v4=. then v4new=.79741;
v5new=v5; if v5=. then v5new=3.31862;
v6new=v6; if v6=. then v6new=100.11364;
v7new=v7; if v7=. then v7new=108.25471;
run;

proc means data=ex1_miss2 n nmiss mean std;
var v1new v2new v3new v4new v5new v6new v7new;
run;

Proc sgplot data=ex1_miss2;
density v3/lineattrs=(color=red) type=kernel
legendlabel="original";
density v3new/lineattrs=(color=blue ) type=kernel
legendlabel="mean replacement";
run;

/*Regression Imputation (Single)*/
proc reg data=ex1;
model v3=v1 v2 v4 v5 v6 v7;
output out=ex1_v3impute p=v3imp;
run;

/*proc print data=ex1_v3impute (obs=10); run;*/

data ex1_miss3;
set ex1_v3impute;
v3new=v3; if v3=. then v3new=v3imp;
run;

proc corr data=ex1_miss3 ;
var v3 v3new ;
with v1-v2 v4-v7;
run;

/*using the missing statement computes the % missing*/
proc freq data=ex1;
tables v1/missing;
run;

data ex1_miss4;
set ex1;
v1cat='Miss';
if v1=1 then v1cat='g1';
if v1=2 then v1cat='g2';
if v1=3 then v1cat='g3';
run;

proc freq data=ex1_miss4;
tables v1cat/missing;
run;

proc glm data=ex1_miss4;
class v1cat;
model v3=v1cat;
contrast 'missing cont.' v1cat 3 -1 -1 -1;
run;

/*Graphs!*/
proc sgplot data=ex1;
histogram v7;
run;

proc sgplot data=ex1_miss4;
vbar v1cat;
run;

/*Change color of bars*/
proc sgplot data=ex1_miss4;
vbar v1cat/fillattrs=(color=green transparency=.75);
run;

proc sgplot data=ex1_miss4;
vbar v1cat;
run;

proc sgplot data=ex1_miss4;
vbar v1cat / fillattrs=(color=green transparency=.75);
run;

proc sgplot data=ex1;
scatter x=v3 y=v7;
reg x=v3 y=v7;
run;

/*have the markers be different colors for each group*/
proc sgplot data=ex1_miss4;
styleattrs datacontrastcolors=(black blue green orange);
scatter x=v3 y=v7/group=v1cat markerattrs=(symbol=circlefilled);
reg x=v3 y=v7/group=v1cat;
run;

/*Scatterplot Matrix*/
proc sgscatter data=ex1_miss4;
matrix v3 v6 v7/diagonal=(histogram);
run;

/*3-d scatter*/
proc g3d data=ex1_miss4;
   scatter v3*v6=v7/      
	  size=.75
      noneedle shape="balloon"
      grid
rotate=90
;
run;
