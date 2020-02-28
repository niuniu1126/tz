import redis

from app.tData import dbConfig


class RedisBase:

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, "instance"):
            cls.instance = super(RedisBase, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        """每一个数据库实例管理一个连接池"""
        pool = redis.ConnectionPool(host=dbConfig.Redis_URL, port=dbConfig.Redis_Port,
                                    db=dbConfig.Redis_Db, password=dbConfig.Redis_Pwd)
        self.r = redis.Redis(connection_pool=pool)

    def redis(self):
        return self.r

    # class RedisUtil(RedisBase):
#
#     def set(self, key, value):
#         """设置值"""
#         return self.r.set(key, value)
#
#     def get(self, key):
#         """获取值"""
#         return self.r.get(key)
#
#     def delete(self, key):
#         """删除键值"""
#         return self.r.delete(key)
#
#     def incr(self, key, value):
#         """插入键值"""
#         return self.r.incr(key, value)

if __name__ == '__main__':
    rb = RedisBase().redis().set('hello', '这是一句话')
    print(rb)
