# filename: plot_stock_prices.py
import yfinance as yf
import matplotlib.pyplot as plt

# 下载股票数据
meta = yf.download('META', start='2022-01-01', end='2023-01-01')
tesla = yf.download('TSLA', start='2022-01-01', end='2023-01-01')

# 绘制股票价格变化图
plt.figure(figsize=(14, 7))
plt.plot(meta['Close'], label='META')
plt.plot(tesla['Close'], label='TESLA')
plt.title('META and TESLA Stock Price Changes')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()