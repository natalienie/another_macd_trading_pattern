from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

class abundent_training(object):

    def __init__(self, stock, frenquency):
        self.stock = stock
        self.frenquency = frenquency




    def patternStorage(self,label_magnitude, position_holding_len, wait_len):

        ts = TimeSeries(key='5891QG9FRTQ9TNS', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=self.stock,
                         interval=self.frenquency,
                         outputsize='full')
        short_ave = data['close'].rolling(12).mean()
        long_ave = data['close'].rolling(26).mean()
        diff = short_ave - long_ave
        dea = diff.rolling(9).mean()
        macd = diff - dea
        data['MACD'] = macd
        data.dropna(axis=0, inplace=True)

        label = []
        bar = 0
        x = len(data) - position_holding_len - wait_len
        pattern = data.loc[:len(data)-position_holding_len-wait_len, ['close', 'MACD']]

        while bar < x:

            maxim = max(data['close'][bar+position_holding_len : bar+position_holding_len+wait_len])
            currentP = data['close'][bar]
            highmag = currentP * (1+label_magnitude)
            lowmag = currentP * (1-label_magnitude)
            minim = min(data['close'][bar+position_holding_len : bar+position_holding_len+wait_len])
            if maxim > highmag and minim > currentP:
                label.append(2)
                bar += 1
            elif maxim > highmag and minim < currentP:
                label.append(1)
                bar += 1
            elif maxim > currentP and minim < lowmag:
                label.append(-1)
                bar += 1
            elif maxim < currentP and minim < lowmag:
                label.append(-2)
                bar += 1
            else:
                label.append(0)
                bar += 1
        return pattern, label
