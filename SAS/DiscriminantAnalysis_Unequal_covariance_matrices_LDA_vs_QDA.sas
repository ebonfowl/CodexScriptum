
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
* Reads in an example data set. Not a Rencher data set;
data school;
   	INFILE "C:\Users\Aaron\Desktop\LinearDiscriminantAnalysis\Day1\t11-6.dat";
	INPUT GPA SAT group ;
run;

proc print data=school;
run;

proc means data=school;
class group; 
run;

* Shows a scatter plot with groups identified;
proc sgplot data=school;
scatter y=GPA x=SAT/group=group markerattrs=(symbol=circlefilled size=10);
run;

*Add centroid to scatterplots;
data school2; set school;
GPA_mean=3.4038710;
	if group=2 then GPA_mean=2.4825;
	if group=3 then GPA_mean=2.9927;
SAT_mean=561.2258065;
	if group=2 then SAT_mean=447.0714286;
	if group=3 then SAT_mean=446.2308;
run;

* Shows a scatter plot with groups identified and centroids added;
proc sgplot data=school2;
styleattrs datacontrastcolors=(blue red green);
scatter y=GPA x=SAT/group=group markerattrs=(symbol=circlefilled size=10);
scatter y=GPA_mean x=SAT_mean/group=group markerattrs=(symbol=squarefilled size=13);
scatter y=GPA_mean x=SAT_mean/group=group markerattrs=(symbol=square color=black size=14);
run;


ods select histogram;  /* prints the histogram only */
proc univariate data=school;
histogram GPA /midpoints=2.2 to 3.8 by .2 ;
run;

* Shows histogram subset by group;
ods select histogram;
proc univariate data=school;
class group; 
histogram GPA / midpoints=2.2 to 3.8 by .2 ;
run;

ods select histogram;
proc univariate data=school;
histogram SAT / midpoints=300 to 700 by 50;
run;

* Shows histogram subset by group;
ods select histogram;
proc univariate data=school;
class group;
histogram SAT / midpoints=300 to 700 by 50;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3-group DISCRIM EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

* First run a MANOVA to test that they are significantly different;
proc glm data=school;
class group;
model GPA SAT=group;
MANOVA H=group/printe printh;
means group;
run;

* The canonical command gives the output that will be similar to Chapter 8;
* POOL=TEST gives us Box's M test for equality of variances;
proc discrim data=school canonical pool=test manova out=discrim_out listerr crossvalidate;  
class group;					/* Box's M indicates violation of homogeneity of covariance matrices */
var GPA SAT;
run;

/* extracting group means "Class Means on Canonical Variables */
proc means data=discrim_out mean std ndec=2;
class group;
var can1 can2;
ways 0 1;
output out=can (where=(_stat_="MEAN" and group ne .));
run;

/* plotting group means */
proc sgplot data=can;
styleattrs datacontrastcolors=(blue red green);
scatter y=can1 x=can2/group=group markerattrs=(symbol=circlefilled size=14) 
	datalabel=group datalabelattrs=(size=13 weight=bold);
refline 0 / axis=x;
refline 0 / axis=y;
xaxis values=(-.75 -.5 -.25 0 .25 .5 .75);
run;

/* examining post hoc group differences */
/* only printing relevant output */
ods select cldiffs;
proc anova data=discrim_out;
class group;
model can1 = group;
means group / tukey ;
run;
quit;

ods select cldiffs;
proc anova data=discrim_out;
class group;
model can2 = group;
means group / tukey ;
run;
quit;

/* creating dummy data set to generate contour plots */
data dummy;
do GPA = 2 to 4 by 0.1;
	do SAT = 300 to 800 by 1;
	output;
	end;
end;
run;

/** Estimate linear discriminant analysis (LDA) - note "pool=yes" specifies pooled covariance matrices **/
/** "pool=test" allows SAS to determine if pooled covariance matrices should be used per the output notes **/
proc discrim data=school canonical out=lda_out testdata=dummy testout=test_lda_out pool=yes noprint; 
class group;
var GPA SAT;
run;

data figure_lda; merge lda_out test_lda_out (rename=(SAT=SAT1 GPA=GPA1)); 
_into2_=max(_1,_2,_3); /* obtaining posterior probabilit of predicted class membership */
run;

/* plotting contour plot illustrating classification boundaries */
/* may want to play around with contourtype and nlevels to get better figure */ 
proc template;
  define statgraph discrim;
    begingraph;
      layout overlay;
        contourplotparm x=SAT1 y=GPA1 z=_into2_ / contourtype=linefill gridded=false nlevels=4 gridded=true;
		scatterplot x=SAT y=GPA / group=group 
				markercharacter=group markercharacterattrs=(size=10 weight=bold) includemissinggroup=false;
        endlayout;
    endgraph;
  end;
run;
proc sgrender data=figure_lda template=discrim;
run;

/** Estimate quadratic discriminant analysis (QDA) - note "pool=no" specifies different covariance matrices for each group **/
proc discrim data=school canonical out=qda_out testdata=dummy testout=test_qda_out pool=no noprint; 
class group;
var GPA SAT;
run;

data figure_qda; merge qda_out test_qda_out (rename=(SAT=SAT1 GPA=GPA1)); 
_into2_=max(_1,_2,_3);
run;

proc template;
  define statgraph discrim;
    begingraph;
      layout overlay;
        contourplotparm x=SAT1 y=GPA1 z=_into2_ / contourtype=linefill gridded=false nlevels=4 gridded=true;
		scatterplot x=SAT y=GPA / group=group 
				markercharacter=group markercharacterattrs=(size=10 weight=bold) includemissinggroup=false;
        endlayout;
    endgraph;
  end;
run;

proc sgrender data=figure_qda template=discrim;
run;

/** QDA with strong prior on group 1 and 2 **/
proc discrim data=school canonical out=qda_out testdata=dummy testout=test_qda_out pool=no noprint; 
class group;
var GPA SAT;
priors '1'=.01 '2'=.09 '3'=.90;
run;

data figure_qda_prior; merge qda_out test_qda_out (rename=(SAT=SAT1 GPA=GPA1)); 
_into2_=max(_1,_2,_3);
run;

proc template;
  define statgraph discrim;
    begingraph;
      layout overlay;
        contourplotparm x=SAT1 y=GPA1 z=_into2_ / contourtype=linefill gridded=false nlevels=4 gridded=true;
		scatterplot x=SAT y=GPA / group=group 
				markercharacter=group markercharacterattrs=(size=10 weight=bold) includemissinggroup=false;
        endlayout;
    endgraph;
  end;
run;

proc sgrender data=figure_qda_prior template=discrim;
run;

/** LDA with strong prior on group 1 and 2 **/
proc discrim data=school canonical out=lda_out testdata=dummy testout=test_lda_out pool=yes noprint; 
class group;
var GPA SAT;
priors '1'=.01 '2'=.09 '3'=.90;
run;

data figure_lda_prior; merge lda_out test_lda_out (rename=(SAT=SAT1 GPA=GPA1)); 
_into2_=max(_1,_2,_3);
run;

proc template;
  define statgraph discrim;
    begingraph;
      layout overlay;
        contourplotparm x=SAT1 y=GPA1 z=_into2_ / contourtype=linefill gridded=false nlevels=4 gridded=true;
		scatterplot x=SAT y=GPA / group=group 
				markercharacter=group markercharacterattrs=(size=10 weight=bold) includemissinggroup=false;
        endlayout;
    endgraph;
  end;
run;

proc sgrender data=figure_lda_prior template=discrim;
run;

