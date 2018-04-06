#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import string
import sys
import os
import urllib
#import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import traceback
import datetime
import time
import xlrd
import decimal
import numbers
import csv

#Posts Class
class posts:
    def __init__(self):
        self.date_post = "" 
        self.content = "" 
        self.num_zan = 0
        self.num_forward = 0
        self.num_comment = 0
        self.list_zan = []
        self.list_comment = []
        self.list_comment_id = []
        self.list_forward_id = []
        self.list_forward = []
        
#Weibo Class
class weibo:
    cookie = {"Cookie": "_T_WM=2ee5b6633176df213607b53fd8a890c8; ALF=1523930834; SCF=AkbCxPsM1cGWll_GhiJb2j768WoA4glTwR6oHhfajA5O88d2OtlYfPN6GvfHVNkAN6U31b9rMW1TtPY9rbH_Pmg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5C797qKi6D_ENRzmvp3deo5JpX5K-hUgL.FoqXeo-0eKzNSo-2dJLoI7fe9gyD9cyKUGH.9g4X; SUB=_2A253qhTsDeRhGeBK6VcS8SzLzTmIHXVVVLykrDV6PUJbkdBeLVjskW1NR87d61DB4yy-cRaCVoWZSApDa1oiWh_L; SUHB=0xnSdRi0VqaBGo; SSOLoginState=1521378492"} #将your cookie替换成自己的cookie
	
    #weibo init
    def __init__(self,user_id,filter = 0):
        self.user_id = user_id # UserID 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter #0 for all 1 for original取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.userName = '' # user nam e用户名，如“Dear-迪丽热巴”
        self.weiboNum = 0 # total number of weibo post 用户全部微博数
        self.weiboNum2 = 0 # total number of web-scraped post 爬取到的微博数
        self.following = 0 # total number of following by this account 用户关注数
        self.followers = 0 # total number of fans 用户粉丝数
        self.weibos = [] # weibo post 微博内容
        self.list_following = []
        self.list_follower = []
        self.currentPage = 1
            
    def getUserFollowing(self):
        try:
            url = 'http://weibo.cn/%s/follow?page=1'%(self.user_id)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]')==[]:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

            for page in range(1,pageNum+1):
                time.sleep(1)
                url2 = 'http://weibo.cn/%s/follow?page=%d'%(self.user_id,page)
                html2 = requests.get(url2, cookies = weibo.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//tr/td[@valign ='top']/a/@href")
                
                for num in range(0,len(info)):
                    tmp = info[num].split("/")
                    if tmp[len(tmp) - 1].isdigit():
                        if tmp[len(tmp) - 1] not in self.list_following:
                            self.list_following.append(tmp[len(tmp) - 1])
        except Exception as e:		 
            content = "Error from getUserFollowing."
            print(content)	
            self.writeLogFile(content)
        
    def getUserFollower(self):
        try:
            url = 'http://weibo.cn/%s/fans?page=1'%(self.user_id)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]')==[]:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

            for page in range(1,pageNum+1):
                time.sleep(1)
                url2 = 'http://weibo.cn/%s/fans?page=%d'%(self.user_id,page)
                html2 = requests.get(url2, cookies = weibo.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//tr/td[@valign ='top']/a/@href")
                
                for num in range(0,len(info)):
                    tmp = info[num].split("/")
                    if tmp[len(tmp) - 1].isdigit():
                        if tmp[len(tmp) - 1] not in self.list_follower:
                            self.list_follower.append(tmp[len(tmp) - 1])
        except Exception as e:		 
            content = "Error from getUserFollower."
            print(content)	
            self.writeLogFile(content)
    
    # Get user name 获取用户昵称 
    def getUserName(self):
        try:
            url = 'http://weibo.cn/%s/info'%(self.user_id)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)
            userName = selector.xpath("//title/text()")[0]
            self.userName = userName[:-3]
            #print '用户昵称：' + self.userName
        except Exception as e:		 
            content = "Error from getUserName."
            print(content)	
            self.writeLogFile(content)
		
	# Get number of post, following and followers 获取用户微博数、关注数、粉丝数
    def getUserInfo(self):
        try:
            url = 'http://weibo.cn/u/%s?filter=%d&page=1'%(self.user_id,self.filter)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)	
            pattern = r"\d+\.?\d*"

            # number of post 微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S|re.M)	
            for value in guid:	 
                num_wb = int(value)	 
                break
            self.weiboNum = num_wb	
            #print '微博数: ' + str(self.weiboNum)	

            # number of following 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)  
            str_gz = selector.xpath("//div[@class='tip2']/a/@href")
            for num in range(0, len(str_gz)):
                tmp = str_gz[num].split("/")
                if tmp[len(tmp) - 1] == "follow":
                    print("     Getting data for all following account...")
                    #weibo.getUserFollowing(self)
                if tmp[len(tmp) - 1] == "fans":
                    print("     Getting data for all follower account...")
                    #weibo.getUserFollower(self)
            self.following = int(guid[0])  
            #print '关注数: ' + str(self.following)
            
            time.sleep(1)
            url = 'http://weibo.cn/u/%s?filter=%d&page=1'%(self.user_id,self.filter)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)	

            # number of followers 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)  
            self.followers = int(guid[0]) 
            #print '粉丝数: ' + str(self.followers)
        except Exception as e:		 
            content = "Error from getUserInfo."
            print(content)	
            self.writeLogFile(content)
            raise
        
	#获取用户微博内容及对应的点赞数、转发数、评论数	
    def getWeiboInfo(self):
        try:
            url = 'http://weibo.cn/u/%s?filter=%d&page=1'%(self.user_id,self.filter)
            html = requests.get(url, cookies = weibo.cookie).content
            selector = etree.HTML(html)
            
            if selector.xpath('//input[@name="mp"]')==[]:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            
            self.getPosts(self.currentPage, pageNum)
            
        except Exception as e:		 
            content = "Error from getWeiboInfo."
            print(content)	
            self.writeLogFile(content)
            
        
    def getPosts(self, currentPage, pageNum):
        try:
            pageBegin = self.currentPage
            for page in range(pageBegin,pageNum+1):
                self.currentPage = page
                pattern = r"\d+\.?\d*"
                print("page: ",page)
                self.writeLogFile("Getting Page " + str(page))
                time.sleep(1)
                url2 = 'http://weibo.cn/u/%s?filter=%d&page=%d'%(self.user_id,self.filter,page)
                html2 = requests.get(url2, cookies = weibo.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                #print len(info)
                
                for i in range(0,max(len(info)-2,0)):
                    pt = posts();
                    self.weiboNum2 = self.weiboNum2 + 1
                    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"     " + str(self.weiboNum2))
                    self.writeLogFile("Getting Post " + str(self.weiboNum2))
                    
                    flag = 0;
                    #微博内容
                    str_t = info[i].xpath("div/span[@class='ctt']")
                    str_full = info[i].xpath("div/span[@class='ctt']/a/@href")
                    test = info[i].xpath("div/span[@class='ctt']/a")
                    if str_full:
                        for j in range (0, len(test)):
                            if test[j].text.encode('utf-8','ignore') == "全文":
                                flag = 1;
                                tmp = "http://weibo.cn"
                                #print str_full[0]
                                tmp += str_full[j]
                                str_full[0] = tmp
                                url3 = str_full[0]
                                #print url3
                                time.sleep(1)
                                html3 = requests.get(url3, cookies = weibo.cookie).content
                                selector3 = etree.HTML(html3)
                                str_full_content = selector3.xpath("//div[@class='c']/div/span[@class='ctt']")
                                if str_full_content:
                                    weibos = str_full_content[0].xpath('string(.)').encode('utf-8','ignore')
                                    pt.content = weibos
                                    #print '微博内容：'+ weibos

                                    time.sleep(1)
                                    url2 = 'http://weibo.cn/u/%s?filter=%d&page=%d'%(self.user_id,self.filter,page)
                                    html2 = requests.get(url2, cookies = weibo.cookie).content
                                    selector2 = etree.HTML(html2)
                                    info = selector2.xpath("//div[@class='c']")
                                    break
                        if flag == 0:
                            if str_t:
                                #print test[0].text
                                weibos = str_t[0].xpath('string(.)').encode('utf-8','ignore')
                                pt.content = weibos
                    else:
                        if str_t:
                            weibos = str_t[0].xpath('string(.)').encode('utf-8','ignore')
                            pt.content = weibos
                            #print '微博内容：'+ weibos
                    
                    #点赞数
                    tem = info[i].xpath("div/a/text()")
                    str_zan = "赞[0]"
                    if len(tem) > 4:
                        str_zan = tem[-4]
                    
                    guid = re.findall(pattern, str_zan, re.M)
                    if guid:
                        num_zan = int(guid[0])
                    else:
                        num_zan = 0
                    pt.num_zan = num_zan
                    #print '点赞数: ' + str(num_zan)
                    
                    #转发数
                    tem = info[i].xpath("div/a/text()")
                    forwarding = "转发[0]"
                    if len(tem) > 4:
                        forwarding = tem[-3]
                        
                    guid = re.findall(pattern, forwarding, re.M)	
                    num_forwarding = int(guid[0])
                    pt.num_forward = num_forwarding		  
                    #print '转发数: ' + str(num_forwarding)
                    
                    #评论数
                    tem = info[i].xpath("div/a/text()")
                    comment = "评论[0]"
                    if len(tem) > 4:
                        comment = tem[-2]
                        
                    guid = re.findall(pattern, comment, re.M)	 
                    num_comment = int(guid[0]) 
                    pt.num_comment = num_comment
                    #print '评论数: ' + str(num_comment)
                    
                    #日期
                    dates = info[i].xpath("div/span[@class='ct']/text()")
                    if len(dates) > 0:
                        dates = re.findall(r'\d+', dates[0])
                        year = 0;
                        month = 0;
                        day = 0;
                        if int(dates[0]) < 13:
                            now = datetime.datetime.now()
                            year = now.year
                            month = int(dates[0])
                            day = int(dates[1])
                        else:
                            year = int(dates[0])
                            month = int(dates[1])
                            day = int(dates[2])
                        pt.date_post = str(year) + "-" + str(month) + "-" + str(day)
                    
                    #点赞者
                    if pt.num_zan > 0:
                        url4 = info[i].xpath("div/a[@class='cc']/@href")
                        tmp = url4[0].split("?")
                        tmp = tmp[0].split("/")
                        tmp = tmp[len(tmp) - 1]
                        url5 = "https://weibo.cn/attitude/" + tmp + "?#attitude"
                        time.sleep(1)
                        html5 = requests.get(url5, cookies = weibo.cookie).content
                        selector5 = etree.HTML(html5)
                        page_zan = selector5.xpath("//div[@class='c']")
                        for j in range(3, len(page_zan)-1):
                            zan_name = page_zan[j].xpath("a/@href") 
                            if zan_name:
                                zan_name = zan_name[0].split("/")
                                zan_name = zan_name[len(zan_name) - 1]
                                if zan_name.isdigit():
                                    pt.list_zan.append(str(zan_name))

                    #转发者
                    if pt.num_forward > 0:
                        url4 = info[i].xpath("div/a[@class='cc']/@href")
                        tmp = url4[0].split("?")
                        tmp = tmp[0].split("/")
                        tmp = tmp[len(tmp) - 1]
                        url5 = "https://weibo.cn/repost/" + tmp + "?uid=" + str(self.user_id) + "&#rt"
                        time.sleep(1)
                        html5 = requests.get(url5, cookies = weibo.cookie).content
                        selector5 = etree.HTML(html5)
                        page_share = selector5.xpath("//div[@class='c']")
                        for j in range(3, len(page_share)-1):
                            share_name = page_share[j].xpath("a/@href")
                            if share_name:
                                share_name = share_name[0].split("/")
                                share_name = share_name[len(share_name) - 1]
                                if share_name.isdigit():
                                    pt.list_forward_id.append(str(share_name))

                                    comment_content = page_share[j].xpath("a/following-sibling::text()")
                                    #print(comment_content[len(comment_content) - 1].encode('utf-8','ignore'))
                                    if comment_content:
                                        pt.list_forward.append(comment_content[len(comment_content) - 1].encode('utf-8','ignore'))
                                
                    #评论者
                    if pt.num_comment > 0:
                        url4 = info[i].xpath("div/a[@class='cc']/@href")
                        tmp = url4[0].split("?")
                        tmp = tmp[0].split("/")
                        tmp = tmp[len(tmp) - 1]
                        url5 = "https://weibo.cn/comment/" + tmp + "?#rt"
                        time.sleep(1)
                        html5 = requests.get(url5, cookies = weibo.cookie).content
                        selector5 = etree.HTML(html5)
                        page_comment = selector5.xpath("//div[@class='c']")
                        for j in range(3, len(page_comment)-1):
                            comment_name = page_comment[j].xpath("a/@href")
                            if comment_name:
                                comment_name = comment_name[0].split("/")
                                comment_name = comment_name[len(comment_name) - 1]
                                if comment_name.isdigit():
                                    pt.list_comment_id.append(str(comment_name))
                                    comment_content = page_comment[j].xpath("span[@class='ctt']/text()")
                                    if comment_content:
                                        pt.list_comment.append(comment_content[len(comment_content) - 1].encode('utf-8','ignore'))
                    
                    time.sleep(1)                    
                    self.weibos.append(pt)
                    self.writeCsvPost(pt,len(self.weibos))
                        
            if self.filter == 0:
                print ('Total: '+str(self.weiboNum2)+' Weibos.')
            else:
                print ('Total: '+str(self.weiboNum)+' Weibos, '+str(self.weiboNum2)+' are Original Posts.')
        except Exception as e:		 
            traceback.print_exc()
            content = "Error from getPosts."
            print(content)	
            self.writeLogFile(content)
            time.sleep(30)
            self.getPosts(self.currentPage,pageNum)
    
    def writeCsvPost(self,pt,num):
        try:
             with open("weibo/%s.csv"%self.user_id, "a",encoding = 'utf-8') as csvfile:
                fieldnames = ['Num', 'Post', 'Date', 'Like', 'Like_ID', 'Share', 'Share_ID', 'Share_Content', 'Comment', 'Comment_ID', 'Comment_Content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                pt.list_comment = [x.decode('utf-8') for x in pt.list_comment]              
                comment = "$".join(pt.list_comment)
                pt.list_forward = [x.decode('utf-8') for x in pt.list_forward]
                share = "$".join(pt.list_forward)
                #print({'Num': num, 'Post': pt.content.decode('utf-8'), 'Date': str(pt.date_post) ,'Like': str(pt.num_zan), 'Like_ID': pt.list_zan ,'Share': str(pt.num_forward), 'Share_ID': str(pt.list_forward_id), 'Share_Content': share, 'Comment': str(pt.num_comment), 'Comment_ID': str(pt.list_comment_id), 'Comment_Content': comment})
                #writer.writerow({'Num': num, 'Post': pt.content, 'Date': str(pt.date_post) ,'Like': str(pt.num_zan), 'Like_ID': pt.list_zan ,'Share': str(pt.num_forward), 'Share_ID': str(pt.list_forward_id), 'Share_Content': share, 'Comment': str(pt.num_comment), 'Comment_ID': str(pt.list_comment_id), 'Comment_Content': comment})                    
                writer.writerow({'Num': num, 'Post': pt.content.decode('utf-8'), 'Date': str(pt.date_post) ,'Like': str(pt.num_zan), 'Like_ID': pt.list_zan ,'Share': str(pt.num_forward), 'Share_ID': str(pt.list_forward_id), 'Share_Content': share, 'Comment': str(pt.num_comment), 'Comment_ID': str(pt.list_comment_id), 'Comment_Content': comment})                    
        except Exception as e:
            content = "Error from writeCsvPost."
            print(content)	
            self.writeLogFile(content)
    
    #将爬取的信息写入文件	
    def writeCsvGeneral(self):
        try:
            with open("weibo/User_info.csv", "a") as csvfile:
                fieldnames = ['Username', 'Account ID', 'Num of Post', 'Num of followers', 'Num of fans', 'Followers ID', 'Fans ID']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Username': self.userName, 'Account ID': str(self.user_id), 'Num of Post': str(self.weiboNum),'Num of followers': str(self.following),'Num of fans': str(self.followers),'Followers ID': self.list_following,'Fans ID': self.list_follower})
            
        except Exception as e:		 
            content = "Error from writeCsvGeneral."
            print(content)	
            self.writeLogFile(content)

    def writeLogFile(self, content):
        with open("weibo/Log.txt","a") as file:
            file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+ "\t---\t" + content + "\n")
                
#Main Program	
text_file = open("input.txt","r")
colValues = text_file.readlines()
text_file.close()

colValues = [x.replace('\n','') for x in colValues]

if not os.path.exists("weibo"):
    os.makedirs("weibo")

if not os.path.isfile("weibo/User_info.csv"):
    with open("weibo/User_info.csv", "w") as csvfile:
        fieldnames = ['Username', 'Account ID', 'Num of Post', 'Num of followers', 'Num of fans', 'Followers ID', 'Fans ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
if not os.path.isfile("weibo/Log.txt"):
    with open("weibo/Log.txt","w") as file:
        file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+ "\t---\t" + "Log file created." + "\n")

for i in range(0,len(colValues)):
    tmp = colValues[i]    
    print ("\nCurrent: " + str(i) + ", User ID: " + str(tmp))
    user_id = str(tmp) #可以改成任意合法的用户id（爬虫的微博id除外）
    
    if not os.path.isfile("weibo/"+user_id+".csv"):
        with open("weibo/"+user_id+".csv", "w") as csvfile:
            fieldnames = ['Num', 'Post', 'Date', 'Like', 'Like_ID', 'Share', 'Share_ID', 'Share_Content', 'Comment', 'Comment_ID', 'Comment_Content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    filter = 0 #值为0表示爬取全部的微博信息（原创微博+转发微博），值为1表示只爬取原创微博
    wb = weibo(user_id,filter) #调用weibo类，创建微博实例wb
    wb.writeLogFile("Getting Information from current user: "+ str(tmp))

    wb.getUserInfo()
    wb.getUserFollowing()
    wb.getUserFollower()
    wb.getUserName()
    wb.writeCsvGeneral()
    wb.getWeiboInfo()
    
    print ('Data Collection Process Finished.')
    print ('===========================================================================')
    
    content = "Data Collection Process Finished."
    wb.writeLogFile(content)




