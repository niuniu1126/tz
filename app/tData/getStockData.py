from app import config
import tushare
import pandas as pd
from datetime import datetime, timedelta

from app.appUtil import Util_tools


class get_skData:
    def __init__(self):
        self.pro = tushare.pro_api(config.token)
        yesterday = (datetime.today() + timedelta(-1)).strftime('%Y%m%d')
        usr_date = Util_tools.dateTime_content('17:00')
        """17:00"""
        if datetime.today() > usr_date:
            self.default_day = usr_date.strftime('%Y%m%d')
        else:
            self.default_day = yesterday

    def stock_b(self, status=None):
        if status is None:
            status = 'L'
        data = self.pro.stock_basic(exchange='', list_status=status, fields='ts_code,symbol,name,area,industry,'
                                                                            'list_date')
        return data

    def daily_b(self, ts_code=None, tr_date=None):
        if tr_date is None:
            tr_date = self.default_day
        dbs = self.pro.daily_basic(ts_code=ts_code, trade_date=tr_date, fields='ts_code,close,trade_date,turnover_rate,'
                                                                               'volume_ratio,pe,pe_ttm,pb,ps,ps_ttm')
        return dbs

    @staticmethod
    def get_realtime_stock(ts_code):
        data = tushare.get_realtime_quotes(ts_code)
        return data

if __name__ == '__main__':
    # tr_data = get_skData().stock_b()
    # tr_data = get_skData.get_realtime_stock('000524')
    tr_data = get_skData().daily_b(ts_code='000732.SZ')
    # df = tushare.get_tick_data('000732', date='20200226', src='tt')
    # df2 = tr_data.drop_duplicates(subset=['industry'], keep='first')
    # for index, row in df2.iterrows():
    #     print(row['industry'])

    # print(tr_data.iloc[0]['price'])
    print(tr_data)