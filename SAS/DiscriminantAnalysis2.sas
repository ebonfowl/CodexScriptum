/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Multi-Group DISCRIM EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
data foot;
   INFILE "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 9 and 10 discrim\T8_3_FOOTBALL.DAT";
  INPUT gr wdim circum fbeye eyehd earhd jaw;
run;

ods rtf;
proc means data=foot; 
class gr;
var wdim circum fbeye eyehd earhd jaw;
run;

*First run a MANOVA to test that they are significantly different;
Title 'MANOVA';
proc glm data=foot;
class gr;
model wdim circum fbeye eyehd earhd jaw=gr / nouni;
MANOVA H=gr/printE printH;
run;

Title 'Discriminant Analysis';
proc discrim data=foot all canonical manova out=dresults;
class gr;
var wdim circum fbeye eyehd earhd jaw;
run;

title "univariate ANOVA on first LDA can1";
proc glm data=dresults;
class gr;
model can1=gr;
means gr/tukey;
run;

ods rtf close;


data means; input gr Can1 Can2;
cards;
1 1.910378468 0.059279426 
2 -1.163989693 0.377134316 
3 -0.746388774 -0.436413742 
;
run;

Proc sgplot data=means;
dot gr/response=Can1 datalabel=gr; 
xaxis min=-1.5 max=2;
run;

Proc sgplot data=means;
dot gr/response=Can2 datalabel=gr; 
xaxis min=-1.5 max=2;
run;

proc template;
  define statgraph classify;
    begingraph;
      layout overlay;
        contourplotparm x=Can1 y=Can2 z=eyehd/ contourtype=fill  
						 nhint = 50 gridded = false;
        scatterplot x=Can1 y=Can2 / group=gr includemissinggroup=false
	                 	    markercharacter = gr MARKERCHARACTERATTRS=(size=10 weight=bold);
      endlayout;
    endgraph;
  end;
run;

proc sgrender data = dresults template = classify;
run;

* Here is the example from Rencher;
* Notice that can1 (1st disrim fuinction) does more than can2 (2nd function);
ods graphics;
proc plot data=dresults;
plot can2*can1=gr;
quit;
run;
ods graphics off;

* stepwise procedure for selecting varaibles into discrim analysis;
/*proc stepdisc data=foot;*/
/*class gr;*/
/*var wdim circum fbeye eyehd earhd jaw;*/
/*run;*/

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSIFICATION EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

proc print data=dresults; run;

data test;
input wdim circum fbeye eyehd earhd jaw;
cards /*who we are trying to reclassify*/; 
 15 55 20 13 14 11
;

title "classification";
proc discrim data=dresults /*use the zs*/ 
testdata=test /*who to classify*/ 
testout=tout /*new classification results*/ 
testlist /*append output*/;
class gr;
var wdim circum fbeye eyehd earhd jaw;
run;

proc print data=tout;
run;

*Now with a strong prior;
proc discrim data=dresults testdata=test testout=tout2 /*testlist*/;
priors '1'=.6 '2'=.3 '3'=.1;
class gr;
var wdim circum fbeye eyehd earhd jaw;
run;

proc print data=tout2;
run;


*show example of computing classification error;

proc discrim canonical data=example1 pool=test out=dresults listerr crossvalidate;
class gr;
var GPA SAT;
run;

proc discrim data=foot listerr crossvalidate;
class gr;
var wdim circum fbeye eyehd earhd jaw;
run;




*Example for classification worksheet;
data school2;
   	INFILE "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 9 and 10 discrim\school2.dat";
INPUT GPA SAT group AP;
run;

Title '3-group Discriminant Analysis';
proc sgscatter data=school2;
matrix GPA SAT AP/group=group diagonal=(histogram kernel);
run;

proc means data=school2;
class group;
var GPA SAT AP;
run;

proc discrim data=school2 canonical pool=test out=worksheet_results; /*zs found in worksheet_results dataset*/
class group;
var GPA SAT AP;
run;

data testschool2;
input GPA SAT AP;
cards;
3.0 500 3
;
run;

proc discrim data=worksheet_results testdata=testschool2 testout=tout testlist;
class group;
var GPA SAT AP;
run;

proc print data=tout; run;

proc discrim data=worksheet_results testdata=testschool2 testout=tout testlist;
class group;
var GPA SAT AP;
priors '1'=.01 '2'=.98 '3'=.01;
run;

proc print data=tout; run;

proc discrim data=school2 canonical listerr crossvalidate;
class group;
var GPA SAT AP;
run;
