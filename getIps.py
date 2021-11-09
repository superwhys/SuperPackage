#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @File    ：getIps.py
# @IDE     ：PyCharm 
# @Author  ：SuperYong
# @Date    ：2021/10/14 16:42 
# @Summary : get the consuld ips
from .consul_util import ConsulUtil
from loguru import logger

def get_ips(service_name):
    cu = ConsulUtil()
    ip = cu.get_address(service_name=service_name)
    logger.debug(f'{service_name} --> {ip}')
    return ip