import pymongo
from time import sleep
from loguru import logger
from typing import List


def mongodb_duplicate_to_table_b(duplicate_service: List, after_duplicate_service: List, duplicate_name):
    """
    has error, don't use
    :param duplicate_service: [ip, db_name, table_name]
    :param after_duplicate_service: [ip, db_name, table_name]
    :return:
    """
    client = pymongo.MongoClient(duplicate_service[0])
    database = client[duplicate_service[1]]
    db_table = database[duplicate_service[2]]

    a_client =  pymongo.MongoClient(after_duplicate_service[0])
    a_database = client[after_duplicate_service[1]]
    a_db_table = database[after_duplicate_service[2]]

    for item in db_table.distinct(duplicate_name):
        before = db_table.find_one({duplicate_name: item}, {'_id': 0})
        a_db_table.insert_one(before)


def mongodb_duplicate(ip, db_name, table_name, duplicate_name):
    """
    对mongo数据库指定字段进行去重
    :param ip: 数据库ip
    :param db_name: 去重的数据库名
    :param table_name: 去重的表名
    :param duplicate_name: 去重的字段名
    :return duplicate_lst: 去重的数据
    """
    client = pymongo.MongoClient(ip)

    database = client[db_name]
    db_table = database[table_name]

    for item in db_table.distinct(duplicate_name):
        logger.info(f'first item: {item}')
        num = db_table.count_documents({duplicate_name: item})
        logger.info(f'first num is : {num}')

        if num != 1:
            repeating = db_table.find_one({duplicate_name: item})
            result = db_table.delete_many({duplicate_name: item})
            db_table.insert_one(repeating)
            logger.info(f'{item} Deduplication completed')

        else:
            logger.info(f'this {duplicate_name} is not repeated')
        logger.info('====================')


if __name__ == '__main__':
    ips = 'localhost:27017'
    db = 'picSearch2'
    table = 'pdd4'
    mongodb_duplicate(ips, db, table, 'url')
