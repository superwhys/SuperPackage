#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @File    ：FeishuSend.py
# @IDE     ：PyCharm 
# @Author  ：SuperYong
# @Date    ：2021/10/26 14:58 
# @Summary : this is the summary 
import requests

def SendFeishu(data_text):
    feishu_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/0ceedf5e-1b0c-4727-8c06-064537743102'
    data = {"msg_type": "text",
            "content": {"text": dumps(data_text, indent=2, ensure_ascii=False)}}
    requests.post(feishu_url, json=data)