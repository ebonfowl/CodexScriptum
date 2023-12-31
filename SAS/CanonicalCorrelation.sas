/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*Example 1: Academic and Psych*/
/*This is a SAS data set*/
/*I thought you might want to see how to 
read in data that is already in a SAS data set*/
libname cc "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 11 and beyond Can Corr and intro to factor";

data example;
set cc.acad_psych;
run;

proc print data=cc.acad_psych(obs=20);
run;
/**/
/*libname cancorr "C:\Users\boykin\Box\Desktop\MVS ESRM6453\Can Corr";*/
/*data example; */
/*set cancorr.acad_psych;*/
/*run;*/

proc contents data=example; run;

proc cancorr corr redundancy data=example out=ex1out
  vprefix=Psych vname='Psych Measurements'
  wprefix=Ac wname='Academics';
  var LOCUS_OF_CONTROL SELF_CONCEPT motivation;
  with read write math science;
run;

proc corr data=ex1out;
var psych1 ac1;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*Example 2: Worksheet*/
ods rtf;
data child;
infile "C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 11 and beyond Can Corr and intro to factor\childbeh.dat";
input x1 x2 x3 y1 y2;
label x1="talk" x2="violent" x3="games" y1="external" y2="internal";
run;

proc print data=child(obs=20);
run;

PROC CANCORR data=child all redundancy
  VPREFIX = TV VNAME = 'TV show VARIABLES'
  WPREFIX = ChildBhx WNAME = 'CHILD bhx VARIABLES';
  WITH Y1 Y2;
  VAR x1 x2 x3;
run;

ods rtf close;
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
