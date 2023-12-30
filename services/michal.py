import base64
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import io

def get_data():
  df = pd.read_csv('/Users/xeross99/Desktop/BTC-USD/data/BTC-USD.csv')
  df['Date'] = pd.to_datetime(df['Date'])
  return df

def all_time_low():
  df = get_data()
  min_low_index = df['Low'].idxmin()
  min_low_row = df.loc[min_low_index]
  plt.plot(df['Date'], df['Low'], label='Cena')
  plt.scatter(min_low_row['Date'], min_low_row['Low'], color='red', label='All Time Low')
  plt.legend()
  plt.xticks(rotation=45)
  plt.xticks(df['Date'].dt.to_period("Y").unique(), [str(year) for year in df['Date'].dt.year.unique()])
  plt.xlabel('Data')
  plt.ylabel('Cena')
  plt.title('Wykres ceny bitcoina z oznaczonym najtańszym jego momentem')
  plt.show()

def all_time_high():
  df = get_data()
  max_high_index = df['High'].idxmax()
  max_high_row = df.loc[max_high_index]  
  plt.plot(df['Date'], df['High'], label='Cena')
  plt.scatter(max_high_row['Date'], max_high_row['High'], color='green', label='All Time High')
  plt.legend()
  plt.xticks(rotation=45)
  plt.xticks(df['Date'].dt.to_period("Y").unique(), [str(year) for year in df['Date'].dt.year.unique()])
  plt.xlabel('Data')
  plt.ylabel('Cena')
  plt.title('Wykres ceny bitcoina z oznaczonym najdroszym jego momentem')
  plt.show()