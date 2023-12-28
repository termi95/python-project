import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io

def getPolandFromDataSet():
    fullPath = os.path.dirname(os.path.dirname(__file__)) + "\\data\\gdp_1960_2020.csv"
    csv = pd.read_csv(fullPath, sep=",", encoding="utf-8")
    x: list[int] = []
    y: list[float] = []
    for index in csv.index[csv['country'] == "Poland"]:
        x.append(csv.iloc[index][0])  # year
        y.append(csv.iloc[index][4] / 1000000000)  # GDP
    plt.figure()
    plt.plot(x, y, color='orange')
    plt.xlim(x[0], x[-1])
    plt.ylabel("GDP (Bilions)")
    plt.title("PKB Polski na przestrzeni 30 lat")
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()


def getPolishShareInTheWorldMarket(year):
    fullPath = os.path.dirname(os.path.dirname(__file__)) + "\\data\\gdp_1960_2020.csv"
    csv = pd.read_csv(fullPath, sep=",", encoding="utf-8")
    x: list[str] = []
    y: list[float] = []
    indexOfPoland = 0
    for index in csv.index[(csv['year'] == year) & (csv['state'] == "Europe")]:
        share = round(csv.iloc[index][5], 2)
        country = csv.iloc[index][2]                
        if share > 0 or country == "Poland":
            x.append(country)  # country
            y.append(share)  # gdp_percent
            if country == "Poland":
                indexOfPoland = x.__len__()-1

    plt.figure()
    explodeValue: list[float] = [0 for i in range(x.__len__())]
    explodeValue[indexOfPoland] = 0.4
    plt.pie(y,labels=x,shadow=True, explode=explodeValue)
    plt.title("Udział polski w światowym PKB, porównanie z krajemy Europy")

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()

def RegionGdpPerYear(year):    
    fullPath = os.path.dirname(os.path.dirname(__file__)) + "\\data\\gdp_1960_2020.csv"
    csv = pd.read_csv(fullPath, sep=",", encoding="utf-8")
    regions = dict()
    for index in csv.index[csv['year'] == year]:
        region = csv.iloc[index][3] # region
        gdp = csv.iloc[index][4] / 1000000000 # GDP
        if region in regions:
            regions[region] = regions[region] + gdp
        else:
            regions[region] = gdp

    plt.figure()
    plt.bar(list(regions.keys()),list(regions.values()))
    plt.xlabel('Region')
    plt.ylabel('suma regionu (w bilionach dolarów)')
    plt.title("Porównianie PKB dla różnych regionów")
    
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()