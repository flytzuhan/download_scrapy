# coding=utf-8

import requests
import os
import json


class Login:
    def __init__(self):
        self._cookies_file = os.path.join('.', 'cookies.json')

    def run(self, acc, pwd, area='86'):
        """
        登录接口
        :param acc: 
        :param pwd: 
        :param area: 
        :return: 
        """
        url = 'https://account.geekbang.org/account/ticket/login'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Host': 'account.geekbang.org',
            'Referer': 'https://account.geekbang.org/signin?redirect=https%3A%2F%2Fwww.geekbang.org%2F',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        data = {
            "country": area,
            "cellphone": acc,
            "password": pwd,
            "captcha": "",
            "remember": 1,
            "platform": 3,
            "appid": 1
        }

        resp = requests.post(url=url, json=data, headers=headers, timeout=10)

        if not (resp.status_code == 200 and resp.json().get('code') == 0):
            raise Exception('login fail:' + resp.json()['error']['msg'])

        cookies = dict(resp.cookies.items())
        with open(self._cookies_file, 'w') as f:
            f.write(json.dumps(cookies))
