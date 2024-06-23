import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('ggplot')

banks_stocks = ['JPM', 'BAC', 'MS', 'C', 'GS']
iron_stocks = ['BHP', 'RIO', 'VALE']

period = "10y"
interval = "1d"
historical_data = {}

for stock in banks_stocks:
    ticker = yf.Ticker(stock)
    data = ticker.history(period=period, interval=interval)
    historical_data[stock] = data[['Close', 'Volume']]

banks = pd.concat(historical_data, axis=1)

close_df = banks.loc[:, pd.IndexSlice[:, 'Close']]
close_df.columns = close_df.columns.get_level_values(0)

volume_df = banks.loc[:, pd.IndexSlice[:, 'Volume']]
volume_df.columns = volume_df.columns.get_level_values(0)

banks_rets = close_df.pct_change()

banks_rets.plot(grid=True, figsize=(14, 6))
plt.title('Bank stocks returns')
plt.ylabel('1d returns')
plt.show()

banks_rets_signal = -(
    banks_rets.rolling(2).sum().subtract(
        banks_rets.rolling(2).sum().mean(axis=1),
        axis=0
    )
)
banks_rets_signal = (
    banks_rets_signal.divide(
        banks_rets_signal.abs().sum(axis=1), 
        axis=0
    )
)

banks_rets_signal.plot(grid=True, figsize=(14, 6))
plt.title('Banks 2D Returns Space Signal')
plt.ylabel('Signal')
plt.show()

banks_rets_signal.shift(2).multiply(banks_rets).sum(axis=1).cumsum().plot(grid=True, figsize=(14, 6))
plt.title('Banks 2D Returns Space Signal Cumulative Returns')
plt.ylabel('Cumulative Returns')
plt.show()

banks_autocorr = volume_df.rolling(20).apply(lambda x: x.autocorr())

banks_autocorr.plot(grid=True, figsize=(14, 6))
plt.title('Banks 20D AutoCorr Space')
plt.ylabel('20D AutoCorr')
plt.show()

banks_autocorr_signal = -(
    banks_autocorr.subtract(
        banks_autocorr.mean(axis=1),
        axis=0
    )
)
banks_autocorr_signal = (
    banks_autocorr_signal.divide(
        banks_autocorr_signal.abs().sum(axis=1), 
        axis=0
    )
)

banks_autocorr_signal.plot(grid=True, figsize=(14, 6))
plt.title('Banks 20D AutoCorr Space Signal')
plt.ylabel('Signal')
plt.show()

equity_curve=banks_autocorr_signal.shift(2).multiply(banks_rets).sum(axis=1).cumsum()+1.
equity_curve.plot(grid=True, figsize=(14, 6))
plt.title('Banks 20d AutoCorr Space Signal Equity Curve (JPM, BAC, C, MS, GS) \n Sharpe Ratio: 0.92')
plt.ylabel('Equity')
plt.savefig("../../quant_itws/tex/include/img/banks_statarb_equity_curve.png", format='png', bbox_inches='tight', dpi=300)
plt.show()