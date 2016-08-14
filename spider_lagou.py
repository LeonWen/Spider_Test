# -*- coding:utf-8 -*-

'''
import requests

s = requests.session()
# login_data = {'email':'wenhecpp@126.com','password':'wenhe07052414'}
# p = s.post('http://music.163.com/',login_data)
p = s.post('http://music.163.com/')
print p.text
r = s.get('http://music.163.com/')
data = r.text
print data
'''

import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import xlwt

# initUrl = 'http://www.lagou.com/zhaopin/Python/?labelWords=label'
def Init(skillName):
    totalPage = 30
    initUrl = 'http://www.lagou.com/zhaopin/'
    # skillName = 'Java'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    headers = {'User-Agent':userAgent}

    # create excel sheet
    workBook = xlwt.Workbook(encoding='utf-8')
    sheetName = skillName + ' Sheet'
    bookSheet = workBook.add_sheet(sheetName)
    rowStart = 0
    for page in range(totalPage):
        page += 1
        print '##################################################### Page ',page,'#####################################################'
        currPage = initUrl + skillName + '/' + str(page) + '/?filterOption=3'
        # print currUrl
        try:
            request = urllib2.Request(currPage,headers=headers)
            response = urllib2.urlopen(request)
            jobData = readPage(response)
            # rowLength = len(jobData)
            for i,row in enumerate(jobData):
                for j,col in enumerate(row):
                    bookSheet.write(rowStart + i,j,col)
            rowStart = rowStart + i +1
        except urllib2.URLError,e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
    xlsName = skillName + '.xls'
    workBook.save(xlsName)

def readPage(response):
    btfsp = BeautifulSoup(response.read())
    webLinks = btfsp.body.find_all('div',{'class':'p_top'})
    # webLinks = btfsp.body.find_all('a',{'class':'position_link'})
    # print weblinks.text
    count = 1
    jobData = []
    for link in webLinks:
        print 'No.',count,'==========================================================================================='
        pageUrl = link.a['href']
        jobList = loadPage(pageUrl)
        # print jobList
        jobData.append(jobList)
        count += 1
    return jobData

def loadPage(pageUrl):
    currUrl = 'http:' + pageUrl
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    headers = {'User-Agent':userAgent}
    try:
        request = urllib2.Request(currUrl,headers=headers)
        response = urllib2.urlopen(request)
        content = loadContent(response.read())
        return content
    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason

def loadContent(pageContent):
    # print pageContent
    btfsp = BeautifulSoup(pageContent)
    # job infomation
    job_detail = btfsp.find('dl',{'id':'job_detail'})
    jobInfo = job_detail.h1.text
    tempInfo = re.split(r'(?:\s*)',jobInfo) # re.split is better than the Python's raw split function
    jobTitle = tempInfo[1]
    jobName = tempInfo[2]
    job_request = job_detail.find('dd',{'class':'job_request'})
    reqList = job_request.find_all('p')
    jobAttract = reqList[1].text
    publishTime = reqList[2].text
    itemLists = job_request.find_all('span')
    salary = itemLists[0].text
    workplace = itemLists[1].text
    experience = itemLists[2].text
    education = itemLists[3].text
    worktime = itemLists[4].text

    # company's infomation
    jobCompany = btfsp.find('dl',{'class':'job_company'})
    # companyName = jobCompany.h2
    companyName = re.split(r'(?:\s*)',jobCompany.h2.text)[1]
    companyInfo = jobCompany.find_all('li')
    # workField = companyInfo[0].text.split(' ',1)
    workField = re.split(r'(?:\s*)|(?:\n*)',companyInfo[0].text)[2]
    # companyScale = companyInfo[1].text
    companyScale = re.split(r'(?:\s*)|(?:\n*)',companyInfo[1].text)[2]
    # homePage = companyInfo[2].text
    homePage = re.split(r'(?:\s*)|(?:\n*)',companyInfo[2].text)[2]
    # currStage = companyInfo[3].text
    currStage = re.split(r'(?:\s*)|(?:\n*)',companyInfo[3].text)[1]
    financeAgent = ''
    if len(companyInfo) == 5:
        # financeAgent = companyInfo[4].text
        financeAgent = re.split(r'(?:\s*)|(?:\n*)',companyInfo[4].text)[1]
    workAddress = ''
    if jobCompany.find('div',{'class':'work_addr'}):
        workAddress = jobCompany.find('div',{'class':'work_addr'})
        workAddress = ''.join(workAddress.text.split()) # It's sooooo cool!

    # workAddress = jobCompany.find('div',{'class':'work_addr'})
    # workAddress = ''.join(workAddress.text.split()) # It's sooooo cool!

    infoList = [companyName,jobTitle,jobName,salary,workplace,experience,education,worktime,jobAttract,publishTime,
                workField,companyScale,homePage,workAddress,currStage,financeAgent]

    return infoList

def SaveToExcel(pageContent):
    pass

if __name__ == '__main__':
    # Init(userAgent)
    Init('Python')