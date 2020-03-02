import pandas as pd
import tushare as tuShare
import datetime
# df = pd.DataFrame(columns=['a', 'b', 'C', 'D', 'e'])
#
# for i in range(1, 100):
#     add_data = pd.Series({'a': i, 'b': 1, 'C': 1, 'D': 1, 'e': 1})
#     # ignore_index=True不能少
#     df = df.append(add_data, ignore_index=True)
#
# f = df.sort_values(by='a', ascending=False)
from app.tData.getStockData import get_skData
import app.appUtil.Util_tools as t_util
from app.tData.RedisDB import RedisBase

# df = tuShare.get_realtime_quotes('000425')
# for index, cow in df.iterrows():
#     print(cow)

# price = df.loc[0, 'price']
# print(price)
# print(df)

# stock_data = get_skData().stock_b()

# flag = RedisBase().redis().set('stock_base', df_bytes)
# df = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))

# date:日期YYYY-MM-DD，默认为上一个交易日，目前只能提供2016-08-09之后的历史数据
stock_basics = tuShare.get_stock_basics('2020-02-28')
df = stock_basics.loc['000732']
start = datetime.datetime.now()
# daily_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_daily'))
# stock_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))
stock_details_daily = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_details_daily'))
end = datetime.datetime.now()
print('Running time: %s Seconds' % (end-start))

# print(daily_data)
print(tuShare.get_stock_basics())
# print(daily_data)
# r = 100 / 100
# print(round(r))
