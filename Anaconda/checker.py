import pandas as pd
import fnmatch
import os

i = 101
n = 1

directory = os.fsencode('e:\\Documents\\RepOne Validation')

# ebonfowl: wrap the whole thing in a while loop to restart the for loop to re-loop for every file name

restart = True

while restart:
    restart = False

    # ebonfowl: loop all file names to find the one I am looking for
    
    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        correctfilename = 'ROV'+str(i)+'_STS'+str(n)+'.csv'
        
        if fnmatch.fnmatch(filename, correctfilename):

            # print('worked')

            fpath = 'e:\\Documents\\RepOne Validation\\'+filename

            mydata = pd.read_csv(fpath) # ebonfowl: figure out how to concatonate files into read_csv

            print(mydata.to_string())

            break
        
                