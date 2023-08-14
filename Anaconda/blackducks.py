import pandas as pd
import csv
import re
import sys

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

with open('e:\\Documents\\RepOne Validation\\ebird.csv', encoding="utf8") as f:

    work = re.sub('[\t]+', ',', f.read())

    print(work, file=open('e:\\Documents\\RepOne Validation\\ebird2.csv', 'w'))

with open('e:\\Documents\\RepOne Validation\\ebird2.csv','rt') as source:
    rdr = csv.reader(source)
    with open('e:\\Documents\\RepOne Validation\\ebird3.csv','wt') as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow((r[4], r[5], r[18], r[19], r[20], r[21]))

# df = pd.read_csv('e:\\Documents\\RepOne Validation\\ebird2.csv', error_bad_lines=False)

# print(df.to_string())
