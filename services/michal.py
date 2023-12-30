import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io

def get_data():
  fullPath = os.path.dirname(os.path.dirname(__file__)) + "/data/BTC-USD.csv"
  df = pd.read_csv(fullPath, encoding="utf-8")
  df['Date'] = pd.to_datetime(df['Date'])
  return df

def allTimeLow():
  df = get_data()
  min_low_index = df['Low'].idxmin()
  min_low_row = df.loc[min_low_index]
  fig, ax = plt.subplots()
  ax.plot(df['Date'], df['Low'], label='Cena')
  ax.scatter(min_low_row['Date'], min_low_row['Low'], color='red', label='All Time Low')
  ax.legend()
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  ax.set_xlabel('Data')
  ax.set_ylabel('Cena')
  ax.set_title('Wykres ceny bitcoina z oznaczonym najtańszym jego momentem')
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

def allTimeHigh():
  df = get_data()
  max_high_index = df['High'].idxmax()
  max_high_row = df.loc[max_high_index]
  fig, ax = plt.subplots() 
  ax.plot(df['Date'], df['High'], label='Cena')
  ax.scatter(max_high_row['Date'], max_high_row['High'], color='green', label='All Time High')
  ax.legend()
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  ax.set_xlabel('Data')
  ax.set_ylabel('Cena')
  ax.set_title('Wykres ceny bitcoina z oznaczonym najdroszym jego momentem')
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()
