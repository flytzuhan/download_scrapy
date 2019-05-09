# coding=utf-8
from article import login
from article import articles
from utils import m3u8_download
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
    # print(course_list)

    # 循环课程列表获取每个课程的简介，建立目录
    for index, value in course_list.items():
        if index == '3': # 下载视频
            m3u8 = m3u8_download.M3u8Download()
            for item in value['list']:
                dir_name = item['column_title']
                # 判断文件目录是否存在
                if not os.path.isdir(os.path.join(out_dir, dir_name)):
                    os.makedirs(os.path.join(out_dir, dir_name))
                # 获取课程的所有内容
                content = article.get_course_content(item['id'])
                if not os.path.isfile(os.path.join(out_dir+'/'+dir_name, 'content_list.json')):
                    with open(os.path.join(out_dir+'/'+dir_name, 'content_list.json'), 'w') as f:
                        f.write(json.dumps(content))

                # 获取每个章节的详细信息
                if int(item['id']) in [98]:
                    for chapter in content:
                        chapter_content = article.get_chapter_content(chapter['id'])
                        print(chapter_content)
                        m3u8.run(chapter_content['video_media_map']['ld']['url'], os.path.join(out_dir, dir_name), chapter_content['article_sharetitle'])

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