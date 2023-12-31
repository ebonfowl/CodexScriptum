/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Example: 2-way ANOVA/MANOVA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
*Read in dataset;
data corn;
input soil $ rotation $ yield	water	herbicide;
cards;
sandy	no	61.3	28.9	6.9
sandy	no	76.9	20.4	3
sandy	no	55.4	29.1	5
sandy	no	64.1	14.5	3.7
sandy	no	61.67	28.90	6.99
sandy	no	77.00	21.06	3.68
sandy	no	56.16	29.34	5.20
sandy	no	64.56	15.00	4.69
sandy	yes	67.3	48.3	5.5
sandy	yes	58.2	42.5	4.8
sandy	yes	66.9	23.9	1.1
sandy	yes	50.5	18	4.8
sandy	yes	67.76	48.63	5.71
sandy	yes	58.43	42.76	5.72
sandy	yes	67.57	24.05	1.99
sandy	yes	50.56	18.72	5.64
salty	no	45	15.9	1.2
salty	no	75.6	27.7	6.3
salty	no	50.6	29.7	4.7
salty	no	68.4	35.3	1.9
salty	no	45.85	16.07	1.78
salty	no	75.99	28.54	7.00
salty	no	51.02	30.27	5.36
salty	no	68.97	35.62	2.41
salty	yes	62.8	25.9	2.9
salty	yes	47.8	36.1	4.1
salty	yes	46.6	46.9	3.6
salty	yes	45.7	27.6	6.2
salty	yes	62.97	26.16	2.94
salty	yes	48.62	36.99	4.58
salty	yes	47.03	47.00	4.29
salty	yes	46.69	28.00	6.35
loam	no	60.5	32.1	6.3
loam	no	88.1	45.1	4.9
loam	no	55	31.1	6.9
loam	no	65.7	27.7	5.3
loam	no	60.79	32.18	6.39
loam	no	88.66	45.76	5.76
loam	no	55.67	31.13	7.30
loam	no	66.19	28.61	5.94
loam	yes	86.7	29.5	7.5
loam	yes	106.1	40.7	4.2
loam	yes	60.2	34.1	11.7
loam	yes	75.4	21.6	4.3
loam	yes	77.27	29.85	7.97
loam	yes	96.91	41.33	4.94
loam	yes	50.26	34.38	12.31
loam	yes	66.16	22.24	5.19
clay	no	80	54.2	4
clay	no	63.5	25.6	3
clay	no	61.5	16.8	1.9
clay	no	49.3	39.4	5.2
clay	no	80.31	54.69	4.06
clay	no	64.29	25.69	3.37
clay	no	61.51	17.05	2.17
clay	no	50.28	39.77	6.16
clay	yes	52.5	39	3.1
clay	yes	54.7	32.1	5.7
clay	yes	46.3	31.8	7.4
clay	yes	62.9	25.8	2.4
clay	yes	53.35	39.71	3.53
clay	yes	55.39	32.68	6.29
clay	yes	46.87	32.26	8.18
clay	yes	63.51	26.11	2.55
; run;

proc print data=corn; run;

*This is for a two way Manova, the test is for all possible hypotheses;
ods graphics on;
proc glm data=corn;
class soil rotation;
model yield	water herbicide=soil rotation soil*rotation;
MANOVA H=_ALL_/PRINTH PRINTE SHORT;
means soil rotation soil*rotation/tukey;
run; 
Quit;
ods graphics off;

*Same as above, only it asks for all hypotheses specifically. 
YOU WILL GET IDENTICAL RESULTS - THIS ONLY ILLUSTRATES WHAT MANOVA H=_ALL_ 
is doing "behind the scenes";
TITLE '2-WAY MANOVA (Other way)';
proc glm data=corn;
class soil rotation;
model yield	water herbicide=soil rotation soil*rotation;
MANOVA H=soil/PRINTH PRINTE SHORT;
MANOVA H=rotation/PRINTH PRINTE SHORT;
MANOVA H=soil*rotation/PRINTH PRINTE SHORT;
run; 

/*Follow-up to a significant interaction
simple main effects can be viewed as miniature one-factor MANOVA’s*/

/*We are answering: within ROTATION, which pairs of soil types differ?*/
ods graphics on;
proc glm data=corn;
class soil rotation;
model yield	water herbicide=soil rotation soil*rotation;
MANOVA H=_ALL_/PRINTH PRINTE SHORT;
lsmeans soil*rotation/slice=rotation ;
run; 
Quit;
ods graphics off;


/*Post-hoc analysis of differences in yield and herbicide across soil level within rotation type*/
proc glm data=corn (where=(rotation="yes"));
class soil;
model yield = soil;
means soil / lsd;
run;

proc glm data=corn (where=(rotation="yes"));
class soil;
model herbicide = soil;
means soil / lsd;
run;

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Box's M~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
data corn;
set corn;
category=cats(soil,rotation);
run;

proc discrim data=corn pool=test;
class category;
var yield water herbicide;
run;

proc discrim data=corn pool=test;
class soil;
var yield water herbicide;
run;

proc discrim data=corn pool=test;
class rotation;
var yield water herbicide;
run;


/*Test for additional information*/
proc glm data=corn;
class soil rotation;
model water herbicide=soil rotation soil*rotation yield	;
MANOVA H=_ALL_/PRINTH PRINTE SHORT;
run; 
