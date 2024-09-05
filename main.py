import os


import sys

from src.convert import convert

if len(sys.argv) > 2:
    print("This tool only takes one argument, which is the filepath.")
    exit(os.EX_USAGE)
elif len(sys.argv) == 1:
    fp = "View_My_Courses.xlsx"
else:
    fp = sys.argv[1]

calendar = convert(fp)

with open("courses.ics", "w") as file:
    file.write(calendar.to_ics())