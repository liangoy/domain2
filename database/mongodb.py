import pymongo
from config import config

client=pymongo.MongoClient(config.DB_LOGIN_STRING)
DB=client.domain

'''
digit6
'''
{
    'domain':'域名,主键',
    'status':'域名状态,默认""',
    'is_ours':'我们是否已经注册过了，1，0'
}