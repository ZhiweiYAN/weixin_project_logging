#!/usr/bin/env python
#-*- coding:utf-8 -*

"""Provide the constants and configuration for the 
Workflow&Weixin development.

Here we load the configuration from the config file.
It includes the constants, error strings and so son.
"""

__author__ = "Zhe Yan, Zhiwei Yan"
__copyright__ = "Copyright 2015, The Workflow&Weixin Project"
__credits__ = ["Weiming Guo"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Zhiwei YAN"
__email__ = "jerod.yan@gmail.com"
__status__ = "Production"

import urllib2, urllib
import time, datetime
import thread
import logging, logmsg
import json
import xml.etree.ElementTree as ET

#the error strings or constants for the project
err_code = {\
    'ERR001': 'N/A', \
    'ERR002': 'N/A', \
    'ERR003': 'N/A', \
    'ERR004': 'N/A'
}    

#WeiXin Auth-codes
weixin_auth_info = { \
    'Token': 'N/A',\
    'EncodingAESKey': 'N/A',\
    'CoprID': 'N/A',\
    'CorpSecret':'N/A',\
    'AccessTokenExpireDuration': 'N/A',\
    'AccessToken':'N/A'
}

#WeiXin Url
weixin_urls = { \
    'FetchTokenUrl':'N/A'
}

#DB Info
db_info = { \
    'DBIP': 'N/A', \
    'DBPort': 'N/A', \
    'DBUser': 'N/A', \
    'DBPassword': 'N/A', \
    'DBName': 'N/A'
}

#load the parameters from the config file
def ReadConfigParameters(cfg_file):
    global err_code
    global weixin_auth_info
    global weixin_urls

    # using the etree to parse the xml file
    tree = ET.ElementTree(file=cfg_file)
    root = tree.getroot() 
    for child_of_root in root:
        #print child_of_root.tag, child_of_root.text
        
        #Auth Info
        if 'Token' == child_of_root.tag:
            weixin_auth_info['Token'] = child_of_root.text
            print 'Token: ', weixin_auth_info['Token'] 
        if 'EncodingAESKey' == child_of_root.tag:
            weixin_auth_info['EncodingAESKey'] = child_of_root.text
            print 'EncodingAESKey: ', weixin_auth_info['EncodingAESKey'] 
        if 'CorpID' == child_of_root.tag:
            weixin_auth_info['CorpID'] = child_of_root.text
            print 'CorpID: ', weixin_auth_info['CorpID'] 
        if 'CorpSecret' == child_of_root.tag:
            weixin_auth_info['CorpSecret'] = child_of_root.text
            print 'CorpSecret: ', weixin_auth_info['CorpSecret'] 
        if 'AccessTokenExpireDuration' == child_of_root.tag:
            weixin_auth_info['AccessTokenExpireDuration'] = child_of_root.text
            print 'AccessTokenExpireDuration: ', weixin_auth_info['AccessTokenExpireDuration'] 
        
        # URLS
        if 'FetchTokenUrl' == child_of_root.tag:
            weixin_urls['FetchTokenUrl'] = child_of_root.text
            print 'FetchTokenUrl: ', weixin_urls['FetchTokenUrl'] 

        # ERROR CODES
        if 'ERR004' == child_of_root.tag:
            err_code['ERR004'] = child_of_root.text
            print 'ERR004: ', err_code['ERR004'] 
        if 'ERR003' == child_of_root.tag:
            err_code['ERR003'] = child_of_root.text
            print 'ERR003: ', err_code['ERR003'] 
        if 'ERR002' == child_of_root.tag:
            err_code['ERR002'] = child_of_root.text
            print 'ERR002: ', err_code['ERR002'] 
        if 'ERR001' == child_of_root.tag:
            err_code['ERR001'] = child_of_root.text
            print 'ERR001: ', err_code['ERR001'] 
       
        #DB configuration info
        if 'DBName' == child_of_root.tag:
            db_info['DBName'] = child_of_root.text
            print 'DBName: ', db_info['DBName'] 
        if 'DBPassword' == child_of_root.tag:
            db_info['DBPassword'] = child_of_root.text
            print 'DBPassword: ', db_info['DBPassword'] 
        if 'DBUser' == child_of_root.tag:
            db_info['DBUser'] = child_of_root.text
            print 'DBUser: ', db_info['DBUser'] 
        if 'DBPort' == child_of_root.tag:
            db_info['DBPort'] = child_of_root.text
            print 'DBPort: ', db_info['DBPort'] 
        if 'DBIP' == child_of_root.tag:
            db_info['DBIP'] = child_of_root.text
            print 'DBIP: ', db_info['DBIP'] 
        

#Fetch the access token periodicaly.
def RefreshAccessToken(threadName, delay):
    global weixin_auth_info
    AccessTokenExpireDuration = weixin_auth_info['AccessTokenExpireDuration']
    sCorpID = weixin_auth_info['CorpID']
    sCorpSecret = weixin_auth_info['CorpSecret']
    sWeixinTokenUrl = weixin_urls['FetchTokenUrl']
    url = sWeixinTokenUrl % (sCorpID, sCorpSecret)
    while True:
        result = Get(url)
        logging.info("Access token packet:|%r|. " %result)
        if ('access_token' in result.keys()):
            weixin_auth_info['Access_token'] = result['access_token']

            Access_token = result['access_token']
            delay = result['expires_in']

            logging.info("Refresh Access Token = |%r|, Expires_in = |%r|." %(Access_token, delay))
            time.sleep(delay - 1)
        else:
            time.sleep(AccessTokenExpireDuration)

# Create one thread to refresh access token as follows
def StartRefreshThread():
    global weixin_auth_info
    try:
        thread.start_new_thread( RefreshAccessToken, \
              ("Refresh-Access-Token-Thread", \
               weixin_auth_info['AccessTokenExpireDuration']) )
    except:
        logging.info( "Error: unable to start Refresh access token thread")


def Post(url, data):
    try:
        req = urllib2.Request(url, data);
        response = urllib2.urlopen(req);
        result = json.loads(response.read())
        logging.info("POST:URL = |%s|" % url)
        logging.info("POST:Response = |%s|" % result)
        if (not result.has_key('errcode')):
            logging.info("There are not errocode in the response.")
        else:
            logging.info("There are errocode: %s." %(result['errocode']))
    except: 
        logging.info("HTTP Post method: Failed.") 

    return result


def Get(url):
    try:
        response = urllib2.urlopen(url)
        result = json.loads(response.read())
        logging.info("GET:URL = |%s|" % url)
        logging.info("GET:Response = |%s|" % result)
        if (not result.has_key('errcode')):
            logging.info("There are not errocode in the response.")
        else:
            logging.info("There are errocode: %s." %(result['errocode']))
    except: 
        logging.info("HTTP GET  method: Failed.") 
    return result

