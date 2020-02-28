from app.tData.getStockData import get_skData
import app.appUtil.Util_tools as t_util
from app.tData.RedisDB import RedisBase

# 初始化股票信息
def init_stock_data():
    stock_data = get_skData().stock_b()
    df_bytes = t_util.dataFrame_to_bytes(stock_data)
    flag = RedisBase().redis().set('stock_base', df_bytes)
    return flag

# 初始化个股详细数据 需要每日更新
def init_stock_daily_data():
    daily_data = get_skData().daily_b()
    df_bytes = t_util.dataFrame_to_bytes(daily_data)
    flag = RedisBase().redis().set('stock_daily', df_bytes)
    return flag


if __name__ == '__main__':
    print(init_stock_data())
    print(init_stock_daily_data())