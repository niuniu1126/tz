from app import config
from app.bean import daily_b
from app.tData.getStockData import get_skData
import pandas as pd
from app.tData.RedisDB import RedisBase
import app.appUtil.Util_tools as t_util

class cal:

    def __init__(self):
        """Redis 数据初始化，取股票基本数据"""
        self.stock_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_base'))
        self.daily_data = t_util.bytes_to_dataFrame(RedisBase().redis().get('stock_daily'))

    # TODO 根据规则筛选并查询数据
    def _filter(self):
        dfNew = pd.DataFrame()
        for index, row in self.stock_data.iterrows():
            df = self.daily_data[self.daily_data['ts_code'] == row['ts_code']]
            list_industry = config.industry.split('|')
            if df.empty is False:
                if 'ST' in row['name']:  # 排除带有ST的股票
                    continue
                df.fillna(value=0)  # 当数据中存在NaN时候用 0 替换
                if row['industry'] in list_industry:
                    bp_ulist = config.bh_.split(',')
                else:
                    bp_ulist = config.bf_.split(',')
                daily_b.ts_code = str(row['ts_code'])  # 股票代码
                daily_b.name = str(row['name'])  # 股票名称
                for rw in df['trade_date']:
                    daily_b.trade_date = str(rw)  # 交易日期
                daily_b.close = float(df['close'])  # 当日收盘价
                daily_b.pe = float(df['pe'])  # 市盈率（总市值/净利润）
                daily_b.pe_ttm = float(df['pe_ttm'])  # 市盈率（TTM）
                daily_b.pb = float(df['pb'])  # 市净率（总市值/净资产）

                bp_low = float(bp_ulist[0])  # 市净率 最小值
                bp_high = float(bp_ulist[1])  # 市净率 最大值

                if bp_low < daily_b.pb < bp_high:  # 市盈率 市净率的10倍
                    pe_ttm_high = daily_b.pb * 10
                    if 0 < daily_b.pe_ttm < pe_ttm_high:
                        data = {'ts_code': daily_b.ts_code, 'symbol': row['symbol'], 'name': daily_b.name,
                                'industry': row['industry'], 'trade_date': daily_b.trade_date, 'pe': daily_b.pe,
                                'pe_ttm': daily_b.pe_ttm, 'pb': daily_b.pb}
                        add_data = pd.Series(data)
                        """ignore_index=True,表示不按原来的索引，从0开始自动递增"""
                        dfNew = dfNew.append(add_data, ignore_index=True)
        return dfNew

    # TODO 对数据进行排序
    def _sort(self):
        # df.sort_index(by='pb', axis=0, ascending=[True])
        df = self._filter()
        if df.empty is False:
            max_lines = int(config.max_lines)
            sort_title = config.sort_title.split('|')
            sort_type = config.sort_type.split('|')
            ndf = df.sort_values(by=sort_title, ascending=sort_type).head(max_lines)
        return ndf

    # TODO 获得当前股价
    def realtime_stock(self):
        df = self._sort()
        if df.empty is False:
            stock_list = df['symbol'].tolist()
            data = get_skData.get_realtime_stock(stock_list)
            for index, cow in df.iterrows():
                now_data = data.loc[data['code'] == cow['symbol']]
                df.loc[index, 'price'] = float(now_data['price'])
        return df

    # TODO 计算分配个股数量
    def cal_every_stock(self, total_money: float):
        df = self.realtime_stock()
        ndf = df.drop(columns=['trade_date', 'pe'])
        """合计列"""
        sum_price = df['price'].sum()
        every_stock = total_money / sum_price
        """最小单位为1手，1手为100股，不够1手补足1手"""
        if every_stock < 100:
            e_stock = 100
        else:
            e_stock = round(every_stock / 100) * 100
        for index, cow in ndf.iterrows():
            buy = cow['price'] * e_stock
            ndf.loc[index, 'buy_stock', 'buy_price'] = [index, e_stock, buy]
        return every_stock


if __name__ == '__main__':
    dn = cal().cal_every_stock(10000)
    print(dn)
