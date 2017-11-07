# -*- coding: utf-8 -*-

'''
    Project : "ArgusMedia"
    Module Name: Extract.py
    Created Date: 2016-07-13
    Scope: To download and push the file into s3 raw folder.

    Version:V1: 2016-9-13
    Details:
'''

from titlecase import titlecase
import glob, csv, xlwt, xlrd
import json
import re
import requests
import urlparse
import os
from datetime import datetime
import time
import sys
import imp
import ftplib
import moment

# Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/argus_media/study_transform/Fundalytics_Utility.py')
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/24/Fundalytics_Utility.py')
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import ast
import ftputil
import urllib2, cookielib
import xlsxwriter
from datetime import date, timedelta
from urlparse import urlparse
import itertools
from xlrd import open_workbook
from xlutils import copy

reload(sys)
sys.setdefaultencoding("utf-8")

date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))

# tempFilePath = "D:/argus_media/study_transform/temp/"
tempFilePath = "D:/01_2017/24/temp/"
if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)


def element_regex_apply(regex, content):
    element_list = []
    if ('REGEX' not in regex) and (regex != 'n/a'):
        if 'ROW' in regex:
            regex = regex.replace("ROW|", "")
            element_list = str(regex).split('|')

        else:

            element = str(regex).split('|')
            for ele in element:
                element_list.append(ele)

    elif ('REGEX' in regex) and (regex != 'n/a'):
        if "ROW" in regex:
            regex = regex.replace("ROW|", "")
            element_list = re.findall(str(regex).replace('REGEX|', ''), str(content), re.I)
        else:
            element = re.findall(str(regex).replace('REGEX|', ''), str(content), re.I)
            for ele in element:
                element_list.append(ele)

            # element_list = re.findall(str(regex).replace('REGEX|', ''),str(content),re.I)

    return element_list


def value_change(value_list,exp):
    val_list,val1_list,val2_list=[],[],[]

    for val1 in value_list:
        for val2 in val1:
            for val3 in val2:
                value=float(val3)
                val4=eval(exp)
                val1_list.append(val4)
            val2_list.append(val1_list)
            val1_list=[]
        val_list.append(val2_list)
        val2_list=[]

    return val_list

def utc_to_time_stamp(date_time, time_stamp):
    dt_list = []
    add_number = time_stamp['plus']
    minues_number = time_stamp['minues']
    for date_t in date_time:
        d = []
        for dt in date_t:
            date_format = moment.unix(float(dt))  # .format("%Y-%m-%d %H:%M:%S")
            # date_format = datetime.strptime(str(date_format), '%Y-%m-%dT%H:%M:%S+05.50') + relativedelta(
            #     minutes=add_number)
            try:
                date_format = datetime.strptime(str(date_format), '%Y-%m-%dT%H:%M:%S+05.50') + relativedelta(minutes=add_number)
            except ValueError:		
                date_format = datetime.strptime(str(date_format), '%Y-%m-%dT%H:%M:%S-00.00') + relativedelta(minutes=add_number)
            date_format = datetime.strptime(str(date_format), '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=minues_number)
            d.append(str(date_format))
            
        dt_list.append(d)

    return dt_list


def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x: not isinstance(x, (str, list, tuple)) or x,
                  (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))


##########################################'''single Date backfill'''####################################################
def singleDate_backFill(DataSourceID, url, control, datasourceName, marketName, backFillEnd):
    try:

        startDate = datetime.strptime(str(backFillEnd), '%Y-%m-%d')

        '''if both {DD-/+}{MM-/+}{YYYY-/+} and {DD}{MM}{YYYY} are in the url, It will be replaced with backFillStart date and its previous or future date'''
        if re.findall(r'\{DD(\W)(\d+)\}', str(url)) and '{DD}' in url or '{MM}' in url or '{YYYY}' in url:
            dateRegex = re.findall(r'\{DD(\W\d+)\}', url, re.I)
            for regex in dateRegex:
                PreviousDay = startDate + relativedelta(days=int(regex))
                day_value = "{DD\\" + regex + "}"
                url = re.sub(str(day_value), str(PreviousDay.strftime('%d')), url)
                month_value = "{MM\\" + regex + "}"
                url = re.sub(month_value, PreviousDay.strftime('%m'), url)
                year_value = "{YYYY\\" + regex + "}"
                url = re.sub(year_value, PreviousDay.strftime('%Y'), url)


        elif re.findall(r'\{DD(\W)(\d+)\}',
                        str(url)) and '{DD}' not in url and '{MM}' not in url and '{YYYY}' not in url:
            '''if {DD-/+}{MM-/+}{YYYY-/+} in the url,It will be replaced with backFillStart date'''
            selectionList = re.findall(r'\{DD(\W)(\d+)\}', str(url))
            for List in selectionList:
                if '-' in List[0]:
                    day_value = "{DD\\" + List[0] + List[1] + "}"
                    url = re.sub(str(day_value), str(startDate.strftime('%d')), url)
                    month_value = "{MM\\" + List[0] + List[1] + "}"
                    url = re.sub(str(month_value), str(startDate.strftime('%m')), url)
                    year_value = "{YYYY\\" + List[0] + List[1] + "}"
                    url = re.sub(str(year_value), str(startDate.strftime('%Y')), url)

        '''if {DD}{MM}{YYYY} in the url,It will be replaced with backFillStart date'''
        url = url.replace('{YYYY}', str(startDate.strftime('%Y')))
        url = url.replace('{DD}', str(startDate.strftime("%d")))
        url = url.replace('{MM}', str(startDate.strftime("%m")))
        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


##########################################'''back filling function'''######################################################
def backfilling(DataSourceID, url, control, datasourceName, marketName):
    try:
        backFillStart = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillFrom")
        print "backFillStart:",backFillStart
        backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
        print "backFillEnd:", backFillEnd
        if str(backFillStart) == str(backFillEnd):
            url = singleDate_backFill(DataSourceID, url, control, datasourceName, marketName, backFillEnd)
        elif str(backFillStart) != str(backFillEnd):

            backFillEnd = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
            startDate = datetime.strptime(str(backFillStart), '%Y-%m-%d %H:%M:%S')

            if re.findall(r'\{DD(\W)(\d+)\}', str(url)):
                selectionList = re.findall(r'\{DD(\W)(\d+)\}', str(url))
                for List in selectionList:
                    if '-' in List[0]:
                        day_value = "{DD\\" + List[0] + List[1] + "}"
                        url = re.sub(str(day_value), str(startDate.strftime('%d')), url)
                        month_value = "{MM\\" + List[0] + List[1] + "}"
                        url = re.sub(str(month_value), str(startDate.strftime('%m')), url)
                        year_value = "{YYYY\\" + List[0] + List[1] + "}"
                        url = re.sub(str(year_value), str(startDate.strftime('%Y')), url)

                        url = url.replace('{YYYY}', str(backFillEnd.strftime('%Y')))
                        url = url.replace('{DD}', str(backFillEnd.strftime("%d")))
                        url = url.replace('{MM}', str(backFillEnd.strftime("%m")))
                    elif '+' in List[0]:
                        # startDate = datetime.strptime(str(backFillStart), '%Y-%m-%d')
                        url = url.replace('{YYYY}', str(startDate.strftime('%Y')))
                        url = url.replace('{DD}', str(startDate.strftime("%d")))
                        url = url.replace('{MM}', str(startDate.strftime("%m")))

                        day_value = "{DD\\" + List[0] + List[1] + "}"
                        url = re.sub(str(day_value), str(backFillEnd.strftime('%d')), url)
                        month_value = "{MM\\" + List[0] + List[1] + "}"
                        url = re.sub(str(month_value), str(backFillEnd.strftime('%m')), url)
                        year_value = "{YYYY\\" + List[0] + List[1] + "}"
                        url = re.sub(str(year_value), str(backFillEnd.strftime('%Y')), url)

        url = url.replace('{HH:MIN}', time.strftime("%H:%M"))

        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


##########################################'''to find date in the url'''####################################################
'''url with date'''


def date_function(DataSourceID, url, control, datasourceName, marketName):
    try:
        if '{YYYY}' and '{MM}' and '{DD}' or '{YY}' or '{DD-' or '{ITA-MNAME}' or '{HH:MIN}' or '{ENG-MNAME}' or '{YYYY-' or '{MM-' or '{MM+' or '{YYYY+' in url:
            try:
                if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                    print "backfilling"
                    backFillStart = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillFrom")
                    backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                    startDate = datetime.strptime(str(backFillStart), '%Y-%m-%d %H:%M:%S')
                    print "startDate:", startDate
                    limit = "limit=" + str((datetime.now() - startDate ).days)
                    print "limit:", limit
                    if re.findall(r'(limit\=\d+)', url, re.I):
                        # print "substituiton"
                        substitution = re.findall(r'(limit\=\d+)', url, re.I)
                        url = re.sub(substitution[0], limit, url)
                        print "url inside backfillin:",url
                    url = backfilling(DataSourceID, url, control, datasourceName, marketName)
                else:
                    raise Exception

            except Exception as e:
                # print str(e) + "\nline no:",str(sys.exc_traceback.tb_lineno)

                url = url.replace('{YY}', time.strftime("%y"))
                url = url.replace('{DD}', time.strftime("%d"))
                now = datetime.now()

                '''modification of day using regex'''
                if re.search(r'\{DD(\W)(\d+)\}', str(url)):
                    '''for loop used for more than one date change in the url'''
                    dateRegex = re.findall(r'\{DD(\W\d+)\}', url, re.I)
                    for regex in dateRegex:
                        PreviousDay = now + relativedelta(days=int(regex))
                        day_value = "{DD\\" + regex + "}"
                        url = re.sub(str(day_value), str(PreviousDay.strftime('%d')), url)
                        month_value = "{MM\\" + regex + "}"
                        url = re.sub(month_value, PreviousDay.strftime('%m'), url)
                        year_value = "{YYYY\\" + regex + "}"
                        url = re.sub(year_value, PreviousDay.strftime('%Y'), url)

                url = url.replace('{MM}', time.strftime("%m"))
                if re.search(r'\{YYYY(\W)(\d+)', str(url)):
                    yearRegex = re.findall(r'\{YYYY(\W\d+)\}', url, re.I)
                    for regex in yearRegex:
                        PreviousYear = now + relativedelta(years=int(regex))
                        yearValue = "{YYYY\\" + str(regex) + '}'
                        url = re.sub(yearValue, PreviousYear.strftime('%Y'), url)

                url = url.replace('{YYYY}', time.strftime("%Y"))

                url = url.replace('{HH:MIN}', time.strftime("%H:%M"))

            return url

    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


####################################################'''json file'''####################################################

def jsonfileContent(DataSourceID, datasourceName, marketName, scraperParameterName, url, method, control, wb,
                    scraper_parameters):
    try:

        print "scraperParameterName:", scraperParameterName
        print "sheet_name:", scraper_parameters
        sheet_name = scraper_parameters
        filed = 1
        col_pos = 0
        sh = wb.add_worksheet(sheet_name)

        print "url:", url
        regex1 = control.get(scraperParameterName, 'E_REGEX1')
        regex2 = control.get(scraperParameterName, 'E_REGEX2')
        regex3 = control.get(scraperParameterName, 'E_REGEX3')
        applies_date_regex = control.get(scraperParameterName, 'E_ADATE')
        public_date_regex = control.get(scraperParameterName, 'E_PDATE')
        applies_hour_regex = control.get(scraperParameterName, 'E_AHOUR')
        public_hour_regex = control.get(scraperParameterName, 'E_PHOUR')
        value_regex = control.get(scraperParameterName, 'E_VALUE')
        value_position = control.get(scraperParameterName, 'E_VALUE_POSITION')
        field1_regex = control.get(scraperParameterName, 'E_FIELD1')
        field2_regex = control.get(scraperParameterName, 'E_FIELD2')
        field3_regex = control.get(scraperParameterName, 'E_FIELD3')
        field4_regex = control.get(scraperParameterName, 'E_FIELD4')
        field5_regex = control.get(scraperParameterName, 'E_FIELD5')
        field6_regex = control.get(scraperParameterName, 'E_FIELD6')
        field7_regex = control.get(scraperParameterName, 'E_FIELD7')
        field8_regex = control.get(scraperParameterName, 'E_FIELD8')
        field9_regex = control.get(scraperParameterName, 'E_FIELD9')
        val_change = control.get(scraperParameterName, 'VALUE_CHANGES')
        utc_time_stamp = control.get(scraperParameterName, 'UTC_TIME_STAMP')
        field1_regex_element, field2_regex_element, field3_regex_element, field4_regex_element, field5_regex_element, field6_regex_element, field7_regex_element, field8_regex_element, field9_regex_element = [], [], [], [], [], [], [], [], []
        # contentReplace = control.get(scraperParameterName,'REPLACEMENT')

        field1_value_regex = field2_value_regex = field3_value_regex = field4_value_regex = field5_value_regex = field6_value_regex = field7_value_regex = field8_value_regex = field9_value_regex = 'n/a'
        url_run = control.get(scraperParameterName, 'JSON_URL_RUN')
        replace_apply = control.get(scraperParameterName, 'REPLACE_APPLY')

        field1_value_block, field2_value_block, field3_value_block, field4_value_block, field5_value_block, field6_value_block, field7_value_block, field8_value_block, field9_value_block, value_block_list, applies_date_list, public_date_list, applies_time_list, public_time_list, f1_value_list, f2_value_list, f3_value_list, f4_value_list, f5_value_list, f6_value_list, f7_value_list, f8_value_list, f9_value_list = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        val_flag = 0
        f1_flag = f2_flag = f3_flag = f4_flag = applies_date_flag = public_date_flag = public_hour_flag = applies_hour_flag = 0
        if url_run == 'n/a':
            if method == 'GET':
                url = date_function(DataSourceID, url, control, datasourceName, marketName)
                con = requests.get(url)
                data = con.content
                data = data.replace('&nbsp;',' ')

            elif method == 'POST':
                cookie_file = '/tmp/cookies'
                cj = cookielib.LWPCookieJar(cookie_file)

                s = requests.Session()
                s.cookies = cj

                con = s.get(url)
                home_con = con.content

                head = control.get(scraperParameterName, 'E_METHOD').split('|')

                # header = date_function(DataSourceID, str(head), control, datasourceName, marketName)

                header = ast.literal_eval(head[1])
                post_content = date_function(DataSourceID, control.get(scraperParameterName, 'E_POSTCONTENT'), control,
                                             datasourceName, marketName)
                post_url = date_function(DataSourceID, control.get(scraperParameterName, 'E_POSTURL'), control,
                                         datasourceName, marketName)
                '''Requesting content by post method'''
                post_response = s.post(url=post_url, data=post_content, cookies=con.cookies, headers=header)
                data = post_response.content
                with open("output.json", "w") as F:
                    F.write(data)

            if replace_apply != 'n/a':
                replace_apply = replace_apply.split('#')
                for rep in replace_apply:
                    rep1 = rep.split('|')
                    data = data.replace(rep1[0], rep1[1])

        else:
            if method == 'GET':
                data = ''
                for x in range(1, int(url_run)):
                    url = re.sub(r'YYYY\-[\d]+', 'YYYY-' + str(x), url)
                    url = re.sub(r'MM\-[\d]+', 'MM-' + str(x), url)
                    url = re.sub(r'DD\-[\d]+', 'DD-' + str(x), url)
                    url = date_function(DataSourceID, url, control, datasourceName, marketName)
                    # if method == 'GET':
                    con = requests.get(url)
                    d = con.content
                    data = data + d

                if replace_apply != 'n/a':
                    replace_apply = replace_apply.split('#')
                    for rep in replace_apply:
                        rep1 = rep.split('|')
                        data = data.replace(rep1[0], rep1[1])

        if regex1 != 'n/a':

            regex1_block_list = re.findall(regex1, str(data), re.I)
            value_final = []
            element1, element2, element3, element4, element5, element6, element7, element8, element9 = [], [], [], [], [], [], [], [], []

            if regex2 != 'n/a':

                for regex1_list in regex1_block_list:
                    regex2_block_list = re.findall(regex2, str(regex1_list), re.I)
                    if regex3 != 'n/a':

                        for regex2_list in regex2_block_list:
                            regex3_block_list = re.findall(regex3, str(regex2_list), re.I)
                            for regex3_list in regex3_block_list:
                                value_block_list.append(re.findall(value_regex, str(regex3_list), re.I))
                                field1_regex_element.append(element_regex_apply(field1_regex, regex3_list))
                                field2_regex_element.append(element_regex_apply(field2_regex, regex3_list))
                                field3_regex_element.append(element_regex_apply(field3_regex, regex3_list))
                                field4_regex_element.append(element_regex_apply(field4_regex, regex3_list))
                                field5_regex_element.append(element_regex_apply(field5_regex, regex3_list))
                                field6_regex_element.append(element_regex_apply(field6_regex, regex3_list))
                                field7_regex_element.append(element_regex_apply(field7_regex, regex3_list))
                                field8_regex_element.append(element_regex_apply(field8_regex, regex3_list))
                                field9_regex_element.append(element_regex_apply(field9_regex, regex3_list))
                    else:

                        for regex2_list in regex2_block_list:
                            value_block_list.append(re.findall(value_regex, str(regex2_list), re.I))
                            field1_regex_element.append(element_regex_apply(field1_regex, regex2_list))
                            field2_regex_element.append(element_regex_apply(field2_regex, regex2_list))
                            field3_regex_element.append(element_regex_apply(field3_regex, regex2_list))
                            field4_regex_element.append(element_regex_apply(field4_regex, regex2_list))
                            field5_regex_element.append(element_regex_apply(field5_regex, regex2_list))
                            field6_regex_element.append(element_regex_apply(field6_regex, regex2_list))
                            field7_regex_element.append(element_regex_apply(field7_regex, regex2_list))
                            field8_regex_element.append(element_regex_apply(field8_regex, regex2_list))
                            field9_regex_element.append(element_regex_apply(field9_regex, regex2_list))

                    value_final.append(value_block_list)
                    element1.append(field1_regex_element)
                    element2.append(field2_regex_element)
                    element3.append(field3_regex_element)
                    element4.append(field4_regex_element)
                    element5.append(field5_regex_element)
                    element6.append(field6_regex_element)
                    element7.append(field7_regex_element)
                    element8.append(field8_regex_element)
                    element9.append(field9_regex_element)
                    value_block_list = []
                    field1_regex_element, field2_regex_element, field3_regex_element, field4_regex_element, field5_regex_element, field6_regex_element, field7_regex_element, field8_regex_element, field9_regex_element = [], [], [], [], [], [], [], [], []
            else:

                for regex1_list in regex1_block_list:
                    value_block_list.append(re.findall(value_regex, str(regex1_list), re.I))
                    field1_regex_element.append(element_regex_apply(field1_regex, regex1_list))
                    field2_regex_element.append(element_regex_apply(field2_regex, regex1_list))
                    field3_regex_element.append(element_regex_apply(field3_regex, regex1_list))
                    field4_regex_element.append(element_regex_apply(field4_regex, regex1_list))
                    field5_regex_element.append(element_regex_apply(field5_regex, regex1_list))
                    field6_regex_element.append(element_regex_apply(field6_regex, regex1_list))
                    field7_regex_element.append(element_regex_apply(field7_regex, regex1_list))
                    field8_regex_element.append(element_regex_apply(field8_regex, regex1_list))
                    field9_regex_element.append(element_regex_apply(field9_regex, regex1_list))
                    value_final.append(value_block_list)
                    value_block_list = []

                    element1.append(field1_regex_element)
                    element2.append(field2_regex_element)
                    element3.append(field3_regex_element)
                    element4.append(field4_regex_element)
                    element5.append(field5_regex_element)
                    element6.append(field6_regex_element)
                    element7.append(field7_regex_element)
                    element8.append(field8_regex_element)
                    element9.append(field9_regex_element)
                    value_block_list = []
                    field1_regex_element, field2_regex_element, field3_regex_element, field4_regex_element, field5_regex_element, field6_regex_element, field7_regex_element, field8_regex_element, field9_regex_element = [], [], [], [], [], [], [], [], []

            applies_date_list, applies_time_list, publish_date_list, publish_time_list = [], [], [], []
            for regex1_list in regex1_block_list:
                if applies_date_regex != 'n/a':
                    applies_date = re.findall(applies_date_regex, str(regex1_list), re.I)
                    applies_date_list.append(applies_date)
                if applies_hour_regex != 'n/a':
                    applies_hr = re.findall(applies_hour_regex, str(regex1_list), re.I)
                    applies_time_list.append(applies_hr)
                if public_date_regex != 'n/a':
                    publish_date = re.findall(public_date_regex, str(regex1_list), re.I)
                    publish_date_list.append(publish_date)
                if public_hour_regex != 'n/a':
                    publish_hr = re.findall(public_hour_regex, str(regex1_list), re.I)
                    publish_time_list.append(publish_hr)
            if val_change != 'n/a':
                value_final = value_change(value_final, val_change)
            if utc_time_stamp != 'n/a':
                time_stamp = ast.literal_eval(utc_time_stamp)
                applies_date_list = utc_to_time_stamp(applies_date_list, time_stamp['appies_date'])
                publish_date_list = utc_to_time_stamp(publish_date_list, time_stamp['publish_date'])

            element_col_inc, element_row_inc, date_row_inc, date_col_inc = 0, 0, 0, 0

            element_row_inc1, element_row_inc2, element_row_inc3, element_row_inc4, element_row_inc5, element_row_inc6, element_row_inc7, element_row_inc8, element_row_inc9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
            element_col_inc1, element_col_inc2, element_col_inc3, element_col_inc4, element_col_inc5, element_col_inc6, element_col_inc7, element_col_inc8, element_col_inc9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
            row = 0
            main_row1, main_row2, main_row3, main_row4, main_row5, main_row6, main_row7, main_row8, main_row9 = 0, 0, 0, 0, 0, 0, 0, 0, 0

            for i, value_block_list in enumerate(value_final):
                element_col_inc1, element_col_inc2, element_col_inc3, element_col_inc4, element_col_inc5, element_col_inc6, element_col_inc7, element_col_inc8, element_col_inc9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
                for j, value_list in enumerate(value_block_list):
                    element_row_inc1, element_row_inc2, element_row_inc3, element_row_inc4, element_row_inc5, element_row_inc6, element_row_inc7, element_row_inc8, element_row_inc9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
                    for k, val in enumerate(value_list):

                        col = 0
                        if applies_date_regex != 'n/a':
                            applies_date = applies_date_list[date_col_inc][date_row_inc]
                            sh.write(row, col, applies_date)
                            col = col + 1
                        if applies_hour_regex != 'n/a':
                            applies_hour = applies_time_list[date_col_inc][date_row_inc]
                            sh.write(row, col, applies_hour)
                            col = col + 1
                        if public_date_regex != 'n/a':
                            publish_date = publish_date_list[date_col_inc][date_row_inc]
                            sh.write(row, col, publish_date)
                            col = col + 1
                        if public_hour_regex != 'n/a':
                            publish_hour = publish_time_list[date_col_inc][date_row_inc]
                            sh.write(row, col, publish_hour)
                            col = col + 1
                        if field1_regex != 'n/a':
                            element = element1[main_row1][element_col_inc1][element_row_inc1]

                            sh.write(row, col, element)
                            col = col + 1
                        if field2_regex != 'n/a':
                            element = element2[main_row2][element_col_inc2][element_row_inc2]

                            sh.write(row, col, element)
                            col = col + 1
                        if field3_regex != 'n/a':
                            element = element3[main_row3][element_col_inc3][element_row_inc3]

                            sh.write(row, col, element)
                            col = col + 1
                        if field4_regex != 'n/a':
                            element = element4[main_row4][element_col_inc4][element_row_inc4]

                            sh.write(row, col, element)
                            col = col + 1
                        if field5_regex != 'n/a':
                            element = element5[main_row5][element_col_inc5][element_row_inc5]
                            sh.write(row, col, element)
                            col = col + 1
                        if field6_regex != 'n/a':
                            element = element6[main_row6][element_col_inc6][element_row_inc6]
                            sh.write(row, col, element)
                            col = col + 1
                        if field7_regex != 'n/a':
                            element = element7[main_row7][element_col_inc7][element_row_inc7]
                            sh.write(row, col, element)
                            col = col + 1
                        if field8_regex != 'n/a':
                            element = element8[main_row8][element_col_inc8][element_row_inc8]
                            sh.write(row, col, element)
                            col = col + 1
                        if field9_regex != 'n/a':
                            element = element9[main_row9][element_col_inc9][element_row_inc9]
                            sh.write(row, col, element)
                            col = col + 1
                        sh.write(row, col, val)
                        col = col + 1

                        if len(value_list) == len(element1[main_row1][element_col_inc1]):
                            if len(element1[main_row1][element_col_inc1]) > 1:
                                element_row_inc1 = element_row_inc1 + 1

                        if len(value_list) == len(element2[main_row2][element_col_inc2]):
                            if len(element2[main_row2][element_col_inc2]) > 1:
                                element_row_inc2 = element_row_inc2 + 1

                        if len(value_list) == len(element3[main_row3][element_col_inc3]):
                            if len(element3[main_row3][element_col_inc3]) > 1:
                                element_row_inc3 = element_row_inc3 + 1

                        if len(value_list) == len(element4[main_row4][element_col_inc4]):
                            if len(element4[main_row4][element_col_inc4]) > 1:
                                element_row_inc4 = element_row_inc4 + 1

                        if len(value_list) == len(element5[main_row5][element_col_inc5]):
                            if len(element5[main_row5][element_col_inc5]) > 1:
                                element_row_inc5 = element_row_inc5 + 1

                        if len(value_list) == len(element6[main_row6][element_col_inc6]):
                            if len(element6[main_row6][element_col_inc6]) > 1:
                                element_row_inc6 = element_row_inc6 + 1

                        if len(value_list) == len(element7[main_row7][element_col_inc7]):
                            if len(element7[main_row7][element_col_inc7]) > 1:
                                element_row_inc7 = element_row_inc7 + 1

                        if len(value_list) == len(element8[main_row8][element_col_inc8]):
                            if len(element8[main_row8][element_col_inc8]) > 1:
                                element_row_inc8 = element_row_inc8 + 1

                        if len(value_list) == len(element9[main_row9][element_col_inc9]):
                            if len(element9[main_row9][element_col_inc9]) > 1:
                                element_row_inc9 = element_row_inc9 + 1

                        if len(value_list) == len(applies_date_list[date_col_inc]):
                            if len(applies_date_list[date_col_inc]) > 1:
                                date_row_inc = date_row_inc + 1
                        row = row + 1

                    if len(value_block_list) == len(element1[main_row1]):
                        if len(element1[main_row1]) > 1:
                            element_col_inc1 = element_col_inc1 + 1

                    if len(value_block_list) == len(element2[main_row2]):
                        if len(element2[main_row2]) > 1:
                            element_col_inc2 = element_col_inc2 + 1

                    if len(value_block_list) == len(element3[main_row3]):
                        if len(element3[main_row3]) > 1:
                            element_col_inc3 = element_col_inc3 + 1

                    if len(value_block_list) == len(element4[main_row4]):
                        if len(element4[main_row4]) > 1:
                            element_col_inc4 = element_col_inc4 + 1
                    if len(value_block_list) == len(element5[main_row5]):
                        if len(element5[main_row5]) > 1:
                            element_col_inc5 = element_col_inc5 + 1

                    if len(value_block_list) == len(element6[main_row6]):
                        if len(element6[main_row6]) > 1:
                            element_col_inc6 = element_col_inc6 + 1

                    if len(value_block_list) == len(element7[main_row7]):
                        if len(element7[main_row7]) > 1:
                            element_col_inc7 = element_col_inc7 + 1

                    if len(value_block_list) == len(element8[main_row8]):
                        if len(element8[main_row8]) > 1:
                            element_col_inc8 = element_col_inc8 + 1

                    if len(value_block_list) == len(element9[main_row9]):
                        if len(element9[main_row9]) > 1:
                            element_col_inc9 = element_col_inc9 + 1

                    if len(value_block_list) == len(applies_date_list):
                        if len(applies_date_list) > 1:
                            date_col_inc = date_col_inc + 1

                if len(value_final) == len(element1):
                    if len(element1) > 1:
                        main_row1 = main_row1 + 1

                if len(value_final) == len(element2):
                    if len(element2) > 1:
                        main_row2 = main_row2 + 1
                if len(value_final) == len(element3):
                    if len(element3) > 1:
                        main_row3 = main_row3 + 1

                if len(value_final) == len(element4):
                    if len(element4) > 1:
                        main_row4 = main_row4 + 1

                if len(value_final) == len(element5):
                    if len(element5) > 1:
                        main_row5 = main_row5 + 1
                if len(value_final) == len(element6):
                    if len(element6) > 1:
                        main_row6 = main_row6 + 1

                if len(value_final) == len(element7):
                    if len(element7) > 1:
                        main_row7 = main_row7 + 1

                if len(value_final) == len(element8):
                    if len(element8) > 1:
                        main_row8 = main_row8 + 1

                if len(value_final) == len(element9):
                    if len(element9) > 1:
                        main_row9 = main_row9 + 1

                if len(value_block_list) == len(applies_date_list[i]):
                    if len(applies_date_list) > 1:
                        date_col_inc = date_col_inc + 1

        return 0
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


####################################################'''Main function'''########################################################
''' Execution starts from Main function '''


# if __name__ == "__main__":
def main(control):
	try:
		'''Get all the arguments from scrapy'''
		DataSourceID = control.dsId
		datasourceName = control.dsName
		marketName = control.mName
		spName = control.scraperParameterName.split('/')
		print DataSourceID, datasourceName, marketName, spName

		s3path_upload = 'data/raw/' + str(datasourceName) + '/' + str(marketName) + '/1.0/'

		try:
			if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
				backFillEnd = control.get("backfill_data-" + str(marketName), str(datasourceName) + "BackFillTo")
				backFillEnd = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
				date_time = str(backFillEnd.strftime('%Y%m%d_%H%M'))
			else:
				raise Exception
		except Exception as e:
			date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))

		rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
		rawFileName = tempFilePath + str(rawFile_time).replace('-', '_') + ".xlsx"

		wb = xlsxwriter.Workbook(rawFileName)

		'''looping through the scraper parameter name'''
		for scraper_parameters in spName:
			scraperParameterName = 'E-' + str(datasourceName) + '-' + str(marketName) + '-' + str(
				scraper_parameters).strip()
			print scraperParameterName

			'''getting url from scraperparameter'''
			get_url_to_scrape = control.get(scraperParameterName, 'URL')
			# print get_url_to_scrape_date

			method = control.get(scraperParameterName, 'E_METHOD').split('|')

			scraperType = control.get(scraperParameterName, 'SCRAPERTYPE').lower()

			# if scraperType=='json' and method[0]=='GET':
			if scraperType == 'json':

				jsonfileContent(DataSourceID, datasourceName, marketName, scraperParameterName, get_url_to_scrape,
								method[0], control, wb, scraper_parameters)

			elif scraperType == 'json' and method[0] == 'POST':
				head = method[1]
				post_content = date_function(DataSourceID, control.get(scraperParameterName, 'E_POSTCONTENT'), control,
											 datasourceName, marketName)
			# postJson(get_url_to_scrape, post_content, DataSourceID, datasourceName, marketName, scraperType,scraperParameterName, control, head)
			# jsonfileContent(get_url_to_scrape, post_content, DataSourceID, datasourceName, marketName, scraperType,scraperParameterName, control, head)

		wb.close()

		s3File = rawFileName
		successStatus = 1
		print "s3File:", s3File

		if successStatus == 1:

			# Fundalytics_Utility.s3_fileupload(s3File, DataSourceID, s3path_upload, 'Extract', control)

			print "Uploaded Completed"

			Fundalytics_Utility.log(DataSourceID, 'Extract-Module', '', 'Extracted',
									str(s3path_upload) + str(str(s3File).replace(tempFilePath, '')))
			control.add_section('status')

			control.add_section('filename')
			control.set("filename", "extractfilename", str(s3File).replace(tempFilePath, ''))

			# os.remove(rawFileName)
			control.set("status", "extractStatus", "1")
			print  "Extraction Completed for " + str(DataSourceID)
			return control
		else:
			Fundalytics_Utility.log(DataSourceID, 'Extract', 'File Error on extraction', 'Error', '')
			control.set("status", "extractStatus", "0")

	except Exception as e:
		print "Exception::" + str(e)
		print  "Error on extraction for " + str(DataSourceID)
		print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
		Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
								'Error', '')
		return control





