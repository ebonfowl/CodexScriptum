from cmath import sqrt
from tkinter import Frame
from statsmodels.stats.weightstats import ttost_paired as TOST
from scipy.stats import pearsonr
import pandas as pd
import pingouin as pg
import numpy as np
import fnmatch
import researchpy as rp
import statsmodels as sm
import pyCompare as pyc
import os

# ebonfowl: function def to convert tuple to string

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

# ebonfowl: import the master analysis csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# df = pd.read_csv('e:\\Documents\\RepOne Validation\\RepOneDatabase.csv')

df = pd.read_csv('RepOneDatabase.csv')

i = 101
n = 1

# directory = os.fsencode('e:\\Documents\\RepOne Validation')

# directory = os.fsencode('e:\\Documents\\RepOne Validation')

# ebonfowl: wrap the whole thing in a while loop to restart the for loop to re-loop for every file name

restart = True

while restart:
    restart = False

    # ebonfowl: loop all file names to find the one I am looking for
    
    for file in os.listdir():

        filename = os.fsdecode(file)
        correctfilename = 'ROV'+str(i)+'_STS_0'+str(n)+'.csv'
        if fnmatch.fnmatch(filename, correctfilename):
            
            # ebonfowl: check that it is a file just in case
        
            # fpath = 'f:\\Anaconda\\'+filename

            fpath = os.path.abspath(filename)
            
            if os.path.isfile(fpath):

                # print('worked')

                # print(correctfilename)

                mydata = pd.read_csv(fpath) # ebonfowl: figure out how to concatonate files into read_csv

                # ebonfowl: make sure we sucked all the data in
                # print(mydata.to_string())

                # ebonfowl: to list column names
                # for col in mydata.columns:
                #     print(col)

                # make the frames start at frame one for forces

                firstframe = mydata.iat[0, 0]

                mydata['Frame'] = mydata['Frame'] - firstframe

                # print(firstframe)

                # ebonfowl: aggregate force data by frame to reduce sampling frequency

                framegrouped = mydata.groupby('Frame').agg({'Fx1':'mean', 'Fy1':'mean', 'Fz1':'mean', 'Fx2':'mean', 'Fy2':'mean', 'Fz2':'mean'})

                # ebonfowl: make sure the force data get frame-smooshed correctly
                # print(framegrouped.to_string())

                # FORCES
                # ebonfowl: multiply GRF by -1 to reverse negative values

                framegrouped['Fz1'] = framegrouped['Fz1']*-1

                framegrouped['Fz2'] = framegrouped['Fz2']*-1

                # ebonfowl: sum forces to get resultant vectors

                framegrouped['FxR'] = framegrouped['Fx1']+framegrouped['Fx2']

                framegrouped['FyR'] = framegrouped['Fy1']+framegrouped['Fy2']

                framegrouped['FzR'] = framegrouped['Fz1']+framegrouped['Fz2']

                # ebonfowl: calculate absolute resultant force

                framegrouped['FR'] = np.sqrt((framegrouped['FxR']*framegrouped['FxR'])+(framegrouped['FyR']*framegrouped['FyR'])+(framegrouped['FzR']*framegrouped['FzR']))

                # POSITION
                # ebonfowl: find the body center coordinates

                framegrouped['X_Cent'] = mydata[['X_LA', 'X_RA', 'X_LP', 'X_RP']].mean(axis=1)

                framegrouped['Y_Cent'] = mydata[['Y_LA', 'Y_RA', 'Y_LP', 'Y_RP']].mean(axis=1)

                framegrouped['Z_Cent'] = mydata[['Z_LA', 'Z_RA', 'Z_LP', 'Z_RP']].mean(axis=1)

                # framegrouped['X_Cent'] = mydata[['X_LA', 'X_RA', 'X_LP', 'X_RP', 'X_LS', 'X_RS']].mean(axis=1)

                # framegrouped['Y_Cent'] = mydata[['Y_LA', 'Y_RA', 'Y_LP', 'Y_RP', 'Y_LS', 'Y_RS']].mean(axis=1)

                # framegrouped['Z_Cent'] = mydata[['Z_LA', 'Z_RA', 'Z_LP', 'Z_RP', 'Z_LS', 'Z_RS']].mean(axis=1)

                # ebonfowl: calculate absolute vertical displacement for later use

                framegrouped['Disp_Vert_Abs'] = framegrouped['Z_Cent'].sub(framegrouped.iloc[0]['Z_Cent'])

                # ebonfowl: calculate vertical velocity from displacement

                framegrouped['Disp_Vert'] = framegrouped['Z_Cent'].sub(framegrouped['Z_Cent'].shift(1))

                framegrouped['Vel_Vert'] = framegrouped['Disp_Vert']/0.01666666667/1000

                # ebonfowl: calculate resultant velocity from displacement

                framegrouped['Vel_Res'] = np.sqrt((framegrouped['X_Cent'].sub(framegrouped['X_Cent'].shift(1)))*(framegrouped['X_Cent'].sub(framegrouped['X_Cent'].shift(1)))+(framegrouped['Y_Cent'].sub(framegrouped['Y_Cent'].shift(1)))*(framegrouped['Y_Cent'].sub(framegrouped['Y_Cent'].shift(1)))+(framegrouped['Z_Cent'].sub(framegrouped['Z_Cent'].shift(1)))*(framegrouped['Z_Cent'].sub(framegrouped['Z_Cent'].shift(1))))/0.01666666667/1000

                # POWER
                # ebonfowl: get vertical power from vertical velocity and vertical force

                framegrouped['Pow_Vert'] = framegrouped['Vel_Vert']*framegrouped['FzR']

                # ebonfowl: get resultant power from resultant velocity and resultant force

                framegrouped['Pow_Res'] = framegrouped['Vel_Res']*framegrouped['FR']

                # print(framegrouped.to_string())

                # OUTCOME VARIABLES

                # ebonfowl: first we must find the starting and stopping point of the movement

                min = framegrouped['Disp_Vert_Abs'].ge(20) # ebonfowl: adjust this diplacement to set the sensitivity to the movement start (10 = 1cm)

                sts_start = min.idxmax()

                # ebonfowl: now we must find the end of the concentric phase of the movement

                sts_end = framegrouped['Disp_Vert_Abs'].idxmax()

                # ebonfowl: now we can compute average velocity and power

                vp_array = framegrouped['Pow_Vert'].to_numpy()

                vp_slice = vp_array[sts_start: sts_end]

                avg_pow_vert = np.mean(vp_slice) # ebonfowl: average vertical power

                vv_array = framegrouped['Vel_Vert'].to_numpy()

                vv_slice = vv_array[sts_start: sts_end]

                avg_vel_vert = np.mean(vv_slice) # ebonfowl: average vertical velocity

                rp_array = framegrouped['Pow_Res'].to_numpy()

                rp_slice = rp_array[sts_start: sts_end]

                avg_pow_res = np.mean(rp_slice) # ebonfowl: average resultant power

                rv_array = framegrouped['Vel_Res'].to_numpy()

                rv_slice = rv_array[sts_start: sts_end]

                avg_vel_res = np.mean(rv_slice) # ebonfowl: average resultant velocity

                # ebonfowl: now compute peak power and velocity

                peak_pow_vert = framegrouped['Pow_Vert'].max()

                peak_vel_vert = framegrouped['Vel_Vert'].max()

                peak_pow_res = framegrouped['Pow_Res'].max()

                peak_vel_res = framegrouped['Vel_Res'].max()

                # peak_vel_res_id = framegrouped['Vel_Res'].idxmax()

                # ANALYSIS DATA SET

                # ebonfowl: add each outcome variable to the analysis dataframe with concatonated index strings

                # stack the outcomes rather than putting them in columns

                row = ((i - 101)*5) + n + 100
                
                # reultant peak power

                label = 'STS_peak_pow_res'

                df.loc[df['ID'] == row, [label]] = peak_pow_res

                # vertical peak power

                label = 'STS_peak_pow_vert'

                df.loc[df['ID'] == row, [label]] = peak_pow_vert

                # resultant peak velocity

                label = 'STS_peak_vel_res'

                df.loc[df['ID'] == row, [label]] = peak_vel_res

                # vertical peak velocity

                label = 'STS_peak_vel_vert'

                df.loc[df['ID'] == row, [label]] = peak_vel_vert

                # resultant average power

                label = 'STS_avg_pow_res'

                df.loc[df['ID'] == row, [label]] = avg_pow_res

                # vertical average power

                label = 'STS_avg_pow_vert'

                df.loc[df['ID'] == row, [label]] = avg_pow_vert

                # resultant average velocity

                label = 'STS_avg_vel_res'

                df.loc[df['ID'] == row, [label]] = avg_vel_res

                # vertical average velocity

                label = 'STS_avg_vel_vert'

                df.loc[df['ID'] == row, [label]] = avg_vel_vert

                # add a column with participant IDs

                label = 'STUDY_ID'

                df.loc[df['ID'] == row, [label]] = i

                # CLEAN UP

                # ebonfowl: probably unneccessary, but just in case I am cleaning everything

                # ebonfowl: on second thought, lets see how it runs first with multiple files

                # ebonfowl: if we made it here, we got the file and can continue with the next in the sequence

                # break
            
            # else: # ebonfowl: if not a file skip to the next one
                # continue
        # else: # ebonfowl: if the file does not match the one we are looking for, skip to the next one
            # continue

    if n < 5:
        restart = True
        n += 1
    else:
        n = 1
        if i < 151: # ebonfowl: stop at max participant number - adjust inequality to alter cutoff
            restart = True
            i += 1

# RUN DEM STATS!

# print(framegrouped.to_string())

# print(str(sts_end))

# print(df.to_string())

# print(df[label].to_string)

df.to_csv('test.csv')

# TENDO AP

aptendo = pd.DataFrame()

aptendo['Atest'] = df['STS_avg_pow_res']

aptendo['Btest'] = df['TENDO_AP']

aptendo['ID'] = df['ID']

TAPcorr = aptendo.corr()

aptendo = aptendo.truncate(before=0, after=136) # remove this line if the data set gets filled up

TAPa = aptendo['Atest'].to_numpy()

TAPb = aptendo['Btest'].to_numpy()

TAPmd = aptendo['Atest'].mean() - aptendo['Btest'].mean()

pyc.blandAltman(aptendo['Atest'], aptendo['Btest'], savePath='AP_TENDO_LOA.png')

aptendo = pd.melt(aptendo, id_vars='ID', value_vars=['Atest', 'Btest'])

TAPicc = pg.intraclass_corr(data=aptendo, targets='ID', raters='variable', ratings='value', nan_policy='omit')

TAPicc.set_index('Type')

low = TAPmd - 21.69

upp = TAPmd + 21.69

TAPtost = TOST(TAPa, TAPb, low, upp)

# print(TAPtost)

# TENDO PP

pptendo = pd.DataFrame()

pptendo['Atest'] = df['STS_peak_pow_res']

pptendo['Btest'] = df['TENDO_PP']

pptendo['ID'] = df['ID']

TPPcorr = pptendo.corr()

pptendo = pptendo.truncate(before=0, after=136) # remove this line if the data set gets filled up

TPPa = pptendo['Atest'].to_numpy()

TPPb = pptendo['Btest'].to_numpy()

TPPmd = pptendo['Atest'].mean() - pptendo['Btest'].mean()

pyc.blandAltman(pptendo['Atest'], pptendo['Btest'], savePath='PP_TENDO_LOA.png')

pptendo = pd.melt(pptendo, id_vars='ID', value_vars=['Atest', 'Btest'])

TPPicc = pg.intraclass_corr(data=pptendo, targets='ID', raters='variable', ratings='value')

TPPicc.set_index('Type')

low = TPPmd - 158.44

upp = TPPmd + 158.44

TPPtost = TOST(TPPa, TPPb, low, upp)

# TENDO AV

avtendo = pd.DataFrame()

avtendo['Atest'] = df['STS_avg_vel_res']

avtendo['Btest'] = df['TENDO_AV']

avtendo['ID'] = df['ID']

TAVcorr = avtendo.corr()

avtendo = avtendo.truncate(before=0, after=136) # remove this line if the data set gets filled up

TAVa = avtendo['Atest'].to_numpy()

TAVb = avtendo['Btest'].to_numpy()

TAVmd = avtendo['Atest'].mean() - avtendo['Btest'].mean()

pyc.blandAltman(avtendo['Atest'], avtendo['Btest'], savePath='AV_TENDO_LOA.png')

avtendo = pd.melt(avtendo, id_vars='ID', value_vars=['Atest', 'Btest'])

TAVicc = pg.intraclass_corr(data=avtendo, targets='ID', raters='variable', ratings='value')

TAVicc.set_index('Type')

low = TAVmd - .0227

upp = TAVmd + .0227

TAVtost = TOST(TAVa, TAVb, low, upp)

# TENDO PV

pvtendo = pd.DataFrame()

pvtendo['Atest'] = df['STS_peak_vel_res']

pvtendo['Btest'] = df['TENDO_PV']

pvtendo['ID'] = df['ID']

TPVcorr = pvtendo.corr()

pvtendo = pvtendo.truncate(before=0, after=136) # remove this line if the data set gets filled up

TPVa = pvtendo['Atest'].to_numpy()

TPVb = pvtendo['Btest'].to_numpy()

TPVmd = pvtendo['Atest'].mean() - pvtendo['Btest'].mean()

pyc.blandAltman(pvtendo['Atest'], pvtendo['Btest'], savePath='PV_TENDO_LOA.png')

pvtendo = pd.melt(pvtendo, id_vars='ID', value_vars=['Atest', 'Btest'])

TPVicc = pg.intraclass_corr(data=pvtendo, targets='ID', raters='variable', ratings='value')

TPVicc.set_index('Type')

low = TPVmd - .14497

upp = TPVmd + .14497

TPVtost = TOST(TPVa, TPVb, low, upp)

# REPONE AP

aprepone = pd.DataFrame()

aprepone['Atest'] = df['STS_avg_pow_res']

aprepone['Btest'] = df['REPONE_AP']

aprepone['ID'] = df['ID']

RAPcorr = aprepone.corr()

aprepone = aprepone.truncate(before=0, after=136) # remove this line if the data set gets filled up

RAPa = aprepone['Atest'].to_numpy()

RAPb = aprepone['Btest'].to_numpy()

RAPmd = aprepone['Atest'].mean() - aprepone['Btest'].mean()

pyc.blandAltman(aprepone['Atest'], aprepone['Btest'], savePath='AP_REPONE_LOA.png')

aprepone = pd.melt(aprepone, id_vars='ID', value_vars=['Atest', 'Btest'])

RAPicc = pg.intraclass_corr(data=aprepone, targets='ID', raters='variable', ratings='value')

RAPicc.set_index('Type')

low = RAPmd - 21.69

upp = RAPmd + 21.69

RAPtost = TOST(RAPa, RAPb, low, upp)

# REPONE AV

avrepone = pd.DataFrame()

avrepone['Atest'] = df['STS_avg_vel_res']

avrepone['Btest'] = df['REPONE_AV']

avrepone['ID'] = df['ID']

RAVcorr = avrepone.corr()

avrepone = avrepone.truncate(before=0, after=136) # remove this line if the data set gets filled up

RAVa = avrepone['Atest'].to_numpy()

RAVb = avrepone['Btest'].to_numpy()

RAVmd = avrepone['Atest'].mean() - avrepone['Btest'].mean()

pyc.blandAltman(avrepone['Atest'], avrepone['Btest'], savePath='AV_REPONE_LOA.png')

avrepone = pd.melt(avrepone, id_vars='ID', value_vars=['Atest', 'Btest'])

RAVicc = pg.intraclass_corr(data=avrepone, targets='ID', raters='variable', ratings='value')

RAVicc.set_index('Type')

low = RAVmd - .0227

upp = RAVmd + .0227

RAVtost = TOST(RAVa, RAVb, low, upp)

# REPONE PV

pvrepone = pd.DataFrame()

pvrepone['Atest'] = df['STS_peak_vel_res']

pvrepone['Btest'] = df['REPONE_PV']

pvrepone['ID'] = df['ID']

RPVcorr = pvrepone.corr()

pvrepone = pvrepone.truncate(before=0, after=136) # remove this line if the data set gets filled up

RPVa = pvrepone['Atest'].to_numpy()

RPVb = pvrepone['Btest'].to_numpy()

RPVmd = pvrepone['Atest'].mean() - pvrepone['Btest'].mean()

pyc.blandAltman(pvrepone['Atest'], pvrepone['Btest'], savePath='PV_REPONE_LOA.png')

pvrepone = pd.melt(pvrepone, id_vars='ID', value_vars=['Atest', 'Btest'])

RPVicc = pg.intraclass_corr(data=pvrepone, targets='ID', raters='variable', ratings='value')

RPVicc.set_index('Type')

low = RPVmd - .14497

upp = RPVmd + .14497

RPVtost = TOST(RPVa, RPVb, low, upp)

# print(RPVicc.to_string())

# DESCRIPTIVE STATS

# desc = df.describe()

desc = rp.summary_cont(df)

desc['MDC'] = sqrt(2)*desc['SD']*1.96

desc['MDC Lower'] = desc['Mean'] - (sqrt(2)*desc['SE']*1.96)

desc['MDC Upper'] = desc['Mean'] + (sqrt(2)*desc['SE']*1.96)

# MAKE A REPORT!

# TAPtost = convertTuple(TAPtost)

with open('LPT_report.txt', 'w') as f:
    f.write('Tendo Average Power ICC')
    f.write('\n')
    f.write('\n')
    f.write(TAPicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('Tendo Average Power correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(TAPcorr))
    f.write('\n')
    f.write('\n')
    f.write('Tendo Average Power TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(TAPtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Power ICC')
    f.write('\n')
    f.write('\n')
    f.write(TPPicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Power correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(TPPcorr))
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Power TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(TPPtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('Tendo Average Velocity ICC')
    f.write('\n')
    f.write('\n')
    f.write(TAVicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('Tendo Average Velocity correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(TAVcorr))
    f.write('\n')
    f.write('\n')
    f.write('Tendo Average Velocity TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(TAVtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Velocity ICC')
    f.write('\n')
    f.write('\n')
    f.write(TPVicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Velocity correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(TPVcorr))
    f.write('\n')
    f.write('\n')
    f.write('Tendo Peak Velocity TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(TPVtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Power ICC')
    f.write('\n')
    f.write('\n')
    f.write(RAPicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Power correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(RAPcorr))
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Power TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(RAPtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Velocity ICC')
    f.write('\n')
    f.write('\n')
    f.write(RAVicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Velocity correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(RAVcorr))
    f.write('\n')
    f.write('\n')
    f.write('RepOne Average Velocity TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(RAVtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('RepOne Peak Velocity ICC')
    f.write('\n')
    f.write('\n')
    f.write(RPVicc.to_string())
    f.write('\n')
    f.write('\n')
    f.write('RepOne Peak Velocity correlation')
    f.write('\n')
    f.write('\n')
    f.write(str(RPVcorr))
    f.write('\n')
    f.write('\n')
    f.write('RepOne Peak Velocity TOST')
    f.write('\n')
    f.write('\n')
    f.write(str(RPVtost))
    f.write('\n')
    f.write('\n')
    f.write('\n')

with open('RepOne_Descriptives_report.txt', 'w') as g:
    g.write('Descriptive Stats')
    g.write('\n')
    g.write('\n')
    g.write(desc.to_string())