from requests import HTTPError

from app import config
import tushare
import pandas as pd
from datetime import datetime, timedelta

from app.appUtil import Util_tools


class get_skData:
    def __init__(self):
        self.pro = tushare.pro_api(config.token)
        yesterday = (datetime.today() + timedelta(-1))
        usr_date = Util_tools.dateTime_content('17:00')
        """17:00"""
        if datetime.today() > usr_date:
            self.default_day = usr_date
        else:
            self.default_day = yesterday

    def stock_b(self, status=None):
        """沪深股票"""
        if status is None:
            status = 'L'
        data = self.pro.stock_basic(exchange='', list_status=status, fields='ts_code,symbol,name,area,industry,'
                                                                            'list_date')
        return data

    def daily_b(self, ts_code=None, tr_date=None):
        """股票每日指标"""
        if tr_date is None:
            tr_date = self.default_day.strftime('%Y%m%d')
        dbs = self.pro.daily_basic(ts_code=ts_code, trade_date=tr_date, fields='ts_code,close,trade_date,turnover_rate,'
                                                                               'volume_ratio,pe,pe_ttm,pb,ps,ps_ttm')
        return dbs

    def daily_fina_indicator(self, ts_code=None, tr_date=None):
        """股票每日财务指标数据"""
        if tr_date is None:
            tr_date = self.default_day
        df = self.pro.query('fina_indicator', ts_code=ts_code, start_date=tr_date, end_date=tr_date)
        return df

    def get_stock_fi(self, ts_code=None, tr_date=None):
        """公司每日基本情况"""
        df_data = pd.DataFrame()
        if ts_code is None:
            if tr_date is None:
                tr_date = self.default_day.strftime('%Y%m%d')
            try:
                df_data = tushare.get_stock_basics(tr_date)
            except OSError:
                return df_data
            except HTTPError:
                return df_data
        else:
            start_data = Util_tools.data_util().get_last_year().get('start').strftime('%Y%m%d')
            end_date = Util_tools.data_util().get_now_year().get('end').strftime('%Y%m%d')
            df_data = self.pro.query('fina_indicator', ts_code=ts_code, start_date=start_data, end_date=end_date)
            df_data = df_data[:1]

        return df_data

    @staticmethod
    def get_realtime_stock(ts_code):
        """股票交易金额"""
        df_data = tushare.get_realtime_quotes(ts_code)
        return df_data

if __name__ == '__main__':
    # tr_data = get_skData().stock_b()
    # tr_data = get_skData.get_realtime_stock('000524')
    # tr_data = get_skData().daily_b(ts_code='000732.SZ')
    # df = tushare.get_tick_data('000732', date='20200226', src='tt')
    # df2 = tr_data.drop_duplicates(subset=['industry'], keep='first')
    # for index, row in df2.iterrows():
    #     print(row['industry'])

    # print(tr_data.iloc[0]['price'])
    # data = get_skData().get_stock_fi('000732.SZ')
    data = get_skData().get_stock_fi()
    print(data)
    # for index, row in data.iterrows():
    #     print(row)
    #     print(row['bps'])
