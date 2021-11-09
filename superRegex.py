#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @File    ：superRegex.py
# @IDE     ：PyCharm 
# @Author  ：SuperYong
# @Date    ：2021/11/9 11:27 
# @Summary : this is the summary 

CHINESE_REGEX = r'[\u4e00-\u9fa5]+'
DATE_REGEX = r'^\d{4}-\d{1,2}-\d{1,2}'
SPACE_LINE_RE = r'\n\s*\r'
IP_RE = r'\d+\.\d+\.\d+\.\d+'