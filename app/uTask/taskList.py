from celery import Celery
from app.tData import initData
from app.uTask import celery

@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6)
def stock_base_stock_update(self):
    """沪深股市-初始化股票信息"""
    try:
        flag = initData.init_stock_data()
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
    return flag


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6)
def stock_base_stock_daily_data(self, In_flag=None):
    """各股每日指标"""
    try:
        flag_d = initData.init_stock_daily_data()
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
    return flag_d


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6)
def stock_base_stock_fi_data(self, In_flag=None):
    """各股基本财务数据"""
    try:
        flag_f = initData.init_stock_fi_data()  # 个股基本情况 由于接口取值通信问题 暂不更新
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
    return flag_f


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6, ignore_result=True)
def stock_base_stock_user_data(self):
    """用户使用股票数据"""
    flag_u = initData.init_stock_daily_user_details()  # 用户使用股票数据
    return flag_u

#auto_tasks
@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6)
def init_base_stock_data(self):
    try:
        flag = initData.init_stock_data()
        flag_d = initData.init_stock_daily_data()
        flag_u = initData.init_stock_daily_user_details()  # 用户使用股票数据
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
    print('init_stock_data', flag, '-------', 'init_stock_daily_data', flag_d, 'init_stock_daily_user_details', flag_u)