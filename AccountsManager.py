#!/usr/bin/python
#encoding=utf-8

import urllib, urllib2
import cookielib
import re
import time
from random import random


class AccountsManager(object):
    """docstring for AccountsManager"""
    def __init__(self):
        super(AccountsManager, self).__init__()
        self.headers = headers = {
            'User-Agent':'IOS_8.2_IPHONE5C',
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


    def customerRegister(self, userName, passWord, imei):
        postdata = urllib.urlencode({
            'UserName':userName,
            'Password':passWord,
            'Imei':imei
        })

        req = urllib2.Request(
            url ='http://service.inkey.com/api/Auth/CustomerRegister',
            data = postdata,
            headers = self.headers
        )

        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        content = urllib2.urlopen(req).read()
        resRegisterCode_pat = re.compile(r'Code":(.*?),')
        result_RegisterCode = re.findall(resRegisterCode_pat, content)
        return content # result_RegisterCode[0]


    def fillBasicInfo(self, gender, trueName, annualIncome=None, birthday=None):
        postdata = urllib.urlencode({
            'Gender':gender,
            'TrueName':trueName,
            'AnnualIncome':annualIncome,
            'Birthday':birthday
        })

        req = urllib2.Request(
            url ='http://service.inkey.com/api/Customer/FillBasicInfo',
            data = postdata,
            headers = self.headers
        )

        content = urllib2.urlopen(req).read()
        resRegisterCode_pat = re.compile(r'Code":(.*?),')
        result_RegisterCode = re.findall(resRegisterCode_pat, content)
        return content # result_RegisterCode[0]


    def register(self):
        self.customerRegister('18665088862', '123456', 'D4720360-1339-47A4-BC96-2BC5B0218331')
        #self.fillBasicInfo('1', '李隆')


    def login(self, userName, passWord, imei):

        postdata = urllib.urlencode({
            'UserName':userName,
            'Password':passWord,
            'Imei':imei
        })

        req = urllib2.Request(
            url ='http://service.inkey.com/api/Auth/Login',
            data = postdata,
            headers = self.headers
        )
        
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        content = urllib2.urlopen(req).read()
        resLoginCode_pat = re.compile(r'Code":(.*?),')
        result_LoginCode = re.findall(resLoginCode_pat, content)
        return result_LoginCode[0]


    '''
    saveMemberCampaign('18613143458', '862966026016476', '0B3F9C35C6216A1BDF09A0AB9A19B4A0D7AA2406', '2')
    saveMemberCampaign('18665088869', '623CA7E5-52AA-4BDE-84DF-AE0B4E5BFC32', 'e6150a2c19026dab18a56a71fcb3c4ebb9b19abd', '2')
    ToDo: sign的生成机制未知
    {"Code":32059,"Desc":"感恩失败，请下载最新版本"}
    '''
    def saveMemberCampaign(self, presenterPhone, currentImei, sign, campaignType='2'):
        postdata = urllib.urlencode({
            'CampaignType':campaignType,
            'CurrentImei':currentImei,
            'PresenterPhone':presenterPhone,
            'Sign':sign
        })

        req = urllib2.Request(
            url ='http://service.inkey.com/api/MemberCampaign/Save',
            data = postdata,
            headers = self.headers
        )

        content = urllib2.urlopen(req).read()
        resCode_pat = re.compile(r'Code":(.*?),')
        result_Code = re.findall(resCode_pat, content)
        return content # result_Code[0]



if __name__ == '__main__':
    #account_file = 'Accounts.dat'
    am = AccountsManager()
    #res = am.register()
    #am.customerRegister('18665088862', '123456', 'D4720360-1339-47A4-BC96-2BC5B0218331')
    print am.login('18665088862', '123456', '862966026016476')
    print am.saveMemberCampaign('18613143458', '862966026016476', '0B3F9C35C6216A1BDF09A0AB9A19B4A0D7AA2406', '2')
    #am.fillBasicInfo('1', '李隆')
    #print res
