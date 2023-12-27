import base64
from turtle import goto
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io

def getPolandFromDataSet():
    fullPath = os.path.dirname(os.path.dirname(__file__)) + "\\data\\gdp_1960_2020.csv"
    print(fullPath)
    csv = pd.read_csv(fullPath, sep=",", encoding="utf-8")
    x: list[int] = []
    y: list[float] = []
    for index in csv.index[csv['country'] == "Poland"]:
        x.append(csv.iloc[index][0])  # year
        y.append(csv.iloc[index][4] / 1000000000)  # GDP
    
    plt.plot(x, y, color='orange')
    plt.xlim(x[0], x[-1])
    plt.ylabel("GDP (Bilions)")
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()