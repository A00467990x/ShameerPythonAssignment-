import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests as rq

def fetch_historical_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    response = rq.get(url, params=params)
    data = response.json()
    prices = data.get("prices", [])
    return prices

# Function to plot coin's price over time
def plot_price(prices1, prices2, coin_name1, coin_name2):
    df1 = pd.DataFrame(prices1, columns=['Date', f'{coin_name1} Price'])
    df2 = pd.DataFrame(prices2, columns=['Date', f'{coin_name2} Price'])
    df1['Date'] = pd.to_datetime(df1['Date'], unit='ms')
    df2['Date'] = pd.to_datetime(df2['Date'], unit='ms')
    
    st.subheader(f"Coin Comparison Chart between {coin_name1} and {coin_name2}")
    plt.figure(figsize=(10, 5))
    plt.plot(df1['Date'], df1[f'{coin_name1} Price'], label=coin_name1)
    plt.plot(df2['Date'], df2[f'{coin_name2} Price'], label=coin_name2)
    plt.xlabel('Date')
    plt.ylabel('Stock price (in USD)')
    plt.title('Coin Comparison Chart')
    plt.legend()
    st.pyplot()

def main():
    st.title("Coin Comparison App")
    
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    coins_list_response = rq.get(coins_list_url)
    coins_list = coins_list_response.json()
    coin_names = [coin['name'] for coin in coins_list]
    
    coin_name1 = st.selectbox("Select Cryptocurrency 1", coin_names)
    coin_name2 = st.selectbox("Select Cryptocurrency 2", coin_names)
    
    time_frame = st.selectbox("Select Time Frame", ["1 week", "1 month", "1 year", "5 years"])
    if time_frame == "1 week":
        days = 7
    elif time_frame == "1 month":
        days = 30
    elif time_frame == "1 year":
        days = 365
    elif time_frame == "5 years":
        days = 1825
    
    coin_id1 = next(coin['id'] for coin in coins_list if coin['name'] == coin_name1)
    coin_id2 = next(coin['id'] for coin in coins_list if coin['name'] == coin_name2)
    prices1 = fetch_historical_data(coin_id1, days)
    prices2 = fetch_historical_data(coin_id2, days)
    
    plot_price(prices1, prices2, coin_name1, coin_name2)

if __name__ == "__main__":
    main()
