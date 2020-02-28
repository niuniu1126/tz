class daily(object):

    def __init__(self, code):
        self.ts_code = code
        self.name = None  # 股票名称
        self.trade_date = None  # 交易日期
        self.open = None  # 开盘价
        self.close = None  # 当日收盘价
        self.pre_close = None  # 昨日收盘价
        self.price = None  # 实时价格
        self.high = None  # 最高
        self.low = None  # 最低
        self.change = None  # 涨幅
        self.pe = None  # 市盈率（总市值/净利润）
        self.pe_ttm = None  # 市盈率（TTM）
        self.pb = None  # 市净率（总市值/净资产）

