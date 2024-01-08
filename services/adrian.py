import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io
import numpy as np

def get_data():
  fullPath = os.path.dirname(os.path.dirname(__file__)) + "/data/usdpln.csv"
  df = pd.read_csv(fullPath, encoding="utf-8")
  df['Date'] = pd.to_datetime(df['Date'])
  return df



def plotHistoricalPrices():
    df = get_data()
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Close'], linestyle='-', color='b')
    plt.title('Historical Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()

def plotLowestPriceSince2000():
    df = get_data()

    df_since_2000 = df[df['Date'] >= '2000-01-01']

    lowest_price_date = df_since_2000.loc[df_since_2000['Close'].idxmin(), 'Date']
    lowest_price_value = df_since_2000['Close'].min()

    plt.figure(figsize=(10, 6))
    plt.plot(df_since_2000['Date'], df_since_2000['Close'], linestyle='-', color='g', label='Historical Prices since 2000')
    plt.scatter(lowest_price_date, lowest_price_value, color='r', label=f'Lowest Price Since 2000: {lowest_price_value:.2f}', marker='x', s=100)
    plt.title('Historical Close Prices with Lowest Price Since 2000 Highlighted')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()

def plotBestTimeToTrade2000_2015():
    # Konwertuj 'Date' na format datetime
    df = get_data()

    # Wybierz dane z zakresu lat 2000-2015
    df_2000_2015 = df[(df['Date'] >= '2000-01-01') & (df['Date'] <= '2015-12-31')]

    # Znajdź indeks dla najniższej ceny (najlepszy czas na zakup)
    min_price_index = df_2000_2015['Close'].idxmin()
    best_time_to_buy_date = df_2000_2015.loc[min_price_index, 'Date']
    best_time_to_buy_price = df_2000_2015.loc[min_price_index, 'Close']

    # Wybierz dane od czasu zakupu do końca zakresu
    df_after_purchase = df_2000_2015[df_2000_2015['Date'] >= best_time_to_buy_date]

    # Znajdź indeks dla najwyższej ceny (najlepszy czas na sprzedaż)
    max_price_index = df_after_purchase['Close'].idxmax()
    best_time_to_sell_date = df_after_purchase.loc[max_price_index, 'Date']
    best_time_to_sell_price = df_after_purchase.loc[max_price_index, 'Close']

    # Rysuj wykres z odpowiednimi oznaczeniami
    plt.figure(figsize=(10, 6))
    plt.plot(df_2000_2015['Date'], df_2000_2015['Close'], label='Close Prices', color='b')
    plt.scatter(best_time_to_buy_date, best_time_to_buy_price, color='g', label=f'Best Time to Buy: {best_time_to_buy_date.strftime("%Y-%m-%d")} at {best_time_to_buy_price:.2f} PLN/USD', marker='^', s=100)
    plt.scatter(best_time_to_sell_date, best_time_to_sell_price, color='r', label=f'Best Time to Sell: {best_time_to_sell_date.strftime("%Y-%m-%d")} at {best_time_to_sell_price:.2f} PLN/USD', marker='v', s=100)

    # Wydłuż zakres osi x o dodatkowy czas (np. 6 miesięcy przed i po)
    plt.xlim(best_time_to_buy_date - pd.DateOffset(months=6), df_2000_2015['Date'].max() + pd.DateOffset(months=6))

    # Dodaj etykiety i legendę
    plt.title('Historical Close Prices (2000-2015) with Best Time to Buy and Sell Highlighted')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()
    
def plotTrendSince2005():
    df = get_data()

    # Filtrowanie danych od 2005 roku
    df_since_2005 = df[df['Date'] >= '2005-01-01']

    # Dopasowanie wielomianu stopnia 1 (liniowego) do danych od 2005 roku
    trend_coefficients = np.polyfit(np.arange(len(df_since_2005)), df_since_2005['Close'], 1)
    trend_line = np.polyval(trend_coefficients, np.arange(len(df_since_2005)))

    plt.figure(figsize=(10, 6))
    plt.plot(df_since_2005['Date'], df_since_2005['Close'], linestyle='-', color='g', label='Historical Prices since 2005')
    plt.plot(df_since_2005['Date'], trend_line, linestyle='--', color='b', label='Trend Line (2005-2024)')
    plt.title('Historical Close Prices with Trend Line (2005-2024)')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode()
