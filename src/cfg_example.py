#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : cfg.py
#   Created         : 16.03.2023
#   Last Modified	: 16.03.2023
#   Version		    : 1.0
#   PIP             :
#   RESULT          :
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : cfg.py
# @echo off
# set ORACLE_HOME=C:\your\path\to\instantclient_11_2
# set PATH=%ORACLE_HOME%;%PATH%

from time import strftime   # Load just the strftime Module from Time


PORTAL_URL = "https:/SERVER/portal"
PORTAL_USER = ''
PORTAL_PASS = ''

SERVER_FOLDERS = ["", "FOLDER1", "FOLDER2"]


FILE_LOG_NAME = 'fastapi-files'
DATETIME_CURRENT = str(strftime("%Y-%m-%d-%H-%M-%S"))
FILE_LOG = DATETIME_CURRENT + '_' + FILE_LOG_NAME + '.log'
FILE_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
FOLDER_OUT = 'log'

CSV_DELIMITER = ','
CSV_FOLDER_OUT = 'out'
CSV_FILE = 'res_out.csv'
CSV_DICT = {'FIO': '',
            'EMAIL': '',
            'TEL': '',
            'PRIORITY': '',
            'CITY': '',
            'GENDER': '',
            'AGE': '',
            'OBR': '',
            'GR': '',
            'ZAN': '',
            'NAVIK': ''
            }