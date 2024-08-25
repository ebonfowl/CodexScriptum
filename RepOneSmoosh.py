import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv('RepOne_df_new.csv')

grouped = df.groupby('STUDY_ID').agg("mean")

grouped.to_csv('RepOneSmooshed_new.csv')