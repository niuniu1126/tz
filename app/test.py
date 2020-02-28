import tushare
import numpy  as np

from app import config


def get_data(gid, start=None, end=None):
    gdata = tushare.get_k_data(gid, start, end)
    return gdata

def get_data_today():
    gdata = tushare.get_today_all()
    return gdata

if __name__ == '__main__':
    token = config.token
    pro = tushare.pro_api(token)
    # data = tushare.get_k_data('000425', '2020-02-18',  '2020-02-18') data = get_data_today() df = pro.daily_basic(
    # ts_code='000029.SZ', trade_date='20200221', fields='ts_code,close,trade_date,turnover_rate,volume_ratio,pe,
    # pb') print(df) df = pro.cctv_news(date='20200220') df = pro.bo_monthly(date='20200220')

    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    dbs = pro.daily_basic(ts_code='', trade_date='20200221', fields='ts_code,close,trade_date,turnover_rate,'
                                                                    'volume_ratio,pe,pe_ttm,pb,ps,ps_ttm')
    # print(daily_bases[daily_bases['ts_code'] == '600708.SH'])

    for index, row in data.iterrows():
        df = dbs[dbs['ts_code'] == row['ts_code']]
        if df.empty is False:
            df.fillna(value=0)
            if 0 < float(df['pe_ttm']) < 4 and 0.6 < float(df['pb']) < 2:
                print(index, row['ts_code'], row['symbol'], row['name'], row['industry'],)
                print(df)
