from cmath import sqrt
from tkinter import Frame
import pandas as pd
import numpy as np
import fnmatch
import os

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
        correctfilename = 'ROV'+str(i)+'_STS'+str(n)+'.csv'
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

                # reultant peak power

                label = 'STS'+str(n)+'_peak_pow_res'

                df.loc[df['ID'] == i, [label]] = peak_pow_res

                # vertical peak power

                label = 'STS'+str(n)+'_peak_pow_vert'

                df.loc[df['ID'] == i, [label]] = peak_pow_vert

                # resultant peak velocity

                label = 'STS'+str(n)+'_peak_vel_res'

                df.loc[df['ID'] == i, [label]] = peak_vel_res

                # vertical peak velocity

                label = 'STS'+str(n)+'_peak_vel_vert'

                df.loc[df['ID'] == i, [label]] = peak_vel_vert

                # resultant average power

                label = 'STS'+str(n)+'_avg_pow_res'

                df.loc[df['ID'] == i, [label]] = avg_pow_res

                # vertical average power

                label = 'STS'+str(n)+'_avg_pow_vert'

                df.loc[df['ID'] == i, [label]] = avg_pow_vert

                # resultant average velocity

                label = 'STS'+str(n)+'_avg_vel_res'

                df.loc[df['ID'] == i, [label]] = avg_vel_res

                # vertical average velocity

                label = 'STS'+str(n)+'_avg_vel_vert'

                df.loc[df['ID'] == i, [label]] = avg_vel_vert

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