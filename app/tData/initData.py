from app.tData.getStockData import get_skData
import app.appUtil.Util_tools as t_util
from app.tData.RedisDB import RedisBase
import pandas as pd
from app.bean import daily_b

# TODO 初始化股票信息
def init_stock_data():
    stock_data = get_skData().stock_b()
    # 排除劣质股
    sdf = stock_data[stock_data['name'].str.contains(r'.*ST.*')]
    stock_data.drop(sdf.index, inplace=True)
    stock_data.fillna(value=0)  # 当数据中存在NaN时候用 0 替换
    df_bytes = t_util.dataFrame_to_bytes(stock_data)
    flag = RedisBase().redis().set('stock_base', df_bytes)
    return flag

# TODO 初始化个股每日指标 需要每日更新
def init_stock_daily_data():
    # 股票每日指标数据
    daily_data = get_skData().daily_b()
    df_bytes = t_util.dataFrame_to_bytes(daily_data)
    flag = RedisBase().redis().set('stock_daily', df_bytes)
    return flag

# TODO 初始化个股基本情况 需要每日更新
def init_stock_fi_data():
    # 股票每日基本数据
    try:
        daily_data = get_skData().get_stock_fi()
        if daily_data.empty is False:
            df_bytes = t_util.dataFrame_to_bytes(daily_data)
            flag = RedisBase().redis().set('stock_fi', df_bytes)
        else:
            flag = False
    except Exception as e:
        print(e.args)
        flag = False
    return flag

# TODO 初始化用户使用股票数据 需要每日更新
def init_stock_daily_user_details():
    # 股票组装用户数据
    stock_details_daily = _init_stock_daily_udata()
    df_bytes = t_util.dataFrame_to_bytes(stock_details_daily)
    flag = RedisBase().redis().set('stock_details_daily', df_bytes)
    return flag

# TODO 初始化个股基本情况 需要每日更新
def init_everyday():
    flag_d = init_stock_daily_data()  # 每日指标
    flag_f = init_stock_fi_data()  # 个股基本情况 由于接口取值通信问题 暂不更新
    flag_u = init_stock_daily_user_details()  # 用户使用股票数据
    print(flag_d, '-----', flag_f, '-----', flag_u)

# TODO 初始化个股详细数据 需要每日更新
def _init_stock_daily_udata():
    new_df = pd.DataFrame()
    # 股票基本分类数据
    stock_base = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))
    stock_daily = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_daily'))
    stock_fi = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_fi'))
    for index, row in stock_base.iterrows():
        df = stock_daily[stock_daily['ts_code'] == row['ts_code']]
        if stock_fi.empty is False:
            bvps = stock_fi.loc[row['symbol']]['bvps']
        if df.empty is False:
            daily_b.ts_code = str(row['ts_code'])  # 股票名称
            daily_b.name = str(row['name'])  # 股票名称
            daily_b.symbol = str(row['symbol'])  # 股票名称
            daily_b.industry = str(row['industry'])  # 股票名称
            daily_b.trade_date = str(df.loc[df.index, 'trade_date'].values[0])  # 交易日期
            daily_b.close = float(df['close'])  # 当日收盘价
            daily_b.ts_code = str(row['ts_code'])  # 股票代码
            daily_b.pe = float(df['pe'])  # 市盈率（总市值/净利润）
            daily_b.pe_ttm = float(df['pe_ttm'])  # 市盈率（TTM）
            daily_b.pb = float(df['pb'])  # 市净率（总市值/净资产）
            if bvps is None:
                daily_b.bps = float(0)  # 每股净资产
            else:
                daily_b.bps = float(bvps)  # 每股净资产

            data = {'ts_code': daily_b.ts_code, 'symbol': daily_b.symbol, 'name': daily_b.name,
                    'industry': daily_b.industry, 'trade_date': daily_b.trade_date, 'pe': daily_b.pe,
                    'pe_ttm': daily_b.pe_ttm, 'pb': daily_b.pb, 'bps': daily_b.bps}
            add_data = pd.Series(data)
            """ignore_index=True,表示不按原来的索引，从0开始自动递增"""
            new_df = new_df.append(add_data, ignore_index=True)
    return new_df


if __name__ == '__main__':
    # print(init_stock_data())
    # print(init_stock_fi_data())
    print(init_stock_fi_data())
    # init_everyday()