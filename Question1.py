import streamlit as st
import requests as rq
import pandas as pd
import matplotlib.pyplot as plt

def stockList():
    call = "https://api.coingecko.com/api/v3/coins/list"
    response = rq.get(call)

    if(response.status_code == 200):
        stockList = response.json()
        stockNameList = [stock["name"].lower() for stock in stockList]
        return stockNameList
    else:
        return st.write("Could not retrieve stock name list")

def inputStock():
    stockList1 = stockList()
    chosenCoin = st.text_input("Enter stock name here: ",key="stock_name_input").lower()
        
    return chosenCoin




def fetch_crypto_marketChart(coinId):
    marketChartUrl = f"https://api.coingecko.com/api/v3/coins/{coinId}/market_chart?vs_currency=usd&days=365&interval=daily&precision=2"
    response = rq.get(marketChartUrl)
    
    data = response.json()
    prices = data.get("prices", [])
    df10 = pd.DataFrame(prices, columns=["Date", "Price"])
    df10['Date'] = pd.to_datetime(df10['Date'], unit='ms')
    return df10

def plotCoin(df2):
    st.subheader("Coin's price over the last year (or 52 weeks): ")

    plt.plot(df2["Date"], df2["Price"])
    plt.title("Coin's price over the last year (or 52 weeks)"   )
    plt.xlabel("Date")
    plt.ylabel("Stock price (in USD)")

    st.pyplot()

def retrieveMax(df3):
    max = df3["Price"].max()
    return max


def retrieveMin(df4):
    min = df4["Price"].max()
    return min

def retrieveMaxDay(df5):
    #locates the row in dictionary with the highest price and then retrieves its Date value
    maxDay = df5.loc[df5["Price"].idxmax()]["Date"].date()
    return maxDay

def retrieveMinDay(df6):
    #locates the row in dictionary with the lowest price and then retrieves its Date value
    minDay = df6.loc[df6["Price"].idxmin()]["Date"].date()
    return minDay

def main():
    st.title("Stock Details App")
    selectedStock = inputStock()
    selectedStockDF = fetch_crypto_marketChart(selectedStock)

    plotCoin(selectedStockDF)
    st.write(f"The minimum price of {selectedStock} over the past year is " , retrieveMin(selectedStockDF) , "(in USD)")
    st.write(f"The maximum price of {selectedStock} over the past year is " , retrieveMax(selectedStockDF) , "(in USD)")

    st.write(f"The date where {selectedStock} had its minimum price over the past year is ", retrieveMinDay(selectedStockDF))
    st.write(f"The date where {selectedStock} had its maximum price over the past year is ",  retrieveMaxDay(selectedStockDF))

if __name__ == "__main__":
    main()








