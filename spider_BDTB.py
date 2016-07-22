# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

# 去除非法标签工具
class Tool(object):
    # remove image tag,7 long space?
    # removeImg = re.compile('<img [/S*( )*]*src="(/S+)" [/S*( )*]*/>') # 这样的正则表达也可以
    removeImg = re.compile('<img.*?>| {7}|') # 这里之所以一直有错，是因为<img>的标签没有右侧闭合
    # remove super address link
    removeAddr = re.compile('<a.*?>|</a>')
    # 将换行的标签替换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将制表符<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将段落开头换为\n加两个空格
    replacePara = re.compile('<p.*?>')
    # 将其与标签删除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n  ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)

        # strip函数将前后多余内容删除
        return x.strip()

# baidutieba_Spider
class BDTB(object):
	"""docstring for BDTB"""
	def __init__(self, baseURL,seeLZ,floorTag):
		self.baseUrl = baseURL
		self.seeLZ = '?see_lz=' + str(seeLZ) # 之前的链接一直是错的，但是也还是打开了，因为百度服务器是识别链接了
		# HTML标签剔除工具类 对象
		self.tool = Tool()
		# 全局file变量，文件写入操作对象
		self.file = None
		# 楼层标号，初始为1
		self.floor = 1
		# 默认标题
		self.defaultTitle = u"百度贴吧"
		# 是否写入楼分隔符标记
		self.floorTag = floorTag

	def getPage(self,pageNum):
		try:
			# get the url
			url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
			print u"链接地址:",url
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
	def getTitle(self,page):
		# page = self.getPage(1)
		pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
		result = re.search(pattern,page)
		if result:
			print result.group(1)
			return result.group(1).strip()
		else:
			return None

	# 获取帖子页数
	def getPagenum(self,page):
		# page = self.getPage(1)
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,page)
		if result:
			print result.group(1)
			return result.group(1).strip()
		else:
			return None

	def getContent(self,page):
		# page = self.getPage(1)
		# re.S 参数的作用是将匹配适用于整个字符串，超越\n的限制
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items = re.findall(pattern,page) # findall 返回的是list
		contents = []
		# floor = 1
		for item in items:
			# print floor,u"楼==================================================================="
			# remove the tag from text
			content = "\n" + self.tool.replace(item) + "\n"
			# content = self.tool.replace(item)
			# print content
			contents.append(content.encode('utf-8'))
			# floor += 1
		return contents

	def setFileTitle(self,title):
		if title is not None:
			self.file = open(title + ".txt","w+")
		else:
			self.file = open(self.defaultTitle + ".txt","w+")

	def writeData(self,contents):
		for item in contents:
			# 如果floorTag是由手动键入信息，则需要考虑字符串转换
			if self.floorTag == 1:
				floorLine = '\n' + str(self.floor) + u'====================================='
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPagenum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print "can not connect the URL,plz try again"
			return
		try:
			print u"该帖子共有" + str(pageNum) + u"页"
			for i in range(1,int(pageNum) + 1):
				print u"正在写入第" + str(i) + u"页数据"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError, e:
			# raise e
			print u"写入异常，原因：" + e.message
		finally:
			print u"写入任务完成"


# baseURL = "http://tieba.baidu.com/p/3138733512"
# bdtb = BDTB(baseURL,1)
# # bdtb.getPage(1)
# # title = bdtb.getTitle()
# # page = bdtb.getPagenum()
# content = bdtb.getContent()

baseURL = "http://tieba.baidu.com/p/3138733512"
seeLZ = 1
floorTag = 1
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()