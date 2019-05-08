# coding=utf-8

import os
import requests
import json


class ArticlesApi:
    def __init__(self):
        """
        初始化操作
        """
        self.cookies = None
        self._cookies_file = os.path.join('..', 'cookies.json')

        if os.path.exists(self._cookies_file):
            with open(self._cookies_file) as f:
                cookies = f.read()
                self.cookies = json.load(cookies) if cookies else None

    def get_course_list(self):
        """
        获取课程列表
        :return: 获取所有的课程列表数据
        """
        url = 'https://time.geekbang.org/serv/v1/column/all'

        headers = {
            'Referer': 'https://time.geekbang.org/paid-content',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        resp = requests.get(url, headers=headers, cookies=self.cookies)

        if not (resp.status_code == 200 and resp.json().get('code') == 0):
            raise Exception('course query fail:' + resp.json()['error']['msg'])

        return resp.json()['data']

    def get_course_content(self, course_id):
        """
        获取课程所有的章节数据
        :param course_id: 课程ID
        :return: 课程章节数据
        """
        url = 'https://time.geekbang.org/serv/v1/column/articles'

        headers = {
            'Referer': 'https://time.geekbang.org/column/{}'.format(str(course_id)),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        data = {"cid": str(course_id), "size": 1000, "prev": 0, "order": "newest"}

        resp = requests.post(url, json=data, cookies=self.cookies, headers=headers, timeout=10)

        if not (resp.status_code == 200 and resp.json().get('code') == 0):
            raise Exception('course query fail:' + resp.json()['error']['msg'])
        if not data:
            raise Exception('course not exists:%s' % course_id)

        return resp.json()['data']['list'][::-1]

    def get_course_intro(self, course_id):
        """
        获取课程简介
        :param course_id: 课程ID
        :return: 课程简介数据
        """
        url = 'https://time.geekbang.org/serv/v1/column/intro'

        headers = {
            'Referer': 'https://time.geekbang.org/column/{}'.format(course_id),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        data = {'cid': str(course_id)}

        resp = requests.post(url, headers=headers, json=data, cookies=self.cookies, timeout=10)

        if not (resp.status_code == 200 and resp.json().get('code') == 0):
            raise Exception('course query fail:' + resp.json()['error']['msg'])
        res = resp.json()['data']
        if not res:
            raise Exception('course not exists:%s' % course_id)

        return res

    def get_chapter_content(self, chapter_id):
        """
        获取课程章节详情
        :param chapter_id: 课程章节ID
        :return: 课程章节详细数据
        """
        url = 'https://time.geekbang.org/serv/v1/article'

        headers = {
            'Referer': 'https://time.geekbang.org/column/article/{}'.format(str(chapter_id)),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        data = {"id": str(chapter_id)}

        resp = requests.post(url, json=data, headers=headers, cookies=self.cookies, timeout=10)

        if not (resp.status_code == 200 and resp.json().get('code') == 0):
            raise Exception('course query fail:' + resp.json()['error']['msg'])

        return resp.json()['data']
