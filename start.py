# coding=utf-8
from article import login
from article import articles
import os
import configparser
import json

def main():
    # 检查是否有cookies.json文件
    if not os.path.isfile('./cookies.json'):
        cell, pwd = parse_config()
        l = login.Login()
        l.run(cell, pwd, '86')

    # 创建下载数据的目录
    out_dir = './all_files'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # 获取所有的课程列表
    article = articles.ArticlesApi()
    course_list = article.get_course_list()
    if not os.path.isfile(os.path.join(out_dir, 'course_list.json')):
        with open(os.path.join(out_dir, 'course_list.json'), 'w') as f:
            f.write(json.dumps(course_list))
    print(course_list)

    # 循环课程列表获取每个课程的简介，建立目录
    for index, value in course_list.items():
        print(index, value)

def parse_config():
    """
    通过读取.env配置项文件 解析配置项数据
    :return: 返回手机号码和密码
    """
    conf = configparser.ConfigParser()
    conf.read('.env')
    cell = conf.get('login', 'cell')
    pwd = conf.get('login', 'password')
    return cell, pwd


if __name__ == '__main__':
    main()