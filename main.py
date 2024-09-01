import os

import pandas as pd
import sys
import ics

if len(sys.argv) > 2:
    print("This tool only takes one argument, which is the filepath.")
    exit(os.EX_USAGE)
elif len(sys.argv) == 1:
    fp = "View_My_Courses.xlsx"
else:
    fp = sys.argv[0]

df = pd.read_excel(fp)
print(df)
