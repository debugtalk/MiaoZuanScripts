#!/usr/bin/python
#encoding=utf-8

import urllib, urllib2
import cookielib
import re
import time
from random import random
from json import dumps as json_dumps, loads as json_loads

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(project_root_path)

from logger.logger import logFactory
logger = logFactory.getLogger(__name__)

class MiaoZuan(object):
    """docstring for MiaoZuan"""
    def __init__(self, account_file):
        super(MiaoZuan, self).__init__()
        self.headers = headers = {
            'User-Agent':'IOS_8.1_IPHONE5C',
            'm-lng':'113.331639',
            'm-ct':'2',
            'm-lat':'23.158624',
            'm-cw':'320',
            'm-iv':'3.0.1',
            'm-ch':'568',
            'm-cv':'6.5.2',
            'm-lt':'1',
            'm-nw':'WIFI',
            #'Content-Type':'application/json;charset=utf-8'
        }
        self.accountList = self.get_account_List(account_file)

    def get_account_List(self, account_file):
        accountList = []
        try:
            with open(account_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    user, userName, passWord, imei = line.strip('\n').split(',')
                    accountList.append([user, userName, passWord, imei])
        except Exception as e:
            logger.exception(e)
        finally:
            return accountList

    def login(self, userName, passWord, imei):

        postdata = urllib.urlencode({
            'UserName':userName,
            'Password':passWord,
            'Imei':imei
        })

        req = urllib2.Request(
            url='http://service.inkey.com/api/Auth/Login',
            data=postdata,
            headers=self.headers
        )
        
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        try:
            content = urllib2.urlopen(req).read()
            resp_dict = json_loads(content)
            return resp_dict
        except Exception as e:
            logger.exception(e)
            return {"IsSuccess": False, "Desc": ""}

    def pull_SilverAdvert_List(self, categoryId):
        postdata = urllib.urlencode({
            'CategoryIds':categoryId
        })
        req = urllib2.Request(
            url='http://service.inkey.com/api/SilverAdvert/Pull',
            data = postdata,
            headers = self.headers
        )

        try:
            content = urllib2.urlopen(req).read()
            silverAdvert_pat = re.compile(r'"Id":(.*?),')
            silverAdvert_list = re.findall(silverAdvert_pat, content)
            logger.debug("categoryId = %s, pull_SilverAdvert_List = %s", categoryId, silverAdvert_list)
        except Exception as e:
            logger.exception(e)
            silverAdvert_list = []

        return silverAdvert_list

    def viewOne_SilverAdvert_by_advertsID(self, advertsID):
        postdata = urllib.urlencode({
            'IsGame':"false",
            "Id":advertsID
        })
        req = urllib2.Request(
            url='http://service.inkey.com/api/SilverAdvert/GeneratedIntegral',
            data = postdata,
            headers = self.headers
        )
        try:
            content = urllib2.urlopen(req).read()
            logger.debug("view advert id = %s, Response from the server: %s", advertsID, content)
            resp_dict = json_loads(content)
            return resp_dict
        except Exception as e:
            logger.exception(e)
            return {"IsSuccess": False}

    def viewAll_SilverAdverts_by_categoryId(self, categoryId):
        silverAdsList = self.pull_SilverAdvert_List(categoryId)
        silverAdsList_Count = len(silverAdsList)

        total_data_by_categoryId = 0
        result_Code = 0
        result_Code_31303_count = 0
        selectNum = 0

        if silverAdsList_Count > 0:
            while True:
                advertsID = silverAdsList[selectNum]
                resp_dict = self.viewOne_SilverAdvert_by_advertsID(advertsID)
                selectNum += 1

                if selectNum >= silverAdsList_Count:
                    selectNum -= silverAdsList_Count

                if resp_dict["IsSuccess"]:
                    total_data_by_categoryId += resp_dict["Data"]
                    logger.debug("get %s more points", resp_dict["Data"])
                elif resp_dict["Code"] == 31303:
                    logger.debug("view advert id = %s, Response from the server: %s", advertsID, resp_dict["Desc"])
                    result_Code_31303_count += 1
                    continue
                elif resp_dict["Code"] == 31307 or result_Code_31303_count > silverAdsList_Count:
                    logger.debug("Response from the server: %s", resp_dict["Desc"])
                    break

                time.sleep(12+3*random())

        logger.info("categoryId = %s, total_data_by_categoryId = %s" % (categoryId, total_data_by_categoryId))

        return [result_Code, total_data_by_categoryId]

    def get_all_silvers(self):
        total_data = 0
        result_Code = 0
        categoryIds = [-1, 1, -2, 2, -3, 3, -4, 4, 5, 6, 10]
        categoryIds_Count = len(categoryIds)
        i = 0
        List_Count_equals_0 = 0 #如果获取12次广告，广告数都为零，则切换至下一个帐号

        while result_Code != '31307' and List_Count_equals_0 < 12:
            categoryId = categoryIds[i]
            [result_Code, data_by_categoryId] = self.viewAll_SilverAdverts_by_categoryId(categoryId)
            total_data += data_by_categoryId
            if result_Code == 0:
                List_Count_equals_0 += 1
            i += 1
            if i >= categoryIds_Count:
                i -= categoryIds_Count

        return total_data

    def start(self):
        for account in self.accountList:
            user, userName, passWord, imei = account
            logger.info("User Iteration Started: %s", user)
            login_result_dict = self.login(userName, passWord, imei)
            if login_result_dict["IsSuccess"]:
                try:
                    total_data_by_all_categoryIds = self.get_all_silvers()
                    logger.debug("total_data_by_all_categoryIds: %s" % total_data_by_all_categoryIds)
                except Exception as e:
                    logger.exception(e)
                finally:
                    logger.info("User Iteration Ended: %s", user)
            else:
                logger.warning("Login failed, login user: %s, error description: %s", user, login_result_dict["Desc"])
            logger.info("---------------------------------------------------\n")

    def run_forever(self):
        while True:
            self.start()
            time.sleep(4*3600)

if __name__ == '__main__':
    account_file = os.path.join(project_root_path, 'Config', 'Accounts.dat')
    mz = MiaoZuan(account_file)
    mz.run_forever()
