import yfinance as yf
import nasdaq_ticker_download as ntd


def extract_nasdaq_tickers():
    target_path = ".\\nasdaq\\tickers"
    ntd.download_files(["nasdaqlisted.txt", "otherlisted.txt", "nasdaqtraded.txt"], target_path)
    nasdaq_tickers = []
    with open("nasdaqlisted.txt", "r") as file:
        for line in file:
            parts = line.split("|")
            ticker = parts[0]
            nasdaq_tickers.append(ticker.strip())
    nasdaq_tickers.pop(0)  # Remove header line
    nasdaq_tickers.pop(-1)  # Remove footer line
    return nasdaq_tickers


def calculate_daily_performance(stock):
    try:
        stock_data = stock.history(period="5d")
        prices = stock_data["Close"]
        performance2 = ((prices.iloc[-1] - prices.iloc[-2]) / prices.iloc[-2]) * 100
        return performance2
    except:
        print(f"Exception: {stock.ticker} doesn't have a proper daily history")
        raise


if __name__ == '__main__':
    performance_list = []

    for i, stock_symbol in enumerate(extract_nasdaq_tickers()):
        try:
            stock = yf.Ticker(stock_symbol)

            # Calculate latest daily performance
            performance = calculate_daily_performance(stock)

            performance_list.append((stock_symbol, performance))
            print(f"{stock_symbol} successfully fetched.")
        except:
            print(f"Exception: error occurred for {stock_symbol}. Ignored.")

    # List sorting
    sorted_performance_list = sorted(performance_list, key=lambda x: x[1], reverse=True)

    # Print sorted list
    for stock_symbol, performance in sorted_performance_list:
        print(f"Stock: {stock_symbol} - Performance: {performance:.2f}%")
