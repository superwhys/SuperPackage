#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @File    ：mongo_utils.py
# @IDE     ：PyCharm 
# @Author  ：SuperYong
# @Date    ：2021/9/10 11:03 
# @Summary : this is the summary 

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


if __name__ == '__main__':
    t = '2021-09-09 22:30:20'
    print(create_mongo_object_id(t))