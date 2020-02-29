from app import config
from app.bean import daily_b
from app.tData.getStockData import get_skData
import pandas as pd
from app.tData.RedisDB import RedisBase
import app.appUtil.Util_tools as t_util
import datetime


class cal:

    def __init__(self):
        """Redis 数据初始化，取股票基本数据"""
        # self.stock_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))
        # self.daily_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_daily'))
        self.stock_details_daily = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_details_daily'))
        """高危版块"""
        self.list_industry = config.industry.split('|')

    # TODO 根据规则筛选并查询数据
    def _filter(self, daily_data, user_ts_code_list: list = None):
        dfNew = pd.DataFrame()

        """排除已选择的数据"""
        if user_ts_code_list is not None:
            self.stock_details_daily = \
                self.stock_details_daily[~self.stock_details_daily['ts_code'].isin(user_ts_code_list)]

        for index, row in self.stock_details_daily.iterrows():
            """市净率选择"""
            if row['industry'] in self.list_industry:
                bp_ulist = config.bh_.split(',')
            else:
                bp_ulist = config.bf_.split(',')

            bp_low = float(bp_ulist[0])  # 市净率 最小值
            bp_high = float(bp_ulist[1])  # 市净率 最大值

            if bp_low < row['pb'] < bp_high:  # 市盈率 市净率的10倍
                pe_ttm_high = row['pb'] * 10
                if 0 < row['pe_ttm'] < pe_ttm_high:
                    """ignore_index=True,表示不按原来的索引，从0开始自动递增"""
                    dfNew = dfNew.append(row, ignore_index=True)
        return dfNew

    # TODO 对数据进行排序
    def _sort(self, user_code_list: list = None, lines: int = None):
        # df.sort_index(by='pb', axis=0, ascending=[True])
        df = self._filter(self.stock_details_daily, user_ts_code_list=user_code_list)
        if df.empty is False:
            if lines is None:
                max_lines = int(config.max_lines)
            else:
                max_lines = lines
            """排序"""
            sort_title = config.sort_title.split('|')
            sort_type = config.sort_type.split('|')
            ndf = df.sort_values(by=sort_title, ascending=sort_type).head(max_lines)
        return ndf

    # TODO 对最终筛选股票
    def choose_stock(self, user_code_list: list = None, lines: int = None):
        df = self._sort(user_code_list=user_code_list, lines=lines)
        return df

    # TODO 获得当前股价
    def realtime_stock(self, user_code_list: list = None, lines: int = None):
        df = self._sort(user_code_list=user_code_list, lines=lines)
        if df.empty is False:
            stock_list = df['symbol'].tolist()
            data = get_skData.get_realtime_stock(stock_list)
            for index, cow in df.iterrows():
                now_data = data.loc[data['code'] == cow['symbol']]
                df.loc[index, 'price'] = float(now_data['price'])
        return df

    # TODO 计算分配个股数量
    def cal_every_stock(self, total_money: float, user_code_list: list = None, lines: int = None):
        t_money = total_money
        ndf = pd.DataFrame()
        fdf = pd.DataFrame()
        df = self.realtime_stock(user_code_list=user_code_list, lines=lines)
        df = df.drop(columns=['trade_date', 'pe'])
        """合计列"""
        sum_price = df['price'].sum()
        every_stock = total_money / sum_price
        """最小单位为1手，1手为100股，不够1手补足1手"""
        if every_stock < 100:
            e_stock = 100
        else:
            """四舍五入购买股票数量 计算超过100股 
            例: 不足150股时按照100股计算超过150时按照200股计算"""
            e_stock = round(every_stock / 100) * 100
        for index, row in df.iterrows():
            buy = row['price'] * e_stock
            row['buy_stock'] = e_stock
            row['buy_price'] = buy
            t_money = t_money - buy
            if t_money > 0:
                ndf = ndf.append(row, ignore_index=True)

        total = total_money - ndf['buy_price'].sum()

        if total > 0:
            for id, row in df.iterrows():
                cdf = ndf[ndf['symbol'] == row['symbol']]
                if cdf.empty:
                    buy = row['price'] * e_stock
                    if buy <= total:
                        row['buy_stock'] = e_stock
                        row['buy_price'] = buy
                        fdf = fdf.append(row, ignore_index=True)
            if fdf.empty:
                t_price = ndf.loc[0]['buy_price'] + total
                h_stock = t_price / ndf.loc[0]['price']
                b_stock = round(h_stock / 100) * 100
                ndf.loc[0, ['buy_stock']] = b_stock
                ndf.loc[0, ['price']] = b_stock * ndf.loc[0]['price']

        ndf = pd.concat([ndf, fdf], ignore_index=True)
        return ndf

    # TODO 筛选新个股
    def single_choose_stock(self, choose_code_list: list = None, lines: int = None):
        """
            choose_code_list 排除已选股票数
            lines 需要返回个股数量
        """
        choose_df = self.realtime_stock(user_code_list=choose_code_list, lines=lines)
        return choose_df

if __name__ == '__main__':
    cal = cal()
    dn = cal.choose_stock()
    # code_list = dn['ts_code'].tolist()
    # sdf = cal.choose_stock(code_list, lines=1)
    print(dn)
    # print(36000 - total)
    # start = datetime.datetime.now()
    # end = datetime.datetime.now()
    # print('Running time: %s Seconds' % (end-start))
