# -*- coding:utf-8 -*-

'''
Author:LeonWen
'''
# 实现保存到文本的功能，并进行格式化输出
import urllib
import urllib2
# import re
from bs4 import BeautifulSoup

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# set the headers
user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
headers = {'User-Agent':user_agent}
try:
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request)
    object_bs = BeautifulSoup(response.read())
    # print object_bs.prettify()
    # items 是一个list保存着返回结果
    items = object_bs.body.find_all("div",{"class":"article block untagged mb15"})
    # print items
    floor = 1
    tag = 0
    for item in items:
        if item.find("div",{"class":"thumb"}) == None:
            # class=thumb为带有图片的标签
            author = item.find("h2")
            upNum = item.find("i",{"class":"number"})
            content = item.find("div",{"class":"content"})
            # print content.prettify()
            # print content.text
            print u"===============",floor,u" 楼 ======================="
            print u"作者:",author.text
            print u"赞同数:",upNum.text
            print u"内容:",content.get_text()
            floor += 1
        else:
            tag += 1
    print u"图片个数:",tag
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
    # content = response.read().decode('utf-8')
    # pattern = re.compile('.*?(.*?).*?(.*?)',re.S)
    # items = re.findall(pattern,content)
    # for item in items:
    #     print item[0],item[1],item[2],item[3],item[4]
    #
    # pageContent = response.read().decode('utf-8')
    # # '<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>'
    # # authorPattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?title=(.*?)>.*?</a>')
    # authorPattern = re.compile('<atitle="(.*?)>"',re.S)
    # authorLists = re.findall(authorPattern,pageContent)
    # print authorLists
    #
    # timePattern = re.compile('',re.S)
    # timeLists = re.findall(timePattern,pageContent)
    #
    # upPattern = re.compile('',re.S)
    # upLists = re.findall(upPattern,pageContent)
    #
    # contentPattern = re.compile('<div.*?class="content">(.*?)</div>',re.S)
    # contentlists = re.findall(contentPattern,pageContent)
    # floor = 1
    # for author in authorlists:
    #     print floor,u'楼=========================='
    #     print author
    #     floor += 1
    # # print author[0]

# except urllib2.URLError,e:
#     # hasattr means if has the attribution
#     if hasattr(e,"code"):
#         print e.code
#     if hasattr(e,"reason"):
#         print e.reason