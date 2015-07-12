# -*- coding: utf-8 -*-

##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : configreader
# 
# Creation      : 2013-8-22
# Author        : huangjj@ucweb.com
###########################################################################
import ConfigParser

class ConfigReader(object):
    ''' Helper class for read the config file both the format "*.ini" and "*.cfg"
        something usage example of Config Parser : http://my.oschina.net/mutour/blog/32530
    '''
   
    def __init__(self, url="../logger/log4py.cfg"):
        ''' Constructor of this class
        Args:
            url: the path of config file
        '''
        self.__log_file_url = url
    
    def readConfig(self):
        '''read the config file
        Return:
            the config object
        '''
        config = ConfigParser.ConfigParser()
        cfgfile = open(self.__log_file_url, "r")
        config.readfp(cfgfile)
        return config
    
    def getSections(self):
        '''get the sections of the config file
        Return:
            a list of the sections available
        '''
        config = self.readConfig()
        sections = config.sections()
        return sections
    
    def getItems(self, section_name):
        '''get a list of (name, value) pairs for each option in the given section.
        Args:
            section_name: the name of the section which want to get the options in it
        Return:
            a list of (name, value) pairs for each option in the given section.
        '''
        config = self.readConfig()
        items = config.items(section_name)
        return items

if __name__ == '__main__':
    confReader = ConfigReader()
    conf = confReader.readConfig()
    sessions = confReader.getSections()
    print sessions
    for session in sessions:
        print session
        print confReader.getItems(session)
