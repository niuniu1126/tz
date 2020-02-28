import pandas as pd
import tushare as tuShare

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
# df_bytes = t_util.dataFrame_to_bytes(stock_data)
# # df_bytes = stock_data.to_msgpack()
# flag = RedisBase().redis().set('stock_base', df_bytes)

df = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))

print(df)

r = 100 / 100
print(round(r))
