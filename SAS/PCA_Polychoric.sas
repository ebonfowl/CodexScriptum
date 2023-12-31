proc import datafile="C:\Users\xl014\Box\Xinya\Courses\ESRM6453\wk 13 PCA\SER example for PCA.xlsx"
out=ser dbms=xlsx replace;
run;

/*ser: student ethical reasoning*/
/*imp: how important do you think ethical reasoning is*/
/*conf: how confident are you in your ethical reasoning skills*/

proc corr data=ser OUTPLC=poly;
var imp1-imp5 conf1-conf5;
run;

/*Use polychoric correlation matrix*/
ods graphics on;
proc factor data=poly method=prin plot=all;
var imp1-imp5 conf1-conf5;
run; 
ods graphics off; 


/*Us pearson's r matrix*/
ods graphics on;
proc factor data=ser method=prin plot=all;
var imp1-imp5 conf1-conf5;
run; 
ods graphics off; 

