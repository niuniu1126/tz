import time

from app.uTask import taskList
from celery.result import AsyncResult
from celery import Celery, chain, group


# 启动celery
# celery -A app.uTask.taskList worker -l info -P eventlet

# 启动celery后台管理工具 flower 命令
# celery flower --address=0.0.0.0 --port=555 --broker=redis://127.0.0.1:6379/1

# TODO 初始化更新沪深股票
def stock_base_task():
    """沪深股市-初始化股票信息"""
    tasks_id = taskList.stock_base_stock_update.AsyncResult()
    return tasks_id

# TODO 更新各股每日指标 每日更新
def stock_daily_data_task():
    """各股每日指标"""
    # tasks_id = taskList.stock_base_stock_daily_data.delay()
    # result = taskList.stock_base_stock_daily_data.apply_async(args=(), link=taskList.stock_base_stock_user_data.s())
    result = chain(taskList.stock_base_stock_daily_data.s() | taskList.stock_base_stock_user_data.s())()
    # return tasks_id
    return result

# TODO 更新各股财务数据 每日更新
def stock_fi_data_task():
    """各股基本财务数据"""
    tasks_id = taskList.stock_base_stock_fi_data.delay()
    return tasks_id

# TODO  整理用户使用股票数据格式 每日更新
def stock_user_data_task():
    """用户使用股票数据"""
    tasks_id = taskList.stock_base_stock_user_data.delay()
    return tasks_id

if __name__ == '__main__':
    # r1 = stock_base_task()
    r2 = stock_daily_data_task()
    # # r3 = stock_fi_data_task()
    # while 1:
    #     finished = r2.ready()
    #     print(finished)
    #     time.sleep(2)
    print(r2)
    # res = AsyncResult(r2)
    # res = group(stock_daily_data_task(), stock_user_data_task())()
    # if res.successful():
    #     while 1:
    #         try:
    #
    #             if res.status == 'SUCCESS':
    #                 r4 = stock_user_data_task()
    #                 break
    #             if res.result == 'False':
    #                 break
    #         except Exception as e:
    #             time.sleep(1)

    # print(res.status, '----', res.result)
    # print(res)