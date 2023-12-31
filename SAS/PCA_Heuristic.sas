data ex;
input ID	Handsome	Beautiful	Unsightly	Brilliant	Brainy	Silly;
cards;
1	6	5	4	8	6	2
2	8	7	2	7	5	3
3	9	8	1	9	7	1
4	5	4	5	9	7	1
5	4	3	6	9	7	1
6	7	6	3	7	5	3
7	3	2	7	7	5	3
;
run;

proc corr data=ex ;
var Handsome	Beautiful	Unsightly	Brilliant	Brainy	Silly;
run;

ods graphics on;
proc factor data=ex method=prin plots=all;
var Handsome	Beautiful	Unsightly	Brilliant	Brainy	Silly;
run;
ods graphics off;
