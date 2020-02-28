import pandas as pd
import pickle
import datetime


# TODO DataFrame 序列化为 Byte
def dataFrame_to_bytes(df):
    df_bytes = pickle.dumps(df)
    return df_bytes


# TODO 将Byte反序列化为DataFrame类型
def bytes_to_dataFrame(rdf_Name):
    r_df = pickle.loads(rdf_Name)
    return r_df


# TODO 根据日期时间格式返回日期类型
def dateTime_content(time, date=None):
    if date is None:
        date = str(datetime.date.today())
    d_time = datetime.datetime.strptime(date + time, '%Y-%m-%d%H:%M')
    return d_time


if __name__ == '__main__':
    dataTime = dateTime_content('17:00')
    print(dataTime)
