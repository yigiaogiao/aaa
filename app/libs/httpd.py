# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/2/13 14:52
'''
requests获取http请求再对异常状态进行处理，最后根据需要返回对应的数据格式
'''
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text