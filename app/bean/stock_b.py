class stock_all(object):

    def __init__(self, code):
        self.ts_code = code
        self.symbol = None  # 股票代码
        self.name = None  # 股票名称
        self.area = None  # 所在地域
        self.industry = None  # 所属行业
        self.market = None  # 市场类型 （主板/中小板/创业板/科创板）
        self.list_status = None  # 上市状态： L上市 D退市 P暂停上市
        self.list_date = None  # 上市日期
        self.delist_date = None  # 退市日期

