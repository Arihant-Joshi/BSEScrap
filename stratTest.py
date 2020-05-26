from os import listdir
from os.path import isfile, join
import pandas as pd

myPath = "Data\\"
onlyfiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for f in onlyfiles:
    df = pd.read_csv(myPath+f)