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

# --- Najnizsza cena historyczna ---
def allTimeLow():
  df = get_data()

  min_low_index = df['Low'].idxmin()
  min_low_row = df.loc[min_low_index]

  fig, ax = plt.subplots()
  ax.plot(df['Date'], df['Low'], label='Cena bitcoina')
  ax.scatter(min_low_row['Date'], min_low_row['Low'], color='red', label='All Time Low')
  ax.legend()
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  ax.set_ylabel('Cena')
  ax.set_title('Wykres ceny bitcoina z oznaczonym ATL.')
  
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Najwyzsza cena historyczna ---
def allTimeHigh():
  df = get_data()
  
  max_high_index = df['High'].idxmax()
  max_high_row = df.loc[max_high_index]
  
  fig, ax = plt.subplots() 
  ax.plot(df['Date'], df['High'], label='Cena bitcoina')
  ax.scatter(max_high_row['Date'], max_high_row['High'], color='green', label='All Time High')
  ax.legend()
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  ax.set_ylabel('Cena')
  ax.set_title('Wykres ceny bitcoina z oznaczonym ATH.')
  
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Wyświetlenie wszystkich halvingow ---
def halvings():
    df = get_data()
    halving_dates = ['2016-07-09', '2020-05-11', '2024-04-19']

    halving_values = df[df['Date'].isin(halving_dates)]
    halving_count = len(halving_values)

    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Close'], label='Cena bitcoina')

    for i in range(halving_count):
        halving_date = halving_values.iloc[i]['Date']
        ax.scatter(halving_date, halving_values.iloc[i]['Close'], color='blue', marker='^', s=100)
        ax.axvline(x=halving_date, color='gray', linestyle='--', label=f'Halving {i+1}')

    halving_3_date = pd.to_datetime('2024-04-19')
    ax.axvline(x=halving_3_date, color='gray', linestyle='--', label='Halving 2024')
    years = pd.to_datetime(df['Date']).dt.year.unique()
    ax.set_xticks([pd.to_datetime(str(year)) for year in years])
    ax.set_xticklabels([str(year) for year in years], rotation=45)
    ax.set_ylabel('Cena')
    ax.set_title('Cena bitcoina (Wszystkie Halvingi)')

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    plt.close(fig)

    return base64.b64encode(my_stringIObytes.read()).decode()

# --- Wyświetlenie 1 halvingu ---
def first_halving():
  df = get_data()
  halving_dates = ['2016-07-09', '2020-05-11', '2024-04-19']
  halving_values = df[df['Date'].isin(halving_dates)]

  halving_1_date = halving_values.iloc[0]['Date']
  halving_2_date = halving_values.iloc[1]['Date']

  price_between_dates = df[(df['Date'] >= halving_1_date) & (df['Date'] <= halving_2_date)]
  fig, ax = plt.subplots()

  years = price_between_dates['Date'].dt.year.unique()
  ax.set_xticks([pd.to_datetime(str(year)) for year in years])
  ax.set_xticklabels([str(year) for year in years], rotation=45)
  ax.plot(price_between_dates['Date'], price_between_dates['Close'], label='Cena bitcoina')
  ax.scatter(halving_values['Date'], halving_values['Close'], color='blue', label='Halving', marker='^', s=100)
  ax.axvline(x=halving_1_date, color='gray', linestyle='--', label='Halving 2016')
  ax.axvline(x=halving_2_date, color='gray', linestyle='--', label='Halving 2020')
  ax.legend()
  ax.set_ylabel('Cena')
  ax.set_title('Cena bitcoina (Halving 2016-2020)')

  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Wyświetlenie 2 halvingu ---
def second_halving():
  df = get_data()
  halving_dates = ['2016-07-09', '2020-05-11', '2024-04-19']

  halving_2_date = pd.to_datetime(halving_dates[1])
  halving_3_date = pd.to_datetime(halving_dates[2])
  price_between_dates = df[(df['Date'] > halving_2_date) & (df['Date'] <= halving_3_date)]
  
  fig, ax = plt.subplots()
  ax.plot(price_between_dates['Date'], price_between_dates['Close'], label='Cena bitcoina')
  ax.scatter(halving_2_date, df[df['Date'] == halving_2_date]['Close'], color='blue', marker='^', s=100)
  ax.axvline(x=halving_2_date, color='gray', linestyle='--', label='Halving 2020')
  ax.axvline(x=halving_3_date, color='gray', linestyle='--', label='Halving 2024')
  ax.legend()
  years = pd.date_range(start=halving_2_date, end=halving_3_date, freq='YS')
  ax.set_xticks(years)
  ax.set_xticklabels([str(year.year) for year in years], rotation=45)
  ax.set_ylabel('Cena')
  ax.set_title('Cena bitcoina (halving 2020-2024)')

  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Najnizsza cena historyczna ---
def miniAllTimeLow():
  df = get_data()
  min_low_index = df['Low'].idxmin()
  min_low_row = df.loc[min_low_index]
  fig, ax = plt.subplots()
  ax.plot(df['Date'], df['Low'])
  ax.scatter(min_low_row['Date'], min_low_row['Low'], color='red')
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Najwyzsza cena historyczna ---
def miniAllTimeHigh():
  df = get_data()  
  max_high_index = df['High'].idxmax()
  max_high_row = df.loc[max_high_index]
  fig, ax = plt.subplots() 
  ax.plot(df['Date'], df['High'])
  ax.scatter(max_high_row['Date'], max_high_row['High'], color='green')
  ax.legend()
  ax.set_xticks(df['Date'].dt.to_period("Y").unique())
  ax.set_xticklabels([str(year) for year in df['Date'].dt.year.unique()], rotation=45)
  
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Wyświetlenie wszystkich halvingow ---
def miniHalvings():
  df = get_data()
  halving_dates = ['2016-07-09', '2020-05-11', '2024-04-19']
  halving_values = df[df['Date'].isin(halving_dates)]
  halving_count = len(halving_values)
  fig, ax = plt.subplots()
  ax.plot(df['Date'], df['Close'], label='Cena bitcoina')
  for i in range(halving_count):
      halving_date = halving_values.iloc[i]['Date']
      ax.scatter(halving_date, halving_values.iloc[i]['Close'], color='blue', marker='^', s=100)
      ax.axvline(x=halving_date, color='gray', linestyle='--')
  halving_3_date = pd.to_datetime('2024-04-19')
  ax.axvline(x=halving_3_date, color='gray', linestyle='--')
  years = pd.to_datetime(df['Date']).dt.year.unique()
  ax.set_xticks([pd.to_datetime(str(year)) for year in years])
  ax.set_xticklabels([str(year) for year in years], rotation=45)
  
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)

  return base64.b64encode(my_stringIObytes.read()).decode()

# --- Wyświetlenie 1 halvingu ---
def mini_first_halving():
  df = get_data()
  halving_dates = ['2016-07-09', '2020-05-11', '2024-04-19']
  halving_values = df[df['Date'].isin(halving_dates)]

  halving_1_date = halving_values.iloc[0]['Date']
  halving_2_date = halving_values.iloc[1]['Date']

  price_between_dates = df[(df['Date'] >= halving_1_date) & (df['Date'] <= halving_2_date)]
  fig, ax = plt.subplots()

  years = price_between_dates['Date'].dt.year.unique()
  ax.set_xticks([pd.to_datetime(str(year)) for year in years])
  ax.set_xticklabels([str(year) for year in years], rotation=45)
  ax.plot(price_between_dates['Date'], price_between_dates['Close'])
  ax.scatter(halving_values['Date'], halving_values['Close'], color='blue',  marker='^', s=100)
  ax.axvline(x=halving_1_date, color='gray', linestyle='--')
  ax.axvline(x=halving_2_date, color='gray', linestyle='--')
  my_stringIObytes = io.BytesIO()
  plt.savefig(my_stringIObytes, format='jpg')
  my_stringIObytes.seek(0)
  plt.close(fig)
  return base64.b64encode(my_stringIObytes.read()).decode()
