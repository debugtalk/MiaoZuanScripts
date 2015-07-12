# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) 2005-2013 UC Mobile Limited. All Rights Reserved
# File          : logger
# 
# Creation      : 2013-8-22
# Author        : huangjj@ucweb.com
# Modified      : 2015-7-10 lilong@ucweb.com
###########################################################################

import sys
import os
project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root_path)

import logging.handlers

from configreader import ConfigReader


class LogFactory(object):
    ''' Helper Class for getting the log object as the config
    '''
    
    def __init__(self, log_config_url="../config/log4py.cfg"):
        ''' Constructor
        Args:
            log_config_url :  the path of the config file
        '''
        self.__level_map = {"NOTSET" : logging.NOTSET,
                "DEBUG" : logging.DEBUG,
                "INFO" : logging.INFO,
                "WARNING" : logging.WARNING,
                "ERROR" : logging.ERROR,
                "CRITICAL" : logging.CRITICAL}
    
        # base config
        self.__format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.__level = "DEBUG"
        self.__url = "/logs/test.log"
        self.__out_place = ["CONSOLE", "FILE"]
        
        # RotatingFileHandler's config
        # the maxBytes value is  1MB
        self.__max_bytes = 1024 * 1024
        # this is the minimum number of logFiles to keep, it is also used by TimedRotatingFileHandler
        self.__backup_count = 10
        
        #TimedRotatingFileHandler's config
        self.__when = 'D'
        self.__interval = 1
        
        self.__log_config_url = log_config_url
        self.__readConfig()
        
    def __readConfig(self):
        ''' Read the base config
        '''
        config_reader = ConfigReader(self.__log_config_url)
        config = config_reader.readConfig()
       
        self.__format = config.get("Output", "format", raw=True)
        self.__level = config.get("Level", "level")
        self.__url = config.get("Url", "log_save_url")

        output_place_string = config.get("Output", "output_place")
        output_place_string.upper()
        self.__out_place = output_place_string.split(",")
        # if output_place=CONSOLE, FILE, ROTATINGFILE
        # then self.__out_place would be ['CONSOLE', ' FILE', ' ROTATINGFILE']
        # in this case, items in self.__out_place should be stripped of blank spaces
        self.__out_place = [output.strip() for output in self.__out_place]
        self.readConfigByFileType(config)
        
    def readConfigByFileType(self, config):
        ''' Read the Config by the file type setting as the config
        Args:
            the object of config
        '''
        if "ROTATINGFILE" in self.__out_place:
            self.__max_bytes = config.get("RotatingFile", "max_bytes")
            self.__backup_count = int(config.get("RotatingFile", "backup_count"))
        elif "TIMEDROTATINGFILE" in self.__out_place:
            self.__when = config.get("TimedRotatingFile", "when")
            self.__interval = long(config.get("TimedRotatingFile", "interval"))
            self.__backup_count = int(config.get("TimedRotatingFile", "backup_count"))

    def getLogger(self, object_name):
        ''' Get the logger object by the object-name
        Args:
            object_name : the object type of the logger
        Returns:
            the object of logger
        '''
        formatter = logging.Formatter(self.__format)
        logger = logging.getLogger(object_name)
        level = self.__level_map.get(self.__level)
        logger.setLevel(level)

        if "CONSOLE" in self.__out_place:
            console_handler = self.__createStreamHandler(formatter)
            logger.addHandler(console_handler)

        if "FILE" in self.__out_place:
            self.__createFile(self.__url)
            file_handler = self.__createFileHandler(formatter)
            logger.addHandler(file_handler)
        elif "ROTATINGFILE" in self.__out_place:
            self.__createFile(self.__url)
            rotating_file_handler = self.__createRotatingFileHandler(formatter)
            logger.addHandler(rotating_file_handler)
        elif "TIMEDROTATINGFILE" in self.__out_place:
            self.__createFile(self.__url)
            timed_rotating_file_handler = self.__createTimedRotatingFileHandler(formatter)
            logger.addHandler(timed_rotating_file_handler)

        return logger

    def __createStreamHandler(self, formatter):
        ''' create a handler to output the information to the console
        Args:
            formatter : the formatter of the output info
        Returns:
            the object of Stream Handler
        '''
        console_handler = logging.StreamHandler()  
        console_handler.setFormatter(formatter)
        return console_handler


    def __createFileHandler(self, formatter):
        ''' Create a handler to write the information to the file
         Args:
            formatter : the formatter of the output info
        Returns:
            the object of File Handler
        '''
        file_handler = logging.FileHandler(self.__url)
        file_handler.setFormatter(formatter)
        return file_handler


    def __createRotatingFileHandler(self, formatter):
        ''' Create a handler to write the information to the files which is limited the maxBytes,
        if the file larger than the maxBytes and the number of log files isn't more than backupCount,
        it will create an new file and continue 

        Args:
            formatter : the formatter of the output-info
        '''
        rotating_file_handler = logging.handlers.RotatingFileHandler(self.__url, maxBytes=self.__max_bytes, backupCount=self.__backup_count)
        rotating_file_handler.setFormatter(formatter)
        return rotating_file_handler
    
    def __createTimedRotatingFileHandler(self, formatter):
        ''' create a handler which can create a file and write information to it according to the time period
        Args:
            formatter : the formatter of the output-info
        Returns:
            the object of TimedRotatingFileHandler
        '''
        timed_rotating_file_handler = logging.handlers.TimedRotatingFileHandler(self.__url, when=self.__when, interval=self.__interval, backupCount=self.__backup_count)
        timed_rotating_file_handler.setFormatter(formatter)
        return timed_rotating_file_handler

    def __createFile(self, path):
        ''' Create File for log
        Args:
            path : location of the file you want to create
        '''
        (folder_url, file_name) = os.path.split(path)
        if not os.path.exists(path):
            if not os.path.exists(folder_url):
                os.makedirs(folder_url)
            fp = open(path, "w")
            fp.close()

log4py_config_file = os.path.join(project_root_path, 'logger', 'log4py.cfg')
logFactory = LogFactory(log4py_config_file)

if __name__ == '__main__':
    logger = logFactory.getLogger(__name__)
    logger.debug("123")
