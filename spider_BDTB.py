# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

# baidutieba_Spider
class BDTB(object):
	"""docstring for BDTB"""
	def __init__(self, baseUrl,seeLZ):
		self.baseUrl = baseUrl
		self.seeLZ = '?seelz=' + str(seeLZ)
		
	def getPage(self,pageNum):
		try:
			url = self.baseUrl + self.seeLZ + '&pn' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			# print response.read()
			# return response.read() # 这里应该返回可以正常阅读的内容
			return response.read().decode('utf-8') # utf-8解决输出乱码问题
		except urllib2.URLError, e:
			# raise e
			if hasattr(e,"reason"):
				print u"failed to connect the tieba,the reason is ",e.reason
				return None
	# 下面这段获取标题的函数，正则表达式部分存在bug
	def getTitle(self):
		page = self.getPage(1)		
		pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)	
		result = re.search(pattern,page)
		if result:
			print result.group(1)
			return result.group(1).strip()
		else:
			return None

	# 获取帖子页数，这个也有bug
	def getPagenum(self):
		page = self.getPage(1)
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,page)
		if result:
			print result.group(1)
			return result.group(1).strip()
		else:
			return None

	# 爬取正文内容
	def getContent(self):
		page = self.getPage(1)
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items = re.findall(pattern,page)
		for item in items:
			print item

baseURL = "http://tieba.baidu.com/p/3138733512"
bdtb = BDTB(baseURL,1)
# bdtb.getPage(1)
title = bdtb.getTitle()
page = bdtb.getPagenum()
content = bdtb.getContent()