from celery import Celery
from app.tData import initData
from app.uTask import celery_config

celery = Celery('app.uTask.taskList', broker=celery_config.CELERY_BROKER_URL,
                backend=celery_config.CELERY_RESULT_BACKEND)


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6, property=0)
def stock_base_stock_update(self):
    """沪深股市-初始化股票信息"""
    try:
        flag = initData.init_stock_data()
    except Exception as e:
        raise self.retry(exc=e, countdown=3)
    return flag


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6, property=0)
def stock_base_stock_daily_data(self, In_flag=None):
    """各股每日指标"""
    try:
        flag = initData.init_stock_daily_data()
    except Exception as e:
        raise self.retry(exc=e, countdown=3)
    return flag


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6, property=0)
def stock_base_stock_fi_data(self, In_flag=None):
    """各股基本财务数据"""
    try:
        flag_f = initData.init_stock_fi_data()  # 个股基本情况 由于接口取值通信问题 暂不更新
    except Exception as e:
        raise self.retry(exc=e, countdown=3)
    return flag_f


@celery.task(bind=True, max_retries=3, default_retry_delay=1 * 6, property=1)
def stock_base_stock_user_data(self):
    """用户使用股票数据"""
    try:
        flag_u = initData.init_stock_daily_user_details()  # 用户使用股票数据
    except Exception as e:
        raise self.retry(exc=e, countdown=3)
    return flag_u
