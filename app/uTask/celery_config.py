from datetime import timedelta

# Celery configuration
BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

CELERY_TIMEZONE = 'Asia/Shanghai'

# 所有异步执行的任务
IMPORT_TASKS = (
    'uTask.taskList',
)
#>celery -A app.uTask.taskList beat
CELERYBEAT_SCHEDULE = {
    'add-every-hours': {
        'task': 'app.uTask.taskList.init_base_stock_data',
        'schedule': timedelta(hours=1),
        "args": ()
    },

    'add-every-minute': {
        'task': 'app.uTask.taskList.stock_base_stock_user_data',
        'schedule': timedelta(minutes=10),
        "args": ()
    }
}