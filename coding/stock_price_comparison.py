# filename: stock_price_comparison.py
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# 下载股票数据
def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

# 获取META和TESLA最近一年的数据
meta_data = get_stock_data('META')
tesla_data = get_stock_data('TSLA')

# 创建图表
plt.figure(figsize=(12, 6))

# 绘制收盘价曲线
plt.plot(meta_data.index, meta_data['Close'], label='META', color='blue')
plt.plot(tesla_data.index, tesla_data['Close'], label='TESLA', color='red')

# 添加图表元素
plt.title('META vs TESLA Stock Price (1 Year)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)

# 自动调整日期显示
plt.gcf().autofmt_xdate()

# 显示图表
plt.show()