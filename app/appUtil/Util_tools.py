import pandas as pd
import pickle
import datetime
import time


# TODO DataFrame 序列化为 Byte
def dataFrame_to_bytes(df):
    df_bytes = pickle.dumps(df)
    return df_bytes


# TODO 将Byte反序列化为DataFrame类型
def bytes_to_dataFrame(rdf_Name):
    r_df = pickle.loads(rdf_Name)
    return r_df


# TODO 根据日期时间格式返回日期类型
def dateTime_content(itime, date=None):
    if date is None:
        date = str(datetime.date.today())
    d_time = datetime.datetime.strptime(date + itime, '%Y-%m-%d%H:%M')
    return d_time

# TODO 日期差
def time_long(time1, time2, type="day"):
    """
    计算时间差
    :param time1: 较小的时间（datetime类型）
    :param time2: 较大的时间（datetime类型）
    :param type: 返回结果的时间类型（暂时就是返回相差天数）
    :return: 相差的天数
    """
    day1 = time.strptime(str(time1), '%Y%m%d')
    day2 = time.strptime(str(time2), '%Y%m%d')
    if type == 'day':
        day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (
                24 * 60 * 60)
    return abs(int(day_num))

class data_util:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.this_year_start = datetime.datetime(self.now.year, 1, 1)

    # TODO 算上一个季度开始结束日期，返回字典类型
    def get_last_quarter(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        this_quarter_start = datetime.datetime(self.now.year, month, 1)
        last_quarter_end = this_quarter_start - datetime.timedelta(days=1)
        last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)
        tdic = {'start': last_quarter_start, 'end': last_quarter_end}
        return tdic

    # TODO 去年第一天和最后一天，返回字典类型
    def get_last_year(self):
        last_year_end = self.this_year_start - datetime.timedelta(days=1)
        last_year_start = datetime.datetime(last_year_end.year, 1, 1)
        tdic = {'start': last_year_start, 'end': last_year_end}
        return tdic

    # TODO 本年第一天和最后一天，返回字典类型
    def get_now_year(self):
        this_year_end = datetime.datetime(self.now.year + 1, 1, 1) - datetime.timedelta(days=1)
        tdic = {'start': self.this_year_start, 'end': this_year_end}
        return tdic


if __name__ == '__main__':
    dataTime = dateTime_content('17:00')
    print(dataTime)
    # days = time_long('20200227', '20200327')
    days = data_util().get_now_year()
    print(days)
