# coding=utf-8

import os
import requests


class Mp3Download:
    def __init__(self):
        pass

    def run(self, mp3_url, out_file, out_dir):
        """
        mp3_url 下载mp3的URL地址
        out_file 保存的文件名称
        out_dir  保存的文件目录
        下载mp3文件到本地
        """
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        res = requests.get(mp3_url)
        with open(os.path.join(out_dir, out_file), 'wb') as f:
            f.write(res.content)
