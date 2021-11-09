#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @File    ：mongo_utils.py
# @IDE     ：PyCharm 
# @Author  ：SuperYong
# @Date    ：2021/9/10 11:03 
# @Summary : this is the summary
from pymongo.collection import Collection
from pymongo import MongoClient
from datetime import datetime
from loguru import logger
from bson import ObjectId


def create_mongo_object_id(t):
    """
    根据指定时间创建mongo中的ObjectId
    :param t: 创建ObjectId 的时间
    :return:
    """
    if isinstance(t, datetime):
        _time = t.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'create ObjectId by: {_time}')
        return ObjectId.from_datetime(t)

    if len(t.split(' ')) == 2:
        try:
            gen_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ('params error, need %Y-%m-%d %h:%m:%s')
    else:
        try:
            gen_time = datetime.strptime(t, '%Y-%m-%d')
        except ValueError:
            raise('params error, need %Y-%m-%d')
    logger.info(f'create ObjectId by: {t}')
    return ObjectId.from_datetime(gen_time)

def check_index(table: Collection, *args):
    """
    check if the index is in table
    :param table:
    :param args: the index if has more than one arg, it represent COMPOUND
    :return: True in table, False not in table
    """
    indexes = set(args)
    index_dic = table.index_information()
    mongo_index_lst = []
    for index_key in index_dic:
        mongo_index_lst.append({key[0] for key in index_dic[index_key]['key']})
    if indexes in mongo_index_lst:
        return True
    return False

def create_index(table: Collection, index_lst: list, unique: bool, sort=1):
    if not check_index(table, *index_lst):
        index_config = [(name, sort) for name in index_lst]
        ok = table.create_index(index_config, unique=unique, background=True)
        logger.info(f'index create success, index name is {ok}')
    else:
        logger.error(f'index_name: {",".join(index_lst)} has been create!')


if __name__ == '__main__':
    # t = '2021-09-09 22:30:20'
    # print(create_mongo_object_id(t))
    con = MongoClient("localhost:27017")
    table = con['source_data']['pdd_url']
    create_index(table=table, index_lst=["tag"], unique=False, sort=1)