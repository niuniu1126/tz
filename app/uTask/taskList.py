from app.tData.getStockData import get_skData
from app.tData.RedisDB import RedisBase
import app.appUtil.Util_tools as t_util
from celery import Celery

from app.uTask import celery_config

celery = Celery('app.uTask.taskList', broker=celery_config.CELERY_BROKER_URL,
                backend=celery_config.CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def stock_base_everyday_update():
    stock_data = get_skData().stock_b()
    df_bytes = t_util.dataFrame_to_bytes(stock_data)
    flag = RedisBase().redis().set('stock_base', df_bytes)
    return flag