from cmath import sqrt
from tkinter import Frame
import pandas as pd
import pingouin as pg
import numpy as np
import fnmatch
import pyCompare as pyc
import os

# ebonfowl: import the master analysis csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# df = pd.read_csv('e:\\Documents\\RepOne Validation\\RepOneDatabase.csv')

dfSTS = pd.read_csv('STS_Starter.csv')
dfCMJ = pd.read_csv('CMJ_Starter.csv')

i = 1
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
        correctfilename = 'PA'+str(i).zfill(3)+'_STS_0'+str(n)+'.csv'
        if fnmatch.fnmatch(filename, correctfilename):
            
            # ebonfowl: check that it is a file just in case

            fpath = os.path.abspath(filename)
            
            if os.path.isfile(fpath):

                mydata = pd.read_csv(fpath, header = None, names = range(21)) # ebonfowl: figure out how to concatonate files into read_csv

                # Just pre-dropping some rows to make it more readable
                mydata = mydata.drop([0, 1, 2, 3, 4])

                SplitID = mydata.index[mydata[0] == 'Trajectories'].tolist()

                SplitID, = SplitID

                df_1 = mydata.loc[:SplitID,:]
                df_2 = mydata.loc[SplitID:,:]
                df_2 = df_2.reset_index(drop = True)

                # Drop columns that aren't needed

                df_1 = df_1.drop([5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20], axis = 1)
                df_2 = df_2.drop([1, 20], axis = 1)

                # Drop rows that aren't needed
                df_2 = df_2.drop([0, 1, 2, 3, 4])

                #print(df_1.head())
                #print(df_2.head())

                # Merge them back

                df_final = pd.concat([df_1, df_2], axis = 1)
                df_final = df_final.reset_index(drop = True)
                df_final.columns = range(df_final.columns.size)

                # Rename the columns

                df_final = df_final.rename(columns = {0: "Frame", 
                                       1: "SubFrame", 
                                       2: "Fx1",
                                       3: "Fy1",
                                       4: "Fz1",
                                       5: "Fx2",
                                       6: "Fy2",
                                       7: "Fz2",
                                       8: "MFrame",
                                       9: "X_LA",
                                       10: "Y_LA",
                                       11: "Z_LA",
                                       12: "X_RA",
                                       13: "Y_RA",
                                       14: "Z_RA",
                                       15: "X_LP",
                                       16: "Y_LP",
                                       17: "Z_LP",
                                       18: "X_RP",
                                       19: "Y_RP",
                                       20: "Z_RP",
                                       21: "X_LS",
                                       22: "Y_LS",
                                       23: "Z_LS",
                                       24: "X_RS",
                                       25: "Y_RS",
                                       26: "Z_RS"
                                       })

                # print(df_final.head())

                df_final = df_final.apply(pd.to_numeric, errors = 'coerce')

                # df_final.to_csv('test.csv')

                # Now start doing calcs!

                # make the frames start at frame one for forces

                firstframe = df_final.iat[0, 0]

                df_final['Frame'] = df_final['Frame'] - (firstframe)

                # print(firstframe)

                # ebonfowl: aggregate force data by frame to reduce sampling frequency

                framegrouped = df_final.groupby('Frame').agg({'Fx1':'mean', 'Fy1':'mean', 'Fz1':'mean', 'Fx2':'mean', 'Fy2':'mean', 'Fz2':'mean'})

                # print(framegrouped.head())

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

                framegrouped['X_Cent'] = df_final[['X_LA', 'X_RA', 'X_LP', 'X_RP']].mean(axis=1)

                framegrouped['Y_Cent'] = df_final[['Y_LA', 'Y_RA', 'Y_LP', 'Y_RP']].mean(axis=1)

                framegrouped['Z_Cent'] = df_final[['Z_LA', 'Z_RA', 'Z_LP', 'Z_RP']].mean(axis=1)

                # ebonfowl: calculate absolute vertical displacement for later use

                framegrouped['Disp_Vert_Abs'] = framegrouped['Z_Cent'].sub(framegrouped.iloc[0]['Z_Cent'])

                # ebonfowl: calculate vertical velocity from displacement

                framegrouped['Disp_Vert'] = framegrouped['Z_Cent'].sub(framegrouped['Z_Cent'].shift(1))

                framegrouped['Vel_Vert'] = framegrouped['Disp_Vert']/0.01/1000

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

                sts_start = int(min.idxmax())

                # ebonfowl: now we must find the end of the concentric phase of the movement

                sts_end = int(framegrouped['Disp_Vert_Abs'].idxmax())

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

                # ANALYSIS DATA SET

                # ebonfowl: add each outcome variable to the analysis dataframe with concatonated index strings

                # stack the outcomes rather than putting them in columns

                row = ((i - 1)*5) + n

                # Record participant number

                label = 'Participant'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = i
                
                # reultant peak power

                label = 'STS_peak_pow_res'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = peak_pow_res

                # vertical peak power

                label = 'STS_peak_pow_vert'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = peak_pow_vert

                # resultant peak velocity

                label = 'STS_peak_vel_res'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = peak_vel_res

                # vertical peak velocity

                label = 'STS_peak_vel_vert'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = peak_vel_vert

                # resultant average power

                label = 'STS_avg_pow_res'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = avg_pow_res

                # vertical average power

                label = 'STS_avg_pow_vert'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = avg_pow_vert

                # resultant average velocity

                label = 'STS_avg_vel_res'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = avg_vel_res

                # vertical average velocity

                label = 'STS_avg_vel_vert'

                dfSTS.loc[dfSTS['ID'] == row, [label]] = avg_vel_vert

    if n < 5: # ebonfowl: max trial number (5)
        restart = True
        n += 1
    else:
        n = 1
        if i < 38: # ebonfowl: stop at max participant number - adjust inequality to alter cutoff (38)
            restart = True
            i += 1

# dfSTS = dfSTS.dropna(subset=['Participant'], inplace=True)

dfSTS = dfSTS.groupby('Participant').agg({'STS_peak_pow_res':'mean', 'STS_peak_pow_vert':'mean', 'STS_peak_vel_res':'mean', 'STS_peak_vel_vert':'mean', 'STS_avg_pow_res':'mean', 'STS_avg_pow_vert':'mean', 'STS_avg_vel_res':'mean', 'STS_avg_vel_vert':'mean'})

dfSTS.to_csv('test.csv')

# DO IT ALL AGAIN FOR CMJ

i = 1
n = 1

restart = True

while restart:
    restart = False

    # ebonfowl: loop all file names to find the one I am looking for
    
    for file in os.listdir():

        filename = os.fsdecode(file)
        correctfilename = 'PA'+str(i).zfill(3)+'_CMJ_0'+str(n)+'.csv'
        if fnmatch.fnmatch(filename, correctfilename):
            
            # ebonfowl: check that it is a file just in case

            fpath = os.path.abspath(filename)
            
            if os.path.isfile(fpath):

                mydata = pd.read_csv(fpath, header = None, names = range(21)) # ebonfowl: figure out how to concatonate files into read_csv

                # Just pre-dropping some rows to make it more readable
                mydata = mydata.drop([0, 1, 2, 3, 4])

                SplitID = mydata.index[mydata[0] == 'Trajectories'].tolist()

                SplitID, = SplitID

                df_1 = mydata.loc[:SplitID,:]
                df_2 = mydata.loc[SplitID:,:]
                df_2 = df_2.reset_index(drop = True)

                # Drop columns that aren't needed

                df_1 = df_1.drop([5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20], axis = 1)
                df_2 = df_2.drop([1, 20], axis = 1)

                # Drop rows that aren't needed
                df_2 = df_2.drop([0, 1, 2, 3, 4])

                #print(df_1.head())
                #print(df_2.head())

                # Merge them back

                df_final = pd.concat([df_1, df_2], axis = 1)
                df_final = df_final.reset_index(drop = True)
                df_final.columns = range(df_final.columns.size)

                # Rename the columns

                df_final = df_final.rename(columns = {0: "Frame", 
                                       1: "SubFrame", 
                                       2: "Fx1",
                                       3: "Fy1",
                                       4: "Fz1",
                                       5: "Fx2",
                                       6: "Fy2",
                                       7: "Fz2",
                                       8: "MFrame",
                                       9: "X_LA",
                                       10: "Y_LA",
                                       11: "Z_LA",
                                       12: "X_RA",
                                       13: "Y_RA",
                                       14: "Z_RA",
                                       15: "X_LP",
                                       16: "Y_LP",
                                       17: "Z_LP",
                                       18: "X_RP",
                                       19: "Y_RP",
                                       20: "Z_RP",
                                       21: "X_LS",
                                       22: "Y_LS",
                                       23: "Z_LS",
                                       24: "X_RS",
                                       25: "Y_RS",
                                       26: "Z_RS"
                                       })

                # print(df_final.head())

                df_final = df_final.apply(pd.to_numeric, errors = 'coerce')

                # df_final.to_csv('test.csv')

                # Now start doing calcs!

                # make the frames start at frame one for forces

                firstframe = df_final.iat[0, 0]

                df_final['Frame'] = df_final['Frame'] - (firstframe)

                # print(firstframe)

                # ebonfowl: aggregate force data by frame to reduce sampling frequency

                framegrouped = df_final.groupby('Frame').agg({'Fx1':'mean', 'Fy1':'mean', 'Fz1':'mean', 'Fx2':'mean', 'Fy2':'mean', 'Fz2':'mean'})

                # print(framegrouped.head())

                # FORCES
                # ebonfowl: multiply GRF by -1 to reverse negative values

                framegrouped['Fz1'] = framegrouped['Fz1']*-1

                framegrouped['Fz2'] = framegrouped['Fz2']*-1

                # ebonfowl: sum forces to get resultant vectors
                # I think everyone performed the movement on platform 1 only

                framegrouped['FxR'] = framegrouped['Fx1'] #+ framegrouped['Fx2']

                framegrouped['FyR'] = framegrouped['Fy1'] #+ framegrouped['Fy2']

                framegrouped['FzR'] = framegrouped['Fz1'] #+ framegrouped['Fz2']

                # ebonfowl: calculate absolute resultant force

                framegrouped['FR'] = np.sqrt((framegrouped['FxR']*framegrouped['FxR'])+(framegrouped['FyR']*framegrouped['FyR'])+(framegrouped['FzR']*framegrouped['FzR']))

                # POSITION
                # ebonfowl: find the body center coordinates

                framegrouped['X_Cent'] = df_final[['X_LA', 'X_RA', 'X_LP', 'X_RP']].mean(axis=1)

                framegrouped['Y_Cent'] = df_final[['Y_LA', 'Y_RA', 'Y_LP', 'Y_RP']].mean(axis=1)

                framegrouped['Z_Cent'] = df_final[['Z_LA', 'Z_RA', 'Z_LP', 'Z_RP']].mean(axis=1)

                # ebonfowl: calculate absolute vertical displacement for later use

                framegrouped['Disp_Vert_Abs'] = framegrouped['Z_Cent'].sub(framegrouped.iloc[0]['Z_Cent'])

                # ebonfowl: calculate vertical velocity from displacement

                framegrouped['Disp_Vert'] = framegrouped['Z_Cent'].sub(framegrouped['Z_Cent'].shift(1))

                framegrouped['Vel_Vert'] = framegrouped['Disp_Vert']/0.01/1000

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

                # min = framegrouped['Disp_Vert_Abs'].ge(20) # ebonfowl: adjust this diplacement to set the sensitivity to the movement start (10 = 1cm)

                # min = framegrouped['Disp_Vert_Abs'].idxmin() # this should be the bottom of the counter movement
                
                # cmj_start = int(min.idxmax())

                cmj_start = int(framegrouped['Disp_Vert_Abs'].idxmin()) # Lowest point in the CMJ

                # ebonfowl: now we must find the takeoff

                cmj_end = int(framegrouped['Vel_Vert'].idxmax()) # Fastest part of the movement is the takeoff

                # takeoff = framegrouped['FzR'].le(20) 

                # cmj_end = 

                # ebonfowl: now we can compute average velocity and power

                vp_array = framegrouped['Pow_Vert'].to_numpy()

                vp_slice = vp_array[cmj_start: cmj_end]

                avg_pow_vert = np.mean(vp_slice) # ebonfowl: average vertical power

                vv_array = framegrouped['Vel_Vert'].to_numpy()

                vv_slice = vv_array[cmj_start: cmj_end]

                avg_vel_vert = np.mean(vv_slice) # ebonfowl: average vertical velocity

                rp_array = framegrouped['Pow_Res'].to_numpy()

                rp_slice = rp_array[cmj_start: cmj_end]

                avg_pow_res = np.mean(rp_slice) # ebonfowl: average resultant power

                rv_array = framegrouped['Vel_Res'].to_numpy()

                rv_slice = rv_array[cmj_start: cmj_end]

                avg_vel_res = np.mean(rv_slice) # ebonfowl: average resultant velocity

                # ebonfowl: now compute peak power and velocity

                peak_pow_vert = framegrouped['Pow_Vert'].max()

                peak_vel_vert = framegrouped['Vel_Vert'].max()

                peak_pow_res = framegrouped['Pow_Res'].max()

                peak_vel_res = framegrouped['Vel_Res'].max()

                jump_height = framegrouped['Disp_Vert_Abs'].max() * 0.039 # Should give jump height in inches


                # ANALYSIS DATA SET

                # ebonfowl: add each outcome variable to the analysis dataframe with concatonated index strings

                # stack the outcomes rather than putting them in columns

                row = ((i - 1)*5) + n

                # Record participant number

                label = 'Participant'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = i
                
                # reultant peak power

                label = 'CMJ_peak_pow_res'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = peak_pow_res

                # vertical peak power

                label = 'CMJ_peak_pow_vert'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = peak_pow_vert

                # resultant peak velocity

                label = 'CMJ_peak_vel_res'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = peak_vel_res

                # vertical peak velocity

                label = 'CMJ_peak_vel_vert'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = peak_vel_vert

                # resultant average power

                label = 'CMJ_avg_pow_res'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = avg_pow_res

                # vertical average power

                label = 'CMJ_avg_pow_vert'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = avg_pow_vert

                # resultant average velocity

                label = 'CMJ_avg_vel_res'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = avg_vel_res

                # vertical average velocity

                label = 'CMJ_avg_vel_vert'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = avg_vel_vert

                # jump height

                label = 'CMJ_height'

                dfCMJ.loc[dfCMJ['ID'] == row, [label]] = jump_height

    if n < 3: # ebonfowl: max trial number (3)
        restart = True
        n += 1
    else:
        n = 1
        if i < 38: # ebonfowl: stop at max participant number - adjust inequality to alter cutoff (38)
            restart = True
            i += 1

dfCMJ = dfCMJ.groupby('Participant').agg({'CMJ_peak_pow_res':'mean', 'CMJ_peak_pow_vert':'mean', 'CMJ_peak_vel_res':'mean', 'CMJ_peak_vel_vert':'mean', 'CMJ_avg_pow_res':'mean', 'CMJ_avg_pow_vert':'mean', 'CMJ_avg_vel_res':'mean', 'CMJ_avg_vel_vert':'mean', 'CMJ_height':'mean'})

dfCMJ.to_csv('test2.csv')