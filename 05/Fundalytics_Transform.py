# -*- coding: utf-8 -*-
'''
    Project : "ArgusMedia"
    Created Date: 2016-07-13
    Module Name: Transform_v2.1.py
    Scope: To convert raw file into cooked file.

    Version:V1: 2016-8-18

'''

''' Import required modules '''

import imp
import ConfigParser
import sys, os
import xlrd
import codecs
import re
from bs4 import BeautifulSoup
from io import BytesIO
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta, date
from titlecase import titlecase
import ast
import csv
from collections import defaultdict
import collections
import imp
from time import gmtime, strftime
import time
from dateutil.relativedelta import relativedelta

Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/05/Fundalytics_Utility.py')
# Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/MuthuBabu/Argus_media/development/Argusmedia/Fundalytics_Utility.py')

reload(sys)
sys.setdefaultencoding("utf-8")

now = datetime.now()
''' get current data time '''

tempFilePath = "D:/01_2017/05/temp/"
# tempFilePath = "D:/MuthuBabu/Argus_media/development/Argusmedia/temp/"
if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)


def datecomparison(comparisonConditon, Element_condition, Element_value_condition, applies_temp_check,publication_temp_check, current_temp_check, e1_condition, e2_condition, e3_condition, e4_condition,e5_condition, e6_condition, e7_condition, e8_condition, e9_condition):
    comparison_condition = ''
    if str(comparisonConditon) == 'appliestime < publicationtime':
        if applies_temp_check < publication_temp_check:
            comparison_condition = 'True'

            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    elif str(comparisonConditon) == 'appliestime = publicationtime':
        if applies_temp_check == publication_temp_check:
            comparison_condition = 'True'
            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    elif str(comparisonConditon) == 'appliestime > publicationtime':
        if applies_temp_check > publication_temp_check:
            comparison_condition = 'True'
            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    elif str(comparisonConditon) == 'appliestime < currenttime':
        if applies_temp_check < current_temp_check:
            comparison_condition = 'True'
            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    elif str(comparisonConditon) == 'appliestime = currenttime':
        if applies_temp_check == current_temp_check:
            comparison_condition = 'True'
            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    elif str(comparisonConditon) == 'appliestime > currenttime':
        if applies_temp_check > current_temp_check:
            comparison_condition = 'True'
            if str(Element_condition) == 'Element01':
                e1_condition = Element_value_condition
            elif str(Element_condition) == 'Element02':
                e2_condition = Element_value_condition
            elif str(Element_condition) == 'Element03':
                e3_condition = Element_value_condition
            elif str(Element_condition) == 'Element04':
                e4_condition = Element_value_condition
            elif str(Element_condition) == 'Element05':
                e5_condition = Element_value_condition
            elif str(Element_condition) == 'Element06':
                e6_condition = Element_value_condition
            elif str(Element_condition) == 'Element07':
                e7_condition = Element_value_condition
            elif str(Element_condition) == 'Element08':
                e8_condition = Element_value_condition
            elif str(Element_condition) == 'Element09':
                e9_condition = Element_value_condition
    else:
        comparison_condition = 'False'
    if str(comparison_condition) == "":
        comparison_condition = 'False'
    return comparison_condition, e1_condition, e2_condition, e3_condition, e4_condition, e5_condition, e6_condition, e7_condition, e8_condition, e9_condition


def translate(t_element, t_condition, t_dict_word):
    t_element = re.sub(r'<[^>]*?>', ' ', str(t_element))
    t_element = re.sub(r'\s+\s*', ' ', str(t_element))
    t_element = re.sub(r'^\s+\s*', '', str(t_element))
    t_element = re.sub(r'\s+\s*', ' ', str(t_element))
    t_element = re.sub(r'\s+\s*$', '', str(t_element))
    if str(t_element) != 'n/a':
        if str(t_condition) == 'yes':
            t_dict = ast.literal_eval(t_dict_word)
            t_matched_word = ''
            for key in t_dict:
                if str(key) == str(t_element):
                    t_matched_word = t_dict[key]
            if str(t_matched_word) != '':
                return t_matched_word
            else:
                return t_element
        else:
            return t_element
    else:
        return t_element


def value_replace(value_replace1):
    value_replace1 = value_replace1.replace('.', '')
    value_replace1 = value_replace1.replace(',', '.')
    if '.' in str(value_replace1):
        value_replace1 = round(float(value_replace1), 3)

    return value_replace1

def value_replace_spl (value_replace2):
    if re.search(r'^\d+\,\d{1,2}$', str(value_replace2)):
        
        value_replace2 = value_replace2.replace(',','.')
    else:
        value_replace2 = value_replace2.replace(',','')
   
    return value_replace2


def element_splitup(element_data, text):
    element_list = []
    if ('REGEX' not in element_data) and (element_data != 'n/a'):
        element_list = str(element_data).split('|')
    elif ('REGEX' in element_data) and (element_data != 'n/a'):
        element_list = re.findall(str(element_data).replace('{', '').replace('}', '').replace('REGEX', ''), str(text),
                                  re.IGNORECASE)
    return element_list


def date_formation(month, date):
    '''
        Format the date, while getting only month and date from raw file
    '''
    if re.search(r'[A-Za-z]+', str(month)):
        month_dict = {'JAN': '01', 'JAN.': '01', 'JANUARY': '01', 'Jan': '01', 'Jan.': '01', 'January': '01',
                      'FEB': '02', 'FEB.': '02', 'FEBRUARY': '02', 'Feb': '02', 'Feb.': '02', 'February': '02',
                      'MAR': '03', 'MAR.': '03', 'MARCH': '03', 'Mar': '03', 'Mar.': '03', 'March': '03', 'APR': '04',
                      'APR.': '04', 'APRIL': '04', 'Apr': '04', 'Apr.': '04', 'April': '04', 'MAY': '05', 'May': '05',
                      'JUN': '06', 'JUN.': '06', 'JUNE': '06', 'Jun': '06', 'Jun.': '06', 'June': '06', 'JUL': '07',
                      'JUL.': '07', 'JULY': '07', 'Jul': '07', 'Jul.': '07', 'July': '07', 'AUG': '08', 'AUG.': '08',
                      'AUGUST': '08', 'Aug': '08', 'Aug.': '08', 'August': '08', 'SEP': '09', 'Sep': '09', 'SEP.': '09',
                      'Sep.': '09', 'SEPT': '09', 'Sept': '09', 'SEPT.': '09', 'Sept.': '09', 'SEPTEMBER': '09',
                      'September': '09', 'OCT': '10', 'Oct': '10', 'OCT.': '10', 'Oct.': '10', 'OCTOBER': '10',
                      'October': '10', 'NOV': '11', 'Nov': '11', 'NOV.': '11', 'Nov.': '11', 'NOVEMBER': '11',
                      'November': '11', 'DEC': '12', 'DEC.': '12', 'DECEMBER': '12', 'Dec': '12', 'Dec.': '12',
                      'December': '12'}
        for key in month_dict:
            if str(month) == str(key):
                month = month_dict[key]

    formated_date = str(now.year) + "-" + str(month) + "-" + str(date)

    return formated_date


def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x: not isinstance(x, (str, list, tuple)) or x,
                  (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))


def clean_fn(clean_test):
    '''
        Data cleaning function
    '''

    clean_test = re.sub(r'<td[^>]*?>\s*<[^>]*?>\s*<[^>]*?>', '', str(clean_test))
    clean_test = re.sub(r'<\/span[^>]*?>\s*<[^>]*?>\s*<[^>]*?>', '', str(clean_test))
    clean_test = re.sub(r'<[^>]*?>', '', str(clean_test))
    clean_test = re.sub(r'^\\n\s+\s*', '', str(clean_test))
    clean_test = re.sub(r'\<', '', str(clean_test))
    # clean_test = re.sub(r'\*', '', str(clean_test))
    # clean_test = re.sub(r'\)', '', str(clean_test))
    # clean_test = re.sub(r'\(', '', str(clean_test))
    clean_test = re.sub(r'^\\r\\n\s*', '', str(clean_test))

    return clean_test


def element_split_function(element_split, value):
    '''
        Regex Split function:
            1. Input Regex and value
            2. Return the grouped value
    '''

    if ('REGEX' not in element_split) and (element_split != 'n/a'):
        element_list = value
        return element_list
    elif ('REGEX' in element_split) and (element_split != 'n/a'):
        element_list = re.findall(str(element_split).replace('{', '').replace('}', '').replace('REGEX', ''), str(value),
                                  re.IGNORECASE)
        return element_list[0]


def value_increment(val_list, element_list, increment_value):
    '''
        Value Incerment:
            1. Compare the two list and increment the row and column.
    '''
    if (len(val_list) == len(element_list)):
        increment_value = increment_value + 1

    return increment_value


def csv_element_extraction(content, values_position, element_split, max_col, max_row):
    '''
       Value Extraction:
           1. Input : Content, Value position and element_split (Hard coded element or Regex)
           2. push the values into the list
    '''

    if str(values_position) == 'n/a' and str(element_split) == 'n/a':
        val1 = []
        val2 = []
        val1.append('n/a')
        val2.append(val1)
        return val2
    elif str(values_position) != 'n/a':

        positions = ast.literal_eval(values_position)
        row_st, row_end, col_st, col_end = '', '', '', ''
        row_st = positions.get('start_row')
        row_end = positions.get('end_row')
        col_st = positions.get('start_col')
        col_end = positions.get('end_col')

        if str(row_end) == "max":
            row_end = max_row
        if str(row_end) == "max-1":
            row_end = int(max_row) - 1
        if str(col_end) == "max":
            col_end = max_col
        if str(col_end) == "max-1":
            col_end = int(max_col) - 1

        val1 = []
        val2 = []
        for col_number in range(col_st, int(col_end)):
            for row_number in range(row_st, int(row_end)):
                try:
                    if str(element_split) == 'n/a':
                        val1.append(content[row_number][col_number])
                    else:
                        val1.append(element_split_function(element_split, (content[row_number][col_number])))
                except:
                    val1.append('')
            val2.append(val1)
            val1 = []
        return val2
    elif str(values_position) == 'n/a':
        val1 = []
        val2 = []
        if 'ROW{' not in str(element_split):
            element_split = str(element_split).split('|')
            for val in element_split:
                val1.append(val)
                val2.append(val1)
                val1 = []
        else:
            element_split = str(element_split).replace('ROW{', '').replace('}', '')
            element_split = str(element_split).split('|')
            val2.append(element_split)
        return val2


def Get_Excel_Elements(sheet, element, element_Position, max_row):
    '''
        Function : To get the elements from excel
        Summary:
            1. Argument "sheet" - Contains Excel sheet object
            2. Argument "element" - Contains hardcoded elements or Regex to get Elements
            3. Argument "element_Position" - Contains elements cell position (i.e. start row, End row, Start col, End col)
            4. Apply the mentioned position & regex or split the hard coded Elements to get Elements and append in list.
    '''
    element_list = []
    Element_List_Temp = []
    if (element_Position != 'n/a'):
        positions = ast.literal_eval(element_Position)
        row_st, row_end, col_st, col_end = '', '', '', ''
        row_st = positions.get('start_row')
        row_end = positions.get('end_row')
        col_st = positions.get('start_col')
        col_end = positions.get('end_col')

        if str(row_end) == "max":
            row_end = max_row

        for col in range(int(col_st), int(col_end)):
            Element_raw = ''
            for row in range(int(row_st), int(row_end)):
                try:
                    Element_raw = sheet.cell(row, col).value
                except:
                    Element_raw=''    
                if ('REGEX' in element):
                    Element_raw = re.findall(str(element).replace('{', '').replace('}', '').replace('REGEX', ''),
                                             str(Element_raw), re.IGNORECASE)
                    if Element_raw:
                        Element_raw = Element_raw[0]
                    else:
                        Element_raw = ''

                Element_raw = re.sub(r'\\r', ' ', str(Element_raw))
                Element_raw = re.sub(r'\\n', ' ', str(Element_raw))
                Element_raw = re.sub(r'\s+\s*', ' ', str(Element_raw))
                Element_List_Temp.append(str(Element_raw))
            element_list.append(Element_List_Temp)
            Element_List_Temp = []
    elif (element != 'n/a'):
        element_temp_1 = []
        if 'ROW{' not in str(element):
            element_temp = element.split('|')
            for tt in element_temp:
                element_temp_1.append(tt)
                element_list.append(element_temp_1)
                element_temp_1 = []
        else:
            element = str(element).replace('ROW{', '').replace('}', '')
            element_temp_1 = str(element).split('|')
            element_list.append(element_temp_1)
    else:
        element_temp = ['n/a']
        # element_temp.append(element_temp)
        element_list.append(element_temp)

    return element_list


def Get_Excel_Values(sheet, value_positions, max_row):
    '''
        Function : To get the elements from excel
        Summary:
            1. Argument "sheet" - Contains Excel sheet object
            2. Argument "value_positions" - Contains values cell position (i.e. start row, End row, Start col, End col)
            4. Apply the mentioned position & regex to get Elements and append in list.
    '''
    Values_list = []
    Values1 = []
    positions = ast.literal_eval(value_positions)
    row_st, row_end, col_st, col_end = '', '', '', ''
    row_st = positions.get('start_row')
    row_end = positions.get('end_row')
    col_st = positions.get('start_col')
    col_end = positions.get('end_col')
    if str(row_end) == "max":
        row_end = max_row

    for col in range(int(col_st), int(col_end)):
        for row in range(int(row_st), int(row_end)):
            # print str(sheet.cell(row, col).value)
            try:
                if re.search(r'\d+e-\d+', str(sheet.cell(row, col).value)):
                    Values1.append(format(sheet.cell(row, col).value, '.8f'))
                elif re.search(r'[a-zA-z]+', str(sheet.cell(row, col).value)):
                    Values1.append('')
                else:
                    Values1.append(str(sheet.cell(row, col).value))
            except:
                Values1.append('')
        Values_list.append(Values1)
        Values1 = []
    return Values_list


def Get_Excel_applies_to_datetime(book, sheet, applies_date, applies_date_positions, date_format_check, date_format,
                                  max_row):
    '''
        Function : To get the elements from excel
        Summary:
            1. Argument "book" - Contains Excel Book object
            1. Argument "sheet" - Contains Excel sheet object
            2. Argument "applies_date" - Contains Regex to get date & time
            3. Argument "applies_date_positions" - Contains date & Time cell position (i.e. start row, End row, Start col, End col)
            4. Argument "date_format_check" - Flag for date, whether the date in number format or actual date format
            5. Apply the mentioned position & regex to get date & time and append in list.
    '''
    Date_List = []
    Date_List1 = []
    if (applies_date_positions != 'n/a' or applies_date != 'n/a'):
        positions = ast.literal_eval(applies_date_positions)
        row_st, row_end, col_st, col_end = '', '', '', ''
        row_st = positions.get('start_row')
        row_end = positions.get('end_row')
        col_st = positions.get('start_col')
        col_end = positions.get('end_col')
        if str(row_end) == "max":
            row_end = max_row
        for col in range(int(col_st), int(col_end)):
            for row in range(int(row_st), int(row_end)):
                try:
                    Date = sheet.cell(row, col).value
                except:
                    Date=''
                try:
                    if (date_format_check == 'Y'):
                        Date1 = datetime(*xlrd.xldate_as_tuple(Date, book.datemode))
                        d1 = datetime.strptime(str(Date1), '%Y-%m-%d %H:%M:%S')
                        Date = str(d1.strftime('%Y-%m-%d'))
                    if (applies_date != 'n/a'):
                        Date1 = re.findall(str(applies_date).replace('{', '').replace('}', '').replace('REGEX', ''),
                                           str(Date), re.IGNORECASE)
                        if (Date1):
                            Date = Date1[0]
                        else:
                            Date = 'n/a'

                    if (date_format != 'n/a'):
                        d = datetime.strptime(str(Date), date_format)
                        Date = str(d.strftime('%Y-%m-%d'))
                except Exception as e:
                    Date = 'n/a'
                Date_List1.append(str(Date))
            Date_List.append(Date_List1)
            Date_List1 = []

    else:
        Date_List1.append('n/a')
        Date_List.append(Date_List1)
    return Date_List


def Get_Excel_applies_to_time(book, sheet, applies_date, applies_date_positions, date_format_check, date_format,
                              max_row):
    '''
        Function : To get the elements from excel
        Summary:
            1. Argument "book" - Contains Excel Book object
            1. Argument "sheet" - Contains Excel sheet object
            2. Argument "applies_date" - Contains Regex to get date & time
            3. Argument "applies_date_positions" - Contains date & Time cell position (i.e. start row, End row, Start col, End col)
            4. Argument "date_format_check" - Flag for date, whether the date in number format or actual date format
            5. Apply the mentioned position & regex to get date & time and append in list.
    '''
    Date_List = []
    Date_List1 = []
    if (applies_date_positions != 'n/a' or applies_date != 'n/a'):
        positions = ast.literal_eval(applies_date_positions)
        row_st, row_end, col_st, col_end = '', '', '', ''
        row_st = positions.get('start_row')
        row_end = positions.get('end_row')
        col_st = positions.get('start_col')
        col_end = positions.get('end_col')
        if str(row_end) == "max":
            row_end = max_row
        # print int(row_end) - int (row_st)
        for col in range(int(col_st), int(col_end)):
            for row in range(int(row_st), int(row_end)):
                try:
                    Date = sheet.cell(row, col).value
                except:
                    Date=''
                try:
                    if (applies_date != 'n/a'):
                        if 'REGEXFORMAT' in str(applies_date):
                            Date1 = datetime(*xlrd.xldate_as_tuple(Date, book.datemode))
                            d1 = datetime.strptime(str(Date1), '%Y-%m-%d %H:%M:%S')
                            #print d1
                            Date = str(d1.strftime('%H:%M:%S'))
                            #print Date
                        elif (applies_date != 'n/a'):
                            Date1 =re.findall(str(applies_date).replace('{', '').replace('}', '').replace('REGEX', ''), str(Date), re.IGNORECASE)
                            # print "List",Date1
                            if(Date1):
                                Date=Date1[0]
                            else:
                                Date='n/a'
                except:
                    Date = 'n/a'
                # print "Datettttt",Date
                Date_List1.append(str(Date))
            Date_List.append(Date_List1)
            Date_List1 = []

    else:
        Date_List1.append('n/a')
        Date_List.append(Date_List1)
    return Date_List


def datetime_format(date, time, applies_date, applies_time, hour_filter):
    temp_time = ''

    if re.search(r'[\d]+', str(time)):
        time = time
    else:
        time = 0

    if str(applies_date) != 'n/a':
        try:
            if str(time).strip() != 'n/a':
                if len(str(time)) > 5:
                    temp_time = str(date) + ' ' + str(time)
                elif len(str(time)) > 3:
                    temp_time = str(date) + ' ' + str(time) + ':00'
                elif len(str(time)) < 3 and len(str(time)) > 0:
                    if str(hour_filter) != 'n/a':
                        n = int(time)
                        temp_time_value = eval(hour_filter)
                        d1 = datetime.strptime(str(date), '%Y-%m-%d') + timedelta(minutes=int(temp_time_value))
                        temp_time = d1.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        d1 = datetime.strptime(str(date), '%Y-%m-%d') + timedelta(hours=int(time))
                        temp_time = d1.strftime('%Y-%m-%d %H:%M:%S')
            else:
                d1 = datetime.strptime(str(date), '%Y-%m-%d') + timedelta(hours=0)
                temp_time = d1.strftime('%Y-%m-%d %H:%M:%S')
        except:
            d1 = datetime.strptime(str(date), '%Y-%m-%d') + timedelta(hours=0)
            temp_time = d1.strftime('%Y-%m-%d %H:%M:%S')

    else:
        now = datetime.now()
        temp_time = now.strftime("%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(str(temp_time), '%Y-%m-%d %H:%M:%S')
    temp_time_format = d2.strftime('%Y-%m-%dT%H:%M:%S.0000000')
    return temp_time_format


def date_custom_function(datasourceid, sheet, DATE_POSITION_CUSTOM, DATE_CUSTOM, row_count):
    try:
        datePositionCustom = ast.literal_eval(DATE_POSITION_CUSTOM)
        dateCustom = ast.literal_eval(DATE_CUSTOM)
        dayRegex, monthRegex, yearRegex = '', '', ''
        if str(dateCustom) != 'n/a':
            dayRegex = dateCustom.get('day')
            monthRegex = dateCustom.get('month')
            yearRegex = dateCustom.get('year')
        else:
            dayRegex, monthRegex, yearRegex = 'n/a', 'n/a', 'n/a'
        dayPosition = datePositionCustom.get('day')
        day_row_start, day_row_end, day_col_start, day_col_end,rowCheckDay = '', '', '', '',''
        if str(dayPosition) != 'n/a':
            day_positions = ast.literal_eval(str(dayPosition))
            day_row_start = day_positions.get('start_row')
            day_row_end = day_positions.get('end_row')
            day_col_start = day_positions.get('start_col')
            day_col_end = day_positions.get('end_col')
            if (str(day_row_end) != 'max' and str(day_col_end) != 'max'):
                row_diff = int(day_row_end) - int(day_row_start)
                col_diff = int(day_col_end) - int(day_col_start)
                if row_diff == 1 and col_diff >1:
                    rowCheckDay='yes'
                else:
                    rowCheckDay='no'
            else:
                    rowCheckDay='no'

        if str(day_row_end) == 'max':
            day_row_end = row_count

        monthPosition = datePositionCustom.get('month')
        month_row_start, month_row_end, month_col_start, month_col_end,rowCheckMonth = '', '', '', '',''
        if str(monthPosition) != 'n/a':
            month_positions = ast.literal_eval(str(monthPosition))
            month_row_start = month_positions.get('start_row')
            month_row_end = month_positions.get('end_row')
            month_col_start = month_positions.get('start_col')
            month_col_end = month_positions.get('end_col')
            if (str(month_row_end) != 'max' and str(month_col_end) != 'max'):
                row_diff = int(month_row_end) - int(month_row_start)
                col_diff = int(month_col_end) - int(month_col_start)
                if row_diff == 1 and col_diff >1:
                    rowCheckMonth='yes'
                else:
                    rowCheckMonth='no'
            else:
                    rowCheckMonth='no'
        rowCheck=''
        if str(rowCheckDay) == 'yes' and str(rowCheckMonth) == 'yes':
            rowCheck='yes'
        else:
            rowCheck='no'
        
        if str(month_row_end) == 'max':
            month_row_end = row_count
        month_col_check = int(month_col_end) - int(month_col_start)
        month_row_check = int(month_row_end) - int(month_row_start)
        yearPosition = datePositionCustom.get('year')
        
        year_row_start,year_row_end,year_col_start,year_col_end,year_col_check,year_row_check,='','','','','',''
        if str(yearPosition) != 'n/a':
            year_positions = ast.literal_eval(str(yearPosition))
            year_row_start = year_positions.get('start_row')
            year_row_end = year_positions.get('end_row')
            year_col_start = year_positions.get('start_col')
            year_col_end = year_positions.get('end_col')

            if str(year_row_end) == 'max':
                year_row_end = row_count

            year_col_check = int(year_col_end) - int(year_col_start)
    
            year_row_check = int(year_row_end) - int(year_row_start)

        dayList = []
        monthList = []
        yearList = []
        dateList = []
        if str(dayPosition) != 'n/a':
            for col in range(int(day_col_start), int(day_col_end)):
                for row in range(int(day_row_start), int(day_row_end)):
                    day_value = sheet.cell(row, col).value
                    if str(dayRegex) != 'n/a':
                        day_temp = re.findall(str(dayRegex).replace('{', '').replace('}', '').replace('REGEX', ''),str(day_value), re.IGNORECASE)
                        day_value_1=''
                        try:
                            day_value_1 = day_temp[0]
                        except:
                            day_value_1='n/a'
                        dayList.append(int(day_value_1))
                    elif re.search(r'[A-Za-z]+', str(day_value)):
                        dayList.append('')
                    elif str(day_value).strip() == "":
                        dayList.append('')
                    else:
                        dayList.append(int(day_value))

        if str(monthPosition) != 'n/a':
            for col1 in range(int(month_col_start), int(month_col_end)):
                for row1 in range(int(month_row_start), int(month_row_end)):
                    month_value = sheet.cell(row1, col1).value
                    
                    if str(monthRegex) != 'n/a':
                        month_temp = re.findall(str(monthRegex).replace('{', '').replace('}', '').replace('REGEX', ''),str(month_value), re.IGNORECASE)
                        month=''
                        try:
                            month = month_temp[0]
                        except:
                            month='n/a'
#                         print "Month", month
                        if re.search(r'[A-Za-z]+', str(month)):
                            month_dict = {'JAN': '01', 'JAN.': '01', 'JANUARY': '01', 'Jan': '01', 'Jan.': '01',
                                          'January': '01', 'FEB': '02', 'FEB.': '02', 'FEBRUARY': '02', 'Feb': '02',
                                          'Feb.': '02', 'February': '02', 'MAR': '03', 'MAR.': '03', 'MARCH': '03',
                                          'Mar': '03', 'Mar.': '03', 'March': '03', 'APR': '04', 'APR.': '04',
                                          'APRIL': '04', 'Apr': '04', 'Apr.': '04', 'April': '04', 'MAY': '05',
                                          'May': '05', 'JUN': '06', 'JUN.': '06', 'JUNE': '06', 'Jun': '06',
                                          'Jun.': '06', 'June': '06', 'JUL': '07', 'JUL.': '07', 'JULY': '07',
                                          'Jul': '07', 'Jul.': '07', 'July': '07', 'AUG': '08', 'AUG.': '08',
                                          'AUGUST': '08', 'Aug': '08', 'Aug.': '08', 'August': '08', 'SEP': '09',
                                          'Sep': '09', 'SEP.': '09', 'Sep.': '09', 'SEPT': '09', 'Sept': '09',
                                          'SEPT.': '09', 'Sept.': '09', 'SEPTEMBER': '09', 'September': '09',
                                          'OCT': '10', 'Oct': '10', 'OCT.': '10', 'Oct.': '10', 'OCTOBER': '10',
                                          'October': '10', 'NOV': '11', 'Nov': '11', 'NOV.': '11', 'Nov.': '11',
                                          'NOVEMBER': '11', 'November': '11', 'DEC': '12', 'DEC.': '12',
                                          'DECEMBER': '12', 'Dec': '12', 'Dec.': '12', 'December': '12', 'jan': '01',
                                          'jan.': '01', 'january': '01', 'jan': '01', 'jan.': '01', 'january': '01',
                                          'feb': '02', 'feb.': '02', 'february': '02', 'feb': '02', 'feb.': '02',
                                          'february': '02', 'mar': '03', 'mar.': '03', 'march': '03', 'mar': '03',
                                          'mar.': '03', 'march': '03', 'apr': '04', 'apr.': '04', 'april': '04',
                                          'apr': '04', 'apr.': '04', 'april': '04', 'may': '05', 'may': '05',
                                          'jun': '06', 'jun.': '06', 'june': '06', 'jun': '06', 'jun.': '06',
                                          'june': '06', 'jul': '07', 'jul.': '07', 'july': '07', 'jul': '07',
                                          'jul.': '07', 'july': '07', 'aug': '08', 'aug.': '08', 'august': '08',
                                          'aug': '08', 'aug.': '08', 'august': '08', 'sep': '09', 'sep': '09',
                                          'sep.': '09', 'sep.': '09', 'sept': '09', 'sept': '09', 'sept.': '09',
                                          'sept.': '09', 'september': '09', 'september': '09', 'oct': '10', 'oct': '10',
                                          'oct.': '10', 'oct.': '10', 'october': '10', 'october': '10', 'nov': '11',
                                          'nov': '11', 'nov.': '11', 'nov.': '11', 'november': '11', 'november': '11',
                                          'dec': '12', 'dec.': '12', 'december': '12', 'dec': '12', 'dec.': '12',
                                          'december': '12', 'Gennaio': '1', 'Febbraio': '2', 'Marzo': '3',
                                          'Aprile': '4', 'Maggio': '5', 'Giugno': '6', 'Luglio': '7', 'Agosto': '8',
                                          'Settembre': '9', 'ottobre': '10', 'novembre': '11', 'dicembre': '12',
                                          'gennaio': '1', 'febbraio': '2', 'marzo': '3', 'aprile': '4', 'maggio': '5',
                                          'giugno': '6', 'luglio': '7', 'agosto': '8', 'settembre': '9',
                                          'ottobre': '10', 'novembre': '11', 'dicembre': '12', 'leden': '01',
                                          'Ãºnor': '02','únor':'02', 'brezen': '03','březen' : '03' ,'duben': '04', 'kveten': '05','květen':'05','červen':'06', 'cerven': '06',
                                          'cervenec': '07','červenec':'07' ,'srpen': '08', 'zÃ¡rÃ­': '09', 'září' : '09','rÃ­jen': '10', 'říjen': '10',
                                          'listopad': '11', 'prosinec': '12', 'Januar': '01', 'Februar': '02',
                                          'MÃ¤rz': '03','März':'03',
                                          'April': '04', 'Mai': '05', 'Juni': '06', 'Juli': '07', 'August': '08',
                                          'September': '09',
                                          'Oktober': '10', 'November': '11', 'Dezember': '12','enero' : '01','febrero' : '02','marzo' : '03','abril' : '04','mayo' : '05','junio' : '06','julio' : '07','agosto' : '08','septiembre' : '09','octubre' : '10','noviembre' : '11','diciembre' : '12'}
                            for key in month_dict:
                                if str(month) == str(key):
                                    month = month_dict[key]
                                    # month = month_dict[key]
                        monthList.append(month)
        else:
            curMonth = now.month
            monthList.append(curMonth)
        if str(yearPosition) != 'n/a':
            for col2 in range(int(year_col_start), int(year_col_end)):
                for row2 in range(int(year_row_start), int(year_row_end)):
                    year_value = sheet.cell(row2, col2).value
    #                 print year_value
                    if str(yearRegex) != 'n/a':
                        year_temp = re.findall(str(yearRegex).replace('{', '').replace('}', '').replace('REGEX', ''),str(year_value), re.IGNORECASE)
                        try:
                            yearList.append(year_temp[0])
                        except:
                            yearList.append('')
        dateListtemp = []
        if len(dayList) == 0:
            dayList.append('01')
        if len(monthList) == 0:
            monthList.append(str(now.month))
        if len(yearList) == 0:
            yearList.append(str(now.year))
#         print yearList[0]
#         print monthList
#         print dayList
#         print yearList
#         print len(monthList)
#         print len(yearList)
#         raw_input()
        
#         print year_row_check
        if len(monthList) > 1 and len(dayList) == 1 and len(yearList) == 1:
            # print "Condition"
            for i, monthValue in enumerate(monthList):
                if str(monthValue) != '':
                    try:
                        d = datetime.strptime(str(yearList[0]) + '-' + str(monthValue) + '-' + str(dayList[0]),
                                              '%Y-%m-%d')
                        Date = str(d.strftime('%Y-%m-%d'))
                        dateListtemp.append(Date)
                    except Exception as e:
#                         print e
                        dateListtemp.append('')
                else:
                    dateListtemp.append('')
            dateList.append(dateListtemp)
        elif len(monthList) > 1 and len(dayList) == 1 and len(yearList) > 1 and (month_row_check > year_row_check) :
#             print "elif len(monthList) > 1 and len(dayList) == 1 and len(yearList) > 1 and (month_row_check > year_row_check) :"
            # for i, monthValue in enumerate(monthList):
            for i, yearValue in enumerate(yearList):
                for i, monthValue in enumerate(monthList):
                    
                    if str(monthValue) != '':
                        try:
                            d = datetime.strptime(str(yearValue) + '-' + str(monthValue) + '-' + str(dayList[0]),
                                                  '%Y-%m-%d')
                            Date = str(d.strftime('%Y-%m-%d'))
                            dateListtemp.append(Date)
                        except Exception as e:
#                             print e
                            dateListtemp.append('')
                    else:
                        dateListtemp.append('')
                dateList.append(dateListtemp)
                dateListtemp = []
        elif len(monthList) > 1 and len(dayList) == 1 and len(yearList) > 1 and (month_row_check < year_row_check) :
#             print "daylist",dayList
            
            for i, monthValue in enumerate(monthList):
                for i, yearValue in enumerate(yearList):
                    if str(monthValue) != '':
                        try:
                            d = datetime.strptime(str(yearValue) + '-' + str(monthValue) + '-' + str(dayList[0]),
                                                  '%Y-%m-%d')
                            Date = str(d.strftime('%Y-%m-%d'))
                            dateListtemp.append(Date)
                        except Exception as e:
#                             print e
                            dateListtemp.append('')
                    else:
                        dateListtemp.append('')
#                 print dateListtemp
#                 raw_input()
                dateList.append(dateListtemp)
                dateListtemp=[]
            #print len(dateList)
#             raw_input()
        elif len(monthList) > 1 and len(dayList) == 1:
            #print "elif len(monthList) > 1 and len(dayList) == 1:"
            for i, monthValue in enumerate(monthList):
                if str(monthValue) != '':
                    try:
                        d = datetime.strptime(str(yearList[i]) + '-' + str(monthValue) + '-' + str(dayList[0]),
                                              '%Y-%m-%d')
                        Date = str(d.strftime('%Y-%m-%d'))
                        dateListtemp.append(Date)
                    except Exception as e:
#                         print e
                        dateListtemp.append('')
                else:
                    dateListtemp.append('')
            dateList.append(dateListtemp)
        elif len(monthList) > 1 and len(dayList) > 1 and len(yearList) == 1:
#             print "elif len(monthList) > 1 and len(dayList) > 1 and len(yearList) == 1:"
#             print monthList
#             print dayList
            for i, monthValue in enumerate(monthList):
                if str(monthValue) != '':
                    try:
                        d = datetime.strptime(str(yearList[0]) + '-' + str(monthValue) + '-' + str(dayList[i]),'%Y-%m-%d')
                        Date = str(d.strftime('%Y-%m-%d'))
                        dateListtemp.append(Date)
                    except Exception as e:
#                         print e
                        dateListtemp.append('')
                else:
                    dateListtemp.append('')
            dateList.append(dateListtemp)
        elif len(monthList) > 1 and len(dayList) > 1 and len(yearList) > 1:
            for i, monthValue in enumerate(monthList):
                if str(monthValue) != '':
                    try:
                        d = datetime.strptime(str(yearList[i]) + '-' + str(monthValue) + '-' + str(dayList[i]),
                                              '%Y-%m-%d')
                        Date = str(d.strftime('%Y-%m-%d'))
                        dateListtemp.append(Date)
                    except Exception as e:
#                         print e
                        dateListtemp.append('')
                else:
                    dateListtemp.append('')
            dateList.append(dateListtemp)
        else:
            for dateValue in dayList:
                if str(dateValue) != '':
                    try:
                        d = datetime.strptime(str(yearList[0]) + '-' + str(monthList[0]) + '-' + str(dateValue),
                                              '%Y-%m-%d')
                        Date = str(d.strftime('%Y-%m-%d'))
                        dateListtemp.append(Date)
                    except Exception as e:
#                         print e
                        dateListtemp.append('')
                else:
                    dateListtemp.append('')

            dateList.append(dateListtemp)
        if len(dateList) == 0:
            dateList.append('')
        
        rowDateValue=[]
        if str(rowCheck) == 'yes' and len(dateList) == 1 and len(dateList[0]) > 1:
            
            for datevalue in dateList[0]:
                rowDateValuetemp=[]
                rowDateValuetemp.append(datevalue)
                rowDateValue.append(rowDateValuetemp)
            return rowDateValue
        else:        
            return dateList
#         t =open("test_year.txt","w")
#         t.write(str(dateList))
#         t.close()
#         print dateList
        
        
    except Exception as e:
        print e, ' ', str(sys.exc_traceback.tb_lineno)
        error_log = e, ' ', str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
        sys.exit()




def html_table_format(ET, Config, document, data_source, datasourceid, raw_file, sectionName, session_bck, value_count,xml_dict, first_date, last_date, publicationformat_date,dateValidationList):
    '''
        Format : HTML table format
        Summary:
            1. Get sessions using "DatasourceName" for columns wise iteration in raw HTML file.
            2. Get the required fields for process HTML table data.
            3. Apply regex for getting date and hours and append in list.
            4. Apply regex for getting values and append in list.
            5. Iterate the value, date and hour list
            6. Set the sub element1 - time_serious and sub element2 - datum
            7. Set the values with the datum tag
            8. Empty  variable

    '''
    for i in range(0, 1):
        # print "session_bck",session_bck
        try:
            frequency_type = Config.get(session_bck, 'FREQUENCYTYPE')

            filename = str(raw_file)
            htmlholder_regex1 = Config.get(session_bck, 'HTMLHOLDER1')

            htmlholder_regex2 = Config.get(session_bck, 'HTMLHOLDER2')
            htmlholder_regex3 = Config.get(session_bck, 'HTMLHOLDER3')
            value_regex1 = Config.get(session_bck, 'VALUE')
            value_position = Config.get(session_bck, 'VALUE_POSITION')
            applies_to_date = Config.get(session_bck, 'APPLIES_TO_DATE')
            col_date_position = Config.get(session_bck, 'COL_DATE_POSITION')
            row_date_position = Config.get(session_bck, 'ROW_DATE_POSITION')
            month_position = Config.get(session_bck, 'MONTH_POSITION')
            date_position = Config.get(session_bck, 'DATE_POSITION')
            ignore_value = Config.get(session_bck, 'CONDITION_TO_IGNORE_VALUE')
            applies_to_time = Config.get(session_bck, 'APPLIES_TO_TIME')
            publication_to_date = Config.get(session_bck, 'PUBLICATION_DATE')
            publication_to_time = Config.get(session_bck, 'PUBLICATION_TIME')
            value_normalize = Config.get(session_bck, 'CONDITION_TO_VALUE_NORMALIZE')
            date_format = Config.get(session_bck, 'DATEFORMAT')
            element01 = Config.get(session_bck, 'ELEMENT01')
            element02 = Config.get(session_bck, 'ELEMENT02')
            element03 = Config.get(session_bck, 'ELEMENT03')
            element04 = Config.get(session_bck, 'ELEMENT04')
            element05 = Config.get(session_bck, 'ELEMENT05')
            element06 = Config.get(session_bck, 'ELEMENT06')
            element07 = Config.get(session_bck, 'ELEMENT07')
            element08 = Config.get(session_bck, 'ELEMENT08')
            element09 = Config.get(session_bck, 'ELEMENT09')
            quality = Config.get(session_bck, 'QUALITY')
            applies_to_hour_filter = Config.get(session_bck, 'APPLIES_HOUR_FILTER_TYPE')
            publication_to_hour_filter = Config.get(session_bck, 'PUBLICATION_HOUR_FILTER_TYPE')
            translation_condition = Config.get('default', 'T_TRANSLATION')
            translation_word = Config.get('default', 'T_TRANSLATEWORD')
        except Exception as e:
            error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
            print error_log
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
            sys.exit()
            break
            
        ''' Variable declaration'''
        # publication_to_date, publication_to_time
        text, temp_time, temp_time1, Row_Content_time, Row_Content_publication_time = '', '', '', '', ''
        f1_Col_Temp_list = []
        datelist = []
        publication_datelist = []
        elem1, elem2, elem3, elem4, elem5, elem6, elem7, elem8, elem9 = '', '', '', '', '', '', '', '', ''

        ''' Read the raw file content and stored it in variable '''
        try:
            with codecs.open(filename, 'r') as f:
                text = f.read()
        except Exception as e:
            error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
            print error_log
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
            sys.exit()
            break

        ''' Apply regex for getting date from raw content '''
        try:

            ''' Apply level 1 regex and value regex to get values and append in list '''
            html_holder1_value = ''
            if str(htmlholder_regex1) != 'n/a':

                html_holder1_value = re.findall(
                    str(htmlholder_regex1).replace('{', '').replace('}', '').replace('REGEX', ''), str(text),
                    re.IGNORECASE)
                # print len(html_holder1_value)
                with open("html_holder1_value.html","wb") as f:
                    f.write(str(html_holder1_value))				
                
                if len(html_holder1_value) > 0:
                    if str(htmlholder_regex2) != 'n/a':
                        for temp_regex2_value in html_holder1_value:
                            html_holder2_value = re.findall(str(htmlholder_regex2).replace('{', '').replace('}', '').replace('REGEX', ''),str(temp_regex2_value), re.IGNORECASE)
#                             print "Len HTML2",len(html_holder2_value)
                            if str(htmlholder_regex3) != 'n/a':
                                for temp_regex3_value in html_holder2_value:
                                    html_holder3_value = re.findall(str(htmlholder_regex3).replace('{', '').replace('}', '').replace('REGEX', ''),str(temp_regex3_value), re.IGNORECASE)

                                    for Row_val in html_holder3_value:
                                        f1_Col_Temp_list.append(re.findall(str(value_regex1).replace('{', '').replace('}', '').replace('REGEX', ''),Row_val, re.IGNORECASE))
                            else:
                                for Row_val in html_holder2_value:
#                                     if 'berackern' in session_bck:
#                                         print "ROW",Row_val
#                                         print "REGEX",str(value_regex1).replace('{', '').replace('}', '').replace('REGEX', '')
#                                         raw_input("df")
                                    f1_Col_Temp_list.append(re.findall(str(value_regex1).replace('{', '').replace('}', '').replace('REGEX', ''),Row_val, re.IGNORECASE))
                    else:
                        for Row_val in html_holder1_value:
                            f1_Col_Temp_list.append(re.findall(str(value_regex1).replace('{', '').replace('}', '').replace('REGEX', ''),Row_val, re.IGNORECASE))
                # print len(f1_Col_Temp_list)
                # tt = open("value_content_list.txt","w")
                # tt.write(str(f1_Col_Temp_list))
                # tt.close()
                # raw_input("len value")
            if len(html_holder1_value) > 0:

                if str(applies_to_date) != 'n/a':

                    Row_Content_date = re.findall(
                        str(applies_to_date).replace('{', '').replace('}', '').replace('REGEX', ''),
                        str(html_holder1_value), re.IGNORECASE)
                    ''' Conditions to be checked for identify the date formats (examples: 2016-07-15, 07/15)'''

                    if str(date_format) == 'n/a' and str(col_date_position) != 'n/a' and str(
                            row_date_position) == 'n/a':

                        datelist.append(date_formation(Row_Content_date[int(col_date_position)][int(month_position)],Row_Content_date[int(col_date_position)][int(date_position)]))

                    elif str(date_format) != 'n/a' and str(col_date_position) != 'n/a':

                        d = datetime.strptime(str(Row_Content_date[int(col_date_position)]), date_format)
                        temp_formatted_date = d.strftime('%Y-%m-%d')

                        if '1900' in str(temp_formatted_date):
                            temp_formatted_date = temp_formatted_date.replace('1900', '2016')
                        datelist.append(temp_formatted_date)

                    elif str(date_format) != 'n/a':

                        for date_val in Row_Content_date:

                            '''Get the actual date format from raw file and convert it into standard format (i.e., 20160715,15/07/2016,07-2016-23, ...  to 2016-07-15)'''

                            d = datetime.strptime(str(date_val), date_format)
                            temp_formatted_date = d.strftime('%Y-%m-%d')

                            if '1900' in str(temp_formatted_date):
                                temp_formatted_date = temp_formatted_date.replace('1900', '2016')

                            datelist.append(temp_formatted_date)
                else:
                    datelist.append(str(now.strftime("%Y-%m-%d")))
                ''' Publication date '''

                if str(publication_to_date) != 'n/a':

                    Row_Content_public_date = re.findall(
                        str(publication_to_date).replace('{', '').replace('}', '').replace('REGEX', ''),
                        str(html_holder1_value), re.IGNORECASE)

                    if str(date_format) == 'n/a' and str(col_date_position) != 'n/a' and str(
                            row_date_position) == 'n/a':

                        publication_datelist.append(
                            date_formation(Row_Content_public_date[int(col_date_position)][int(month_position)],
                                           Row_Content_public_date[int(col_date_position)][int(date_position)]))
										   
                    elif str(date_format) != 'n/a' and str(col_date_position) != 'n/a':

                        d = datetime.strptime(str(Row_Content_date[int(col_date_position)]), date_format)
                        temp_formatted_date = d.strftime('%Y-%m-%d')
						

                        if '1900' in str(temp_formatted_date):
                            temp_formatted_date = temp_formatted_date.replace('1900', '2016')
                        publication_datelist.append(temp_formatted_date)										   
					

                    elif str(date_format) != 'n/a':

                        for date_val1 in Row_Content_public_date:
                            '''Get the actual date format from raw file and convert it into standard format (i.e., 20160715,15/07/2016,07-2016-23, ...  to 2016-07-15)'''

                            d = datetime.strptime(str(date_val1), date_format)
                            temp_formatted_date = d.strftime('%Y-%m-%d')

                            publication_datelist.append(temp_formatted_date)

                ''' If hours is available in raw file, we apply regex to get it and append in list '''

                if str(applies_to_time) != 'n/a':
                    Row_Content_time = re.findall(
                        str(applies_to_time).replace('{', '').replace('}', '').replace('REGEX', ''),
                        str(html_holder1_value), re.IGNORECASE)
                if str(publication_to_time) != 'n/a':
                    Row_Content_publication_time = re.findall(
                        str(publication_to_time).replace('{', '').replace('}', '').replace('REGEX', ''),
                        str(html_holder1_value), re.IGNORECASE)

            f1_Col_Temp_list = remove_empty(f1_Col_Temp_list)

            ''' Split or Apply regex to get the element and append in list'''
            elem1 = element_splitup(element01, html_holder1_value)
            elem2 = element_splitup(element02, html_holder1_value)
            elem3 = element_splitup(element03, html_holder1_value)
            elem4 = element_splitup(element04, html_holder1_value)
            elem5 = element_splitup(element05, html_holder1_value)
            elem6 = element_splitup(element06, html_holder1_value)
            elem7 = element_splitup(element07, html_holder1_value)
            elem8 = element_splitup(element08, html_holder1_value)
            elem9 = element_splitup(element09, html_holder1_value)
            ''' Cooked file generation '''
            publication_datelist_inc, datelist_inc, element1_inc, element2_inc, element3_inc, element4_inc, element5_inc, element6_inc, element7_inc, element8_inc, element9_inc, hour_inc, publication_hour_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            # print len(f1_Col_Temp_list)
            # raw_input()
            for i, x in enumerate(f1_Col_Temp_list):

                '''
                Condition for validate the values i.e., the values should not be blank or any special character like '-',etc,.
                '''
                if (re.match(ignore_value, str(f1_Col_Temp_list[i][int(value_position)])) is None) and (
                    str(f1_Col_Temp_list[i][int(value_position)]).strip() != ""):
                    try:
                        str(re.sub(r'\\n\s+\s*', '', str(elem1[element1_inc]).strip()))
                        element = ''
                        if str(element01) != 'n/a':
                            element = str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem1[element1_inc]).strip())).strip(), translation_condition,translation_word))

                        if str(element02) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem2[element2_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element03) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem3[element3_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element04) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem4[element4_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element05) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem5[element5_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element06) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem6[element6_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element07) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem7[element7_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'
                        if str(element08) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem8[element8_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        if str(element09) != 'n/a':
                            element = str(element) + '|' + str(translate(str(re.sub(r'\\n\s+\s*', '', str(elem9[element9_inc]).strip())).strip(), translation_condition,translation_word))
                        else:
                            element = str(element) + '|' + 'n/a'

                        xml_key = 'time_series' + '|' + str(last_date) + '|' + str(first_date) + '|' + str(
                            frequency_type) + '|' + 'xref|' + element + '|' + str(data_source)

                        ''' create datum sub node in time_serious node and set values, applies_to_datetime, publication_datetime '''

                        value_count = value_count + 1
                        value_format = ''
                        if str(value_normalize) == 'yes':
                            value_format = clean_fn(str(value_replace(f1_Col_Temp_list[i][int(value_position)])).replace(' ',''))
                        elif str(value_normalize) == 'yes1':
                            value_format = clean_fn(str(value_replace_spl(f1_Col_Temp_list[i][int(value_position)])).replace(' ',''))
                        else:
                            value_format = clean_fn(str(f1_Col_Temp_list[i][int(value_position)]).replace(' ', ''))

                        applies_temp_time, publication_temp_time = '', ''

                        if str(applies_to_time) != 'n/a':
                            applies_temp_time = datetime_format(datelist[datelist_inc], Row_Content_time[hour_inc],applies_to_date, applies_to_time,applies_to_hour_filter)
                        else:
                            applies_temp_time = datetime_format(datelist[datelist_inc], '00', applies_to_date,applies_to_time, applies_to_hour_filter)

                        if str(publication_to_date) != 'n/a':
                            if str(publication_to_time) != 'n/a':
                                publication_temp_time = datetime_format(publication_datelist[publication_datelist_inc],Row_Content_publication_time[publication_hour_inc], publication_to_date,publication_to_time, publication_to_hour_filter)
                            else:
                                publication_temp_time = datetime_format(publication_datelist[publication_datelist_inc],'00', publication_to_date, publication_to_time,publication_to_hour_filter)
                        elif str(publication_to_date) == 'n/a' and str(publication_to_hour_filter) != 'n/a':
                            n = 0
                            publication_temp_hour_value1 = eval(publication_to_hour_filter)
                            d1 = datetime.strptime(str(applies_temp_time), '%Y-%m-%dT%H:%M:%S.0000000') + timedelta(minutes=int(publication_temp_hour_value1))
                            publication_temp_time = d1.strftime('%Y-%m-%dT00:00:00.0000000')
                            
                        else:
                            publication_temp_time = publicationformat_date
                        date_format1 = datetime.strptime(str(applies_temp_time), '%Y-%m-%dT%H:%M:%S.0000000')
                        dateValidationList.append(str(date_format1.strftime('%Y-%m-%d')))
                        xml_value = 'datum' + '|' + str(applies_temp_time) + '|' + str(publication_temp_time) + '|' + str(value_format) + '|' + str(quality)
                        xml_dict.setdefault(xml_key, []).append(xml_value)
                        xml_value = ''
                        xml_key = ''

                    except Exception as e:
                        error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                        print error_log
                        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                        sys.exit()
                        break
                ''' Increment the variables if it has greater then 1 '''
                if len(Row_Content_time) != 1:
                    hour_inc = hour_inc + 1
                if len(Row_Content_publication_time) != 1:
                    publication_hour_inc = publication_hour_inc + 1
                if len(datelist) != 1:
                    datelist_inc = datelist_inc + 1
                if len(publication_datelist) != 1:
                    publication_datelist_inc = publication_datelist_inc + 1
                if (len(elem1) != 1) and (elem1 != ""):
                    element1_inc = element1_inc + 1
                if (len(elem2) != 1) and (elem2 != ""):
                    element2_inc = element2_inc + 1
                if (len(elem3) != 1) and (elem3 != ""):
                    element3_inc = element3_inc + 1
                if (len(elem4) != 1) and (elem4 != ""):
                    element4_inc = element4_inc + 1
                if (len(elem5) != 1) and (elem5 != ""):
                    element5_inc = element5_inc + 1
                if (len(elem6) != 1) and (elem6 != ""):
                    element6_inc = element6_inc + 1
                if (len(elem7) != 1) and (elem7 != ""):
                    element7_inc = element7_inc + 1
                if (len(elem8) != 1) and (elem8 != ""):
                    element8_inc = element8_inc + 1
                if (len(elem9) != 1) and (elem9 != ""):
                    element9_inc = element9_inc + 1
            ''' Empty the local varibales'''
            frequency_type, filename, htmlholder_regex1, value_regex1, value_position, applies_to_date, col_date_position, row_date_position, month_position, date_position, condition1, applies_to_time, date_format, element01, element02, element03, quality = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
        except Exception as e:
            error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
            print error_log
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
            sys.exit()
            break
    return xml_dict, value_count , dateValidationList


def csv_format(ET, Config, document, data_source, datasourceid, raw_file, sectionName, session_bck, value_count,
               xml_dict, first_date, last_date, publicationformat_date,dateValidationList):
    '''
        Format : CSV File format
        Summary:
            1. Read the required sections from the control file.
            2. Get all the values from the control file and stored it in local variables.
            3. Read the CSV file and store the content in the list.
            4. Extract the values, element and date by column and row wise iteration and store it in list.
            5. Looping the list and generate the cooked data
            6. Return the cooked data as a object to the main function.

    '''
    try:
        for i in range(0, 1):

            try:
                frequency_type = Config.get(session_bck, 'FREQUENCYTYPE')
                filename = str(raw_file)
                element01_positions = Config.get(session_bck, 'ELEMENT01_POSITIONS')
                element02_positions = Config.get(session_bck, 'ELEMENT02_POSITIONS')
                element03_positions = Config.get(session_bck, 'ELEMENT03_POSITIONS')
                element04_positions = Config.get(session_bck, 'ELEMENT04_POSITIONS')
                element05_positions = Config.get(session_bck, 'ELEMENT05_POSITIONS')
                element06_positions = Config.get(session_bck, 'ELEMENT06_POSITIONS')
                element07_positions = Config.get(session_bck, 'ELEMENT07_POSITIONS')
                element08_positions = Config.get(session_bck, 'ELEMENT08_POSITIONS')
                element09_positions = Config.get(session_bck, 'ELEMENT09_POSITIONS')
                applies_date_positions = Config.get(session_bck, 'APPLIES_DATE_POSITION')
                applies_hour_positions = Config.get(session_bck, 'APPLIES_HOUR_POSITION')
                ignore_value = Config.get(session_bck, 'CONDITION_TO_IGNORE_VALUE')
                value_normalize = Config.get(session_bck, 'CONDITION_TO_VALUE_NORMALIZE')
                publication_date_positions = Config.get(session_bck, 'PUBLICATION_DATE_POSITIONS')
                publication_hour_positions = Config.get(session_bck, 'PUBLICATION_HOUR_POSITIONS')
                date_format = Config.get(session_bck, 'DATEFORMAT')
                element01 = Config.get(session_bck, 'ELEMENT01')
                element02 = Config.get(session_bck, 'ELEMENT02')
                element03 = Config.get(session_bck, 'ELEMENT03')
                element04 = Config.get(session_bck, 'ELEMENT04')
                element05 = Config.get(session_bck, 'ELEMENT05')
                element06 = Config.get(session_bck, 'ELEMENT06')
                element07 = Config.get(session_bck, 'ELEMENT07')
                element08 = Config.get(session_bck, 'ELEMENT08')
                element09 = Config.get(session_bck, 'ELEMENT09')
                quality = Config.get(session_bck, 'QUALITY')
                
                applies_date = Config.get(session_bck, 'APPLIES_DATE')
                applies_hour = Config.get(session_bck, 'APPLIES_HOUR')
                publication_date = Config.get(session_bck, 'PUBLICATION_DATE')
                publication_hour = Config.get(session_bck, 'PUBLICATION_HOUR')
                value_positions = Config.get(session_bck, 'VALUE_POSITIONS')
                delimit = Config.get(session_bck, 'DELIMITER')
                applies_hour_filter_type = Config.get(session_bck, 'APPLIES_HOUR_FILTER_TYPE')
                publication_hour_filter_type = Config.get(session_bck, 'PUBLICATION_HOUR_FILTER_TYPE')
                date_filter = Config.get(session_bck, 'DATE_FILTER')
                filter_condition1 = Config.get(session_bck, 'FILTER_CONDITION1')
                filter_data = Config.get(session_bck, 'FILTER_DATA')
                translation_condition = Config.get('default', 'T_TRANSLATION')
                translation_word = Config.get('default', 'T_TRANSLATEWORD')
                try:
                    datetimeComparison = Config.get(session_bck, 'DATETIME_COMPARISON')
                except:
                    datetimeComparison = 'n/a'
                try:
                    quality_positions = Config.get(session_bck, 'QUALITY_POSITIONS')
                except:
                    quality_positions = 'n/a'
                
#                 print "date_format",publication_date,publication_hour publication_date_positions publication_hour_positions

            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                sys.exit()
                print error_log
                break
            '''
             Read the content from the csv file and push all the rows into the list

            '''
            sourcecontent = []
            try:
                f = open(filename, 'rt')

                reader = ''
                if str(delimit) != 'n/a':
                    reader = csv.reader(f, delimiter=(
                    delimit.replace('VAL', '').replace('{', '').replace('}', '')).strip())

                for data in reader:
                    sourcecontent.append(data)
            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                print error_log
                sys.exit()
                break

            '''
             Get maximum row and column numbers
            '''

            max_row = len(sourcecontent)
            max_col = max(len(l) for l in sourcecontent)

            '''
            Element, Date, Values were captured in different set of lists, finally column wise iteration done to joined list for transformation

            '''
            element01_val, element02_val, element03_val, element04_val, element06_val, element07_val, element08_val, element09_val, applies_date_value, applies_hour_value, publication_date_value, publication_hour_value, values, filter_data_values = '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            quality_val=''
            
            try:
                element01_val = csv_element_extraction(sourcecontent, element01_positions, element01, max_col, max_row)
                element02_val = csv_element_extraction(sourcecontent, element02_positions, element02, max_col, max_row)
                element03_val = csv_element_extraction(sourcecontent, element03_positions, element03, max_col, max_row)
                print "element03_val",len(element03_val)
                element04_val = csv_element_extraction(sourcecontent, element04_positions, element04, max_col, max_row)
                print "element04_val",len(element04_val)
                element05_val = csv_element_extraction(sourcecontent, element05_positions, element05, max_col, max_row)
                element06_val = csv_element_extraction(sourcecontent, element06_positions, element06, max_col, max_row)
                element07_val = csv_element_extraction(sourcecontent, element07_positions, element07, max_col, max_row)
                element08_val = csv_element_extraction(sourcecontent, element08_positions, element08, max_col, max_row)
                element09_val = csv_element_extraction(sourcecontent, element09_positions, element09, max_col, max_row)
                applies_date_value = csv_element_extraction(sourcecontent, applies_date_positions, applies_date,max_col, max_row)
                applies_hour_value = csv_element_extraction(sourcecontent, applies_hour_positions, applies_hour,max_col, max_row)
                publication_date_value = csv_element_extraction(sourcecontent, publication_date_positions,publication_date, max_col, max_row)
                publication_hour_value = csv_element_extraction(sourcecontent, publication_hour_positions,publication_hour, max_col, max_row)
                values = csv_element_extraction(sourcecontent, value_positions, 'n/a', max_col, max_row)
                print "values",len(values)
                if str(quality) != '' and str(quality_positions) != 'n/a' :
                    quality_val = csv_element_extraction(sourcecontent, quality_positions, quality, max_col, max_row)
                if str(filter_data) != 'n/a':
                    filter_data_values = csv_element_extraction(sourcecontent, filter_data, 'n/a', max_col, max_row)
            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                print error_log
                sys.exit()
                break

            '''
            Declared incremental variables for column and row iteration
            '''

            element01_col_inc, element02_col_inc, element03_col_inc, element04_col_inc, element05_col_inc, element06_col_inc, element07_col_inc, element08_col_inc, element09_col_inc, date_col_inc, hour_col_inc, publication_date_col_inc, publication_hour_col_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            element01_row_inc, element02_row_inc, element03_row_inc, element04_row_inc, element05_row_inc, element06_row_inc, element07_row_inc, element08_row_inc, element09_row_inc, date_row_inc, hour_row_inc, publication_date_row_inc, publication_hour_row_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            quality_row_inc,quality_col_inc = 0,0
            column_number, condition_value = '', ''
            if str(filter_condition1) != 'n/a':
                filter_condition = ast.literal_eval(filter_condition1)
                column_number = filter_condition.get('column_number')
                condition_value = filter_condition.get('condition_value')

            plus_date, minus_date = '', ''

            if str(date_filter) != 'n/a':
                filter_fields = ast.literal_eval(date_filter)

                plus_date = filter_fields.get('plus_date')
                minus_date = filter_fields.get('minus_date')

            ''' For loop for column wise iteration'''
            # if str(quality) != '' and str(quality_positions) != 'n/a' :
            for i, val_pos in enumerate(values):

                ''' For loop for row wise iteration'''
                for j, val in enumerate(val_pos):
                    e1, e2, e3, e4, e5, e6, e7, e8, e9, applies_date_hour, publication_date_hour, d, d1, d2, d3 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    if str(val).strip() != "":
                        try:

                            publication_formatted_hour = ''
                            applies_formatted_hour = ''
                            publication_date_hour = ''
                            applies_date_hour = ''
                            applies_date_temp = ''
                            date_plus, date_minus, applies_date_validation = '', '', ''

                            ''' Get the elements from the list'''
                            e1 = translate(element01_val[element01_col_inc][element01_row_inc], translation_condition,translation_word)
                            e2 = translate(element02_val[element02_col_inc][element02_row_inc], translation_condition,translation_word)
                            e3 = translate(element03_val[element03_col_inc][element03_row_inc], translation_condition,translation_word)
                            e4 = translate(element04_val[element04_col_inc][element04_row_inc], translation_condition,translation_word)
                            e5 = translate(element05_val[element05_col_inc][element05_row_inc], translation_condition,translation_word)
                            e6 = translate(element06_val[element06_col_inc][element06_row_inc], translation_condition,translation_word)
                            e7 = translate(element07_val[element07_col_inc][element07_row_inc], translation_condition,translation_word)
                            e8 = translate(element08_val[element08_col_inc][element08_row_inc], translation_condition,translation_word)
                            e9 = translate(element09_val[element09_col_inc][element09_row_inc], translation_condition,translation_word)

                            ''' Format the applies and publication date'''
                            # print "quality_val",len(quality_val[0])
                            applies_temp_hour_value,qualityValue = '',''
                            if str(quality) != '' and str(quality_positions) != 'n/a' :
                                qualityValue = quality_val[quality_col_inc][quality_row_inc]
                                print "qualityValue",qualityValue
                            else:
                                qualityValue = quality
                            if str(applies_hour_filter_type) != 'n/a':
                                n = int(applies_hour_value[hour_col_inc][hour_row_inc])
                                applies_temp_hour_value = eval(applies_hour_filter_type)

                            publication_temp_hour_value = ''
                            
                            if str(publication_hour_filter_type) != 'n/a' and str(publication_hour) != 'n/a':
                                n = int(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc])
                                publication_temp_hour_value = eval(publication_hour_filter_type)

                            if str(applies_date_value[date_col_inc][date_row_inc]) != None and str(applies_date_value[date_col_inc][date_row_inc]) != '':

                                applies_date_temp = str(applies_date_value[date_col_inc][date_row_inc])
#                                 print "DATE FORM",date_format
#                                 print  applies_date_temp
                                d = datetime.strptime(str(applies_date_temp), date_format)

                                if (str(applies_hour) != 'n/a' or str(applies_hour_positions) != 'n/a') and str(applies_hour_filter_type) != 'n/a':
                                    applies_formatted_hour = timedelta(minutes=int(applies_temp_hour_value))
                                elif (str(applies_hour) != 'n/a' or str(applies_hour_positions) != 'n/a') and len(applies_hour_value[hour_col_inc][hour_row_inc]) > 5:
                                    applies_formatted_hour = applies_hour_value[hour_col_inc][hour_row_inc]
                                elif (str(applies_hour) != 'n/a' or str(applies_hour_positions) != 'n/a') and len(applies_hour_value[hour_col_inc][hour_row_inc]) == 2:
                                    applies_formatted_hour = str(applies_hour_value[hour_col_inc][hour_row_inc]) + ':00:00'
                                elif (str(applies_hour) != 'n/a' or str(applies_hour_positions) != 'n/a') and len(applies_hour_value[hour_col_inc][hour_row_inc]) == 1:
                                    applies_formatted_hour = '0' + str(applies_hour_value[hour_col_inc][hour_row_inc]) + ':00:00'
                                elif (str(applies_hour) != 'n/a' or str(applies_hour_positions) != 'n/a') and len(applies_hour_value[hour_col_inc][hour_row_inc]) > 2:
                                    applies_formatted_hour = str(applies_hour_value[hour_col_inc][hour_row_inc]) + ':00'
                                else:
                                    applies_formatted_hour = '00:00:00'

                                applies_formatted_date = str(d.strftime('%Y-%m-%d')) + ' ' + str(applies_formatted_hour)
                                d1 = datetime.strptime(str(applies_formatted_date), '%Y-%m-%d %H:%M:%S')
                                applies_date_hour = d1.strftime('%Y-%m-%dT%H:%M:%S.0000000')
                            else:
                                applies_date_hour = now.strftime("%Y-%m-%dT%H:%M:%S.0000000")
                            publication_date_temp = ''

                            if str(publication_date_value[publication_date_col_inc][publication_date_row_inc]) !='n/a' and str(publication_date_value[publication_date_col_inc][publication_date_row_inc]) != None and str(publication_date_value[publication_date_col_inc][publication_date_row_inc]) != '':
                                d2 = ''

                                if str(publication_date) != 'n/a' and str(publication_date_value[publication_date_col_inc][publication_date_row_inc]) != '':
                                    publication_date_temp = str(publication_date_value[publication_date_col_inc][publication_date_row_inc])
                                    d2 = datetime.strptime(str(publication_date_temp), date_format)
                                else:
                                    publication_date_temp = strftime("%Y-%m-%d", gmtime())
                                    d2 = datetime.strptime(str(publication_date_temp), '%Y-%m-%d')

                                if (str(publication_hour) != 'n/a' or str(publication_hour_positions) != 'n/a') and str(publication_hour_filter_type) != 'n/a':
                                    publication_formatted_hour = timedelta(minutes=int(publication_temp_hour_value))
                                elif (str(publication_hour) != 'n/a' or str(publication_hour_positions) != 'n/a') and len(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) > 5:
                                    publication_formatted_hour = publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]
                                elif (str(publication_hour) != 'n/a' or str(publication_hour_positions) != 'n/a') and len(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) == 2:
                                    publication_formatted_hour = str(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) + ':00:00'
                                elif (str(publication_hour) != 'n/a' or str(publication_hour_positions) != 'n/a') and len(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) == 1:
                                    publication_formatted_hour = '0' + str(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) + ':00:00'
                                elif (str(publication_hour) != 'n/a' or str(publication_hour_positions) != 'n/a') and len(applies_hour_value[hour_col_inc][hour_row_inc]) > 2:
                                    publication_formatted_hour = str(publication_hour_value[publication_hour_col_inc][publication_hour_row_inc]) + ':00'
                                else:
                                    publication_formatted_hour = strftime("%H:%M:%S", gmtime())
                                publication_formatted_date = str(d2.strftime('%Y-%m-%d')) + ' ' + str(publication_formatted_hour)
                                d3 = datetime.strptime(str(publication_formatted_date), '%Y-%m-%d %H:%M:%S')
                                publication_date_hour = d3.strftime('%Y-%m-%dT%H:%M:%S.0000000')
                            elif str(publication_date_positions) == 'n/a' and str(publication_hour_positions) == 'n/a' and str(publication_hour_filter_type) != 'n/a':
                                n = 0
                                publication_temp_hour_value1 = eval(publication_hour_filter_type)
                                d1 = datetime.strptime(str(applies_date_hour), '%Y-%m-%dT%H:%M:%S.0000000') + timedelta(minutes=int(publication_temp_hour_value1))
                                publication_date_hour = d1.strftime('%Y-%m-%dT00:00:00.0000000')
                            else:
                                publication_date_hour = publicationformat_date
                            '''
                            Filter condition
                            '''
                            condition1 = ''
                            condition2 = ''

                            if (str(filter_condition1) != 'n/a'):
                                if (re.search(
                                        str(condition_value.replace('{', '').replace('}', '').replace('REGEX', '')),
                                        str(filter_data_values[column_number][j])) is not None):
                                    condition1 = 'True'
                                else:
                                    condition1 = 'False'
                            else:
                                condition1 = 'True'
                            '''
                            Validating Date condition and filter condition
                            '''
                            if str(date_filter) != 'n/a':
                                check_day_plus = date.today() + timedelta(int(plus_date))
                                day_plus = check_day_plus.strftime('%d')
                                month_plus = check_day_plus.strftime('%m')
                                check_day_minus = date.today() - timedelta(int(minus_date))
                                day_minus = check_day_minus.strftime('%d')
                                month_minus = check_day_minus.strftime('%m')
                                date_plus_a_day = datetime(now.year, int(month_plus), int(day_plus))
                                date_minus_a_day = datetime(now.year, int(month_minus), int(day_minus))
                                date_plus = str(check_day_plus.strftime('%Y-%m-%d'))
                                date_minus = str(check_day_minus.strftime('%Y-%m-%d'))
                                applies_date_validation = str(d.strftime('%Y-%m-%d'))
                                if date_plus >= applies_date_validation and date_minus <= applies_date_validation:
                                    condition2 = 'True'
                                else:
                                    condition2 = 'False'
                            else:
                                condition2 = 'True'

                            comparison_condition = ''

                            e1_condition, e2_condition, e3_condition, e4_condition, e5_condition, e6_condition, e7_condition, e8_condition, e9_condition = '', '', '', '', '', '', '', '', ''
                            if str(datetimeComparison) != 'n/a':
                                datetimeComparison_condition = ast.literal_eval(datetimeComparison)
                                comparisonConditon = datetimeComparison_condition.get('condition')
                                Element_condition = datetimeComparison_condition.get('Element')
                                Element_value_condition = datetimeComparison_condition.get('Element_value')
                                applies_temp = datetime.strptime(str(applies_date_hour), '%Y-%m-%dT%H:%M:%S.0000000')
                                applies_temp_check = applies_temp.strftime('%Y-%m-%dT%H:%M:%S.0000000')

                                publication_temp = datetime.strptime(str(publication_date_hour),
                                                                     '%Y-%m-%dT%H:%M:%S.0000000')
                                publication_temp_check = publication_temp.strftime('%Y-%m-%dT%H:%M:%S.0000000')

                                current_temp_check = now.strftime("%Y-%m-%dT%H:%M:%S.0000000")
                                comparison_condition, e1_condition, e2_condition, e3_condition, e4_condition, e5_condition, e6_condition, e7_condition, e8_condition, e9_condition = datecomparison(
                                    comparisonConditon, Element_condition, Element_value_condition, applies_temp_check,
                                    publication_temp_check, current_temp_check, e1_condition, e2_condition,
                                    e3_condition, e4_condition, e5_condition, e6_condition, e7_condition, e8_condition,
                                    e9_condition)

                            else:
                                comparison_condition = 'True'

                            if condition1 == 'True' and condition2 == 'True' and (
                                str(val).strip() != "") and comparison_condition == 'True':

                                if (re.match(ignore_value, str(val)) is None):

                                    ''' Set the elements in the time_series tag'''
                                    value_count = value_count + 1
                                    element = ''
                                    e1_condition, e2_condition, e3_condition, e4_condition, e5_condition, e6_condition, e7_condition, e8_condition, e9_condition
                                    if (str(element01) != 'n/a' or str(element01_positions) != 'n/a'):
                                        element = str(re.sub(r'\\n\s+\s*', '', str(e1).strip()))
                                        
                                    elif str(e1_condition) != "":
                                        element = str(e1_condition).strip()

                                    if (str(element02) != 'n/a' or str(element02_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e2).strip()))
                                    elif str(e2_condition) != "":
                                        element = str(element) + '|' + str(e2_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element03) != 'n/a' or str(element03_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e3).strip()))
                                    elif str(e3_condition) != "":
                                        element = str(element) + '|' + str(e3_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element04) != 'n/a' or str(element04_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e4).strip()))
                                    elif str(e4_condition) != "":
                                        element = str(element) + '|' + str(e4_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element05) != 'n/a' or str(element05_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e5).strip()))
                                    elif str(e5_condition) != "":
                                        element = str(element) + '|' + str(e5_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element06) != 'n/a' or str(element06_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e6).strip()))
                                    elif str(e6_condition) != "":
                                        element = str(element) + '|' + str(e6_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element07) != 'n/a' or str(element07_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e7).strip()))
                                    elif str(e7_condition) != "":
                                        element = str(element) + '|' + str(e7_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'
                                    if (str(element08) != 'n/a' or str(element08_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e8).strip()))
                                    elif str(e8_condition) != "":
                                        element = str(element) + '|' + str(e8_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'

                                    if (str(element09) != 'n/a' or str(element09_positions) != 'n/a'):
                                        element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(e9).strip()))
                                    elif str(e9_condition) != "":
                                        element = str(element) + '|' + str(e9_condition).strip()
                                    else:
                                        element = str(element) + '|' + 'n/a'
                                    
                                    date_format1 = datetime.strptime(str(applies_date_hour), '%Y-%m-%dT%H:%M:%S.0000000')
                                    dateValidationList.append(str(date_format1.strftime('%Y-%m-%d')))
                                    xml_key = 'time_series' + '|' + str(last_date) + '|' + str(first_date) + '|' + str(frequency_type) + '|' + 'xref|' + element + '|' + str(data_source)
                                    val_formattted = ''
                                    if str(value_normalize) == 'yes':
                                        val_formattted=clean_fn(str(value_replace(str(val).replace('..','0'))).replace(' ',''))
                                    elif str(value_normalize) == 'yes1':
                                        val_formattted=clean_fn(str(value_replace_spl(str(val).replace('..','0'))).replace(' ',''))
                                    else:
                                        val_formattted = clean_fn(str(val).replace('..', '0').replace(' ', ''))
                                    xml_value = 'datum' + '|' + str(applies_date_hour) + '|' + str(publication_date_hour) + '|' + str(val_formattted) + '|' + str(qualityValue)
                                    xml_dict.setdefault(xml_key, []).append(xml_value)
                                    xml_value = ''
                                    xml_key = ''
                        except Exception as e:
                            print e, str(sys.exc_traceback.tb_lineno)
                            break
                    ''' Increment the rows '''
                    element01_row_inc = value_increment(val_pos, element01_val[element01_col_inc], element01_row_inc)
                    element02_row_inc = value_increment(val_pos, element02_val[element02_col_inc], element02_row_inc)
                    element03_row_inc = value_increment(val_pos, element03_val[element03_col_inc], element03_row_inc)
                    element04_row_inc = value_increment(val_pos, element04_val[element04_col_inc], element04_row_inc)
                    element05_row_inc = value_increment(val_pos, element05_val[element05_col_inc], element05_row_inc)
                    element06_row_inc = value_increment(val_pos, element06_val[element06_col_inc], element06_row_inc)
                    element07_row_inc = value_increment(val_pos, element07_val[element07_col_inc], element07_row_inc)
                    element08_row_inc = value_increment(val_pos, element08_val[element08_col_inc], element08_row_inc)
                    element09_row_inc = value_increment(val_pos, element09_val[element09_col_inc], element09_row_inc)
                    date_row_inc = value_increment(val_pos, applies_date_value[date_col_inc], date_row_inc)
                    hour_row_inc = value_increment(val_pos, applies_hour_value[hour_col_inc], hour_row_inc)
                    publication_date_row_inc = value_increment(val_pos,publication_date_value[publication_date_col_inc],publication_date_row_inc)
                    publication_hour_row_inc = value_increment(val_pos,publication_hour_value[publication_hour_col_inc],publication_hour_row_inc)
                    if str(quality) != '' and str(quality_positions) != 'n/a' :
                        quality_row_inc = value_increment(val_pos, quality_val[quality_col_inc], quality_row_inc)
                ''' Increment the columns'''
                element01_col_inc = value_increment(values, element01_val, element01_col_inc)
                element02_col_inc = value_increment(values, element02_val, element02_col_inc)
                element03_col_inc = value_increment(values, element03_val, element03_col_inc)
                element04_col_inc = value_increment(values, element04_val, element04_col_inc)
                element05_col_inc = value_increment(values, element05_val, element05_col_inc)
                element06_col_inc = value_increment(values, element06_val, element06_col_inc)
                element07_col_inc = value_increment(values, element07_val, element07_col_inc)
                element08_col_inc = value_increment(values, element08_val, element08_col_inc)
                element09_col_inc = value_increment(values, element09_val, element09_col_inc)
                date_col_inc = value_increment(values, applies_date_value, date_col_inc)
                hour_col_inc = value_increment(values, applies_hour_value, hour_col_inc)
                publication_date_col_inc = value_increment(values, publication_date_value, publication_date_col_inc)
                publication_hour_col_inc = value_increment(values, publication_hour_value, publication_hour_col_inc)
                if str(quality) != '' and str(quality_positions) != 'n/a' :
                    quality_col_inc = value_increment(values, quality_val, quality_col_inc)
                
                ''' Empty the local variables '''
                element01_row_inc, element02_row_inc, element03_row_inc, element04_row_inc, element05_row_inc, element06_row_inc, element07_row_inc, element08_row_inc, element09_row_inc, date_row_inc, hour_row_inc, publication_date_row_inc, publication_hour_row_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        return xml_dict, value_count,dateValidationList
    except Exception as e:
        error_log = e, str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')


def excel_format(ET, Config, document, data_source, datasourceid, raw_file, sectionName, session_bck, value_count,
                 xml_dict, first_date, last_date, publicationformat_date,dateValidationList):
    try:
        for i in range(0, 1):
            # print session_bck
            try:
                frequency_type = Config.get(session_bck, 'FREQUENCYTYPE')
                filename = str(raw_file)
                sheet_name = Config.get(session_bck, 'SHEET_NAME')
                element01_positions = Config.get(session_bck, 'ELEMENT01_POSITIONS')
                element02_positions = Config.get(session_bck, 'ELEMENT02_POSITIONS')
                element03_positions = Config.get(session_bck, 'ELEMENT03_POSITIONS')
                element04_positions = Config.get(session_bck, 'ELEMENT04_POSITIONS')
                element05_positions = Config.get(session_bck, 'ELEMENT05_POSITIONS')
                element06_positions = Config.get(session_bck, 'ELEMENT06_POSITIONS')
                element07_positions = Config.get(session_bck, 'ELEMENT07_POSITIONS')
                element08_positions = Config.get(session_bck, 'ELEMENT08_POSITIONS')
                element09_positions = Config.get(session_bck, 'ELEMENT09_POSITIONS')
                applies_date_positions = Config.get(session_bck, 'APPLIES_DATE_POSITION')
                applies_hour_positions = Config.get(session_bck, 'APPLIES_HOUR_POSITION')
                ignore_value = Config.get(session_bck, 'CONDITION_TO_IGNORE_VALUE')
                publication_date_positions = Config.get(session_bck, 'PUBLICATION_DATE_POSITIONS')
                publication_hour_positions = Config.get(session_bck, 'PUBLICATION_HOUR_POSITIONS')
                date_format = Config.get(session_bck, 'DATEFORMAT')
                element01 = Config.get(session_bck, 'ELEMENT01')
                element02 = Config.get(session_bck, 'ELEMENT02')
                element03 = Config.get(session_bck, 'ELEMENT03')
                element04 = Config.get(session_bck, 'ELEMENT04')
                element05 = Config.get(session_bck, 'ELEMENT05')
                element06 = Config.get(session_bck, 'ELEMENT06')
                element07 = Config.get(session_bck, 'ELEMENT07')
                element08 = Config.get(session_bck, 'ELEMENT08')
                element09 = Config.get(session_bck, 'ELEMENT09')
                quality = Config.get(session_bck, 'QUALITY')
                applies_date = Config.get(session_bck, 'APPLIES_DATE')
                applies_hour = Config.get(session_bck, 'APPLIES_HOUR')
                publication_date = Config.get(session_bck, 'PUBLICATION_DATE')
                publication_hour = Config.get(session_bck, 'PUBLICATION_HOUR')
                date_format_check = Config.get(session_bck, 'NUMBER_TO_DATE_FORMAT')
                value_positions = Config.get(session_bck, 'VALUE_POSITIONS')
                translation_condition = Config.get('default', 'T_TRANSLATION')
                translation_word = Config.get('default', 'T_TRANSLATEWORD')
                date_filter = Config.get(session_bck, 'DATE_FILTER')
                filter_condition1 = Config.get(session_bck, 'FILTER_CONDITION1')
                filter_data = Config.get(session_bck, 'FILTER_DATA')
                applies_hour_filter_type = Config.get(session_bck, 'APPLIES_HOUR_FILTER_TYPE')
                publication_hour_filter_type = Config.get(session_bck, 'PUBLICATION_HOUR_FILTER_TYPE')
                value_normalize = Config.get(session_bck, 'CONDITION_TO_VALUE_NORMALIZE')
                date_position_custom, date_custom = '', ''
                try:
                    date_position_custom = Config.get(session_bck, 'DATE_POSITION_CUSTOM')
                    date_custom = Config.get(session_bck, 'DATE_CUSTOM')
                except:
                    date_position_custom = 'n/a'
                    date_custom = 'n/a'
                try:
                    quality = Config.get(session_bck, 'QUALITY_POSITIONS')
                except:
                    quality_positions='n/a'
            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                print error_log
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                sys.exit()
                break

            ''' Read the raw excel file content and stored it in variable ''' 
            book, sheet = '', ''
            try:
                if '.xls' in str(filename) or '.xlsx' in str(filename):
                    book = xlrd.open_workbook(str(filename))
                else:
                    break

            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                print error_log
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                sys.exit()
                # break
            try:
                sheet = book.sheet_by_name(sheet_name)
            except Exception as e:
                break
            ''' call the function to get Elements '''
            quality_val=''
            row_count = int(sheet.nrows)
            try:
                element01_val = Get_Excel_Elements(sheet, element01, element01_positions, row_count)
                element02_val = Get_Excel_Elements(sheet, element02, element02_positions, row_count)
                element03_val = Get_Excel_Elements(sheet, element03, element03_positions, row_count)
                element04_val = Get_Excel_Elements(sheet, element04, element04_positions, row_count)
                element05_val = Get_Excel_Elements(sheet, element05, element05_positions, row_count)
                element06_val = Get_Excel_Elements(sheet, element06, element06_positions, row_count)
                element07_val = Get_Excel_Elements(sheet, element07, element07_positions, row_count)
                element08_val = Get_Excel_Elements(sheet, element08, element08_positions, row_count)
                element09_val = Get_Excel_Elements(sheet, element09, element09_positions, row_count)
                filter_data_values = Get_Excel_Elements(sheet, 'n/a', filter_data, row_count)
                if str(quality_positions) != 'n/a' and str(quality) != '':
                    quality_val = Get_Excel_Elements(sheet, quality_positions, quality_positions, row_count)
                
                ''' call the function to get values '''
                try:
                    values = Get_Excel_Values(sheet, value_positions, row_count)
                except:
                    break

                ''' call the function to get date '''
                applies_date_value = ''

                if str(date_position_custom) != 'n/a':

                    applies_date_value = date_custom_function(datasourceid, sheet, date_position_custom, date_custom,row_count)
                else:
                    applies_date_value = Get_Excel_applies_to_datetime(book, sheet, applies_date,applies_date_positions, date_format_check,date_format, row_count)

                date_format_1 = ''
                try:
                    date_format_1 = Config.get(session_bck, 'PUBLICATION_DATEFORMAT')
                    date_format_check = 'N'
                except:
                    date_format_1 = date_format

                publication_date_value = Get_Excel_applies_to_datetime(book, sheet, publication_date,publication_date_positions, date_format_check,date_format_1, row_count)

                ''' call the function to get time '''

                applies_hour_value = Get_Excel_applies_to_time(book, sheet, applies_hour, applies_hour_positions, 'n/a','n/a', row_count)

                publication_hour_value = Get_Excel_applies_to_time(book, sheet, publication_hour,publication_hour_positions, 'n/a', 'n/a', row_count)
                
            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                print error_log
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                sys.exit()
                break

            ''' Initialize the increment variables  '''
            element01_col_inc, element02_col_inc, element03_col_inc, element04_col_inc, element05_col_inc, element06_col_inc, element07_col_inc, element08_col_inc, element09_col_inc, date_col_inc, hour_col_inc, publication_date_col_inc, publication_hour_col_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            element01_row_inc, element02_row_inc, element03_row_inc, element04_row_inc, element05_row_inc, element06_row_inc, element07_row_inc, element08_row_inc, element09_row_inc, date_row_inc, hour_row_inc, publication_date_row_inc, publication_hour_row_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            quality_row_inc,quality_col_inc = 0,0
            column_number, condition_value = '', ''
            if str(filter_condition1) != 'n/a':
                filter_condition = ast.literal_eval(filter_condition1)
                column_number = filter_condition.get('column_number')
                condition_value = filter_condition.get('condition_value')

            plus_date, minus_date = '', ''
            if str(date_filter) != 'n/a':
                filter_fields = ast.literal_eval(date_filter)

                plus_date = filter_fields.get('plus_date')
                minus_date = filter_fields.get('minus_date')

            ''' Start iteration based on the elements length to generate the xml file '''
            # print len(applies_date_value)
            # print len(values)
            # raw_input()
            for col_value in values:

                for j, row_value in enumerate(col_value):

                    if (str(row_value).strip() != "") and str(applies_date_value[date_col_inc][date_row_inc]).strip() != "":
                        el1, el2, el3, el4, el5, el6, el7, el8, el9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
                        # print row_value
                        el1 = translate(element01_val[element01_col_inc][element01_row_inc], translation_condition,
                                        translation_word)
                        el2 = translate(element02_val[element02_col_inc][element02_row_inc], translation_condition,
                                        translation_word)
                        el3 = translate(element03_val[element03_col_inc][element03_row_inc], translation_condition,
                                        translation_word)
                        el4 = translate(element04_val[element04_col_inc][element04_row_inc], translation_condition,
                                        translation_word)
                        el5 = translate(element05_val[element05_col_inc][element05_row_inc], translation_condition,
                                        translation_word)
                        el6 = translate(element06_val[element06_col_inc][element06_row_inc], translation_condition,
                                        translation_word)
                        el7 = translate(element07_val[element07_col_inc][element07_row_inc], translation_condition,
                                        translation_word)
                        el8 = translate(element08_val[element08_col_inc][element08_row_inc], translation_condition,
                                        translation_word)
                        el9 = translate(element09_val[element09_col_inc][element09_row_inc], translation_condition,
                                        translation_word)
                        qualityValue=''
                        if str(quality_positions) != 'n/a' and str(quality) != '':
                            qualityValue = quality_val[quality_col_inc][quality_row_inc]
                            
                        applies_date_temp = ''
                        publication_date_temp = ''
                        if str(applies_date_value[date_col_inc][date_row_inc]) != 'n/a':
                            applies_date_temp = str(applies_date_value[date_col_inc][date_row_inc])
                        else:
                            applies_date_temp = now.strftime("%Y-%m-%d")

                        if str(publication_date_value[publication_date_col_inc][publication_date_row_inc]) != 'n/a':

                            publication_date_temp = str( publication_date_value[publication_date_col_inc][publication_date_row_inc])
                        else:
                            publication_date_temp = strftime("%Y-%m-%d", gmtime())

                        format_applies_date, format_publication_date = '', ''

                        format_applies_date = datetime_format(applies_date_temp,applies_hour_value[hour_col_inc][hour_row_inc], 1, 'n/a',applies_hour_filter_type)
                        
                        #publication_date,publication_hour
                        
                        if str(publication_date) != 'n/a' or str(publication_date_positions) != 'n/a':
                            format_publication_date = datetime_format(publication_date_temp,publication_hour_value[publication_hour_col_inc][publication_hour_row_inc], 1, 'n/a',publication_hour_filter_type)
                        elif str(publication_date) == 'n/a' and str(publication_date_positions) == 'n/a' and str(publication_hour_filter_type) != 'n/a':
                            n = 0
                            publication_temp_hour_value1 = eval(publication_hour_filter_type)
                            # print "publication_temp_hour_value1",publication_temp_hour_value1
                            # print "format_applies_date",format_applies_date
                            d1 = datetime.strptime(str(format_applies_date), '%Y-%m-%dT%H:%M:%S.0000000') + timedelta(minutes=int(publication_temp_hour_value1))
                            # print "d1",d1
                            format_publication_date = d1.strftime('%Y-%m-%dT00:00:00.0000000')
                            # print "format_publication_date",format_publication_date
                        else:
                            format_publication_date = publicationformat_date
                        '''
                        Filter condition
                        '''
                        condition1 = ''
                        condition2 = ''
                        if (str(filter_condition1) != 'n/a'):
                            if (re.search((condition_value).replace('{', '').replace('}', '').replace('REGEX', ''),
                                          str(filter_data_values[column_number][j])) is not None):
                                condition1 = 'True'
                            else:
                                condition1 = 'False'
                        else:
                            condition1 = 'True'

                        '''
                        Validating Date condition and filter condition
                        '''
                        if str(date_filter) != 'n/a':
                            check_day_plus = date.today() + timedelta(int(plus_date))
                            day_plus = check_day_plus.strftime('%d')
                            month_plus = check_day_plus.strftime('%m')
                            check_day_minus = date.today() - timedelta(int(minus_date))
                            day_minus = check_day_minus.strftime('%d')
                            month_minus = check_day_minus.strftime('%m')
                            date_plus_a_day = datetime(now.year, int(month_plus), int(day_plus))
                            date_minus_a_day = datetime(now.year, int(month_minus), int(day_minus))
                            date_plus = str(check_day_plus.strftime('%Y-%m-%d'))
                            date_minus = str(check_day_minus.strftime('%Y-%m-%d'))
                            applies_date_validation = applies_date_temp
                            if date_plus >= applies_date_validation and date_minus <= applies_date_validation:
                                condition2 = 'True'
                            else:
                                condition2 = 'False'
                        else:
                            condition2 = 'True'

                        if (re.match(ignore_value, str(row_value)) is None) and (str(row_value).strip() != "") and condition1 == 'True' and condition2 == 'True':

                            element = ''
                            # print "row_value",row_value

                            if str(element01) != 'n/a' or str(element01_positions) != 'n/a':
                                element = re.sub(r'^\\n\s+\s*', '', str(el1).strip())
                            if str(element02) != 'n/a' or str(element02_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el2).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element03) != 'n/a' or str(element03_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el3).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element04) != 'n/a' or str(element04_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el4).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element05) != 'n/a' or str(element05_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el5).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element06) != 'n/a' or str(element06_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el6).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element07) != 'n/a' or str(element07_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el7).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'
                            if str(element08) != 'n/a' or str(element08_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el8).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'

                            if str(element09) != 'n/a' or str(element09_positions) != 'n/a':
                                element = str(element) + '|' + str(re.sub(r'\\n\s+\s*', '', str(el9).strip()))
                            else:
                                element = str(element) + '|' + 'n/a'
                            
                            date_format1 = datetime.strptime(str(format_applies_date), '%Y-%m-%dT%H:%M:%S.0000000')
                            dateValidationList.append(str(date_format1.strftime('%Y-%m-%d')))
                            value_count = value_count + 1
                            xml_key = 'time_series' + '|' + str(last_date) + '|' + str(first_date) + '|' + str(
                                frequency_type) + '|' + 'xref|' + element + '|' + str(data_source)
                            val_formattted = ''
                            if str(value_normalize) == 'yes':
                                val_formattted=value_replace(str(clean_fn(str(row_value).replace('..','0').replace('%',''))).replace(' ', ''))
                            
                            elif str(value_normalize) == 'yes1':
                                val_formattted=value_replace_spl(str(clean_fn(str(row_value).replace('..','0').replace('%',''))).replace(' ', '')) 
                            else:
                                val_formattted = clean_fn(
                                    str(row_value).replace('..', '0').replace('%', '').replace(' ', ''))

                            xml_value = 'datum' + '|' + str(format_applies_date) + '|' + str(
                                format_publication_date) + '|' + str(val_formattted) + '|' + str(quality)
                            xml_dict.setdefault(xml_key, []).append(xml_value)
                            xml_value = ''
                            xml_key = ''
                    if (len(col_value) == len(element01_val[element01_col_inc])):
                        element01_row_inc = element01_row_inc + 1
                    if (len(col_value) == len(element02_val[element02_col_inc])):
                        element02_row_inc = element02_row_inc + 1
                    if (len(col_value) == len(element03_val[element03_col_inc])):
                        element03_row_inc = element03_row_inc + 1
                    if (len(col_value) == len(element04_val[element04_col_inc])):
                        element04_row_inc = element04_row_inc + 1
                    if (len(col_value) == len(element05_val[element05_col_inc])):
                        element05_row_inc = element05_row_inc + 1
                    if (len(col_value) == len(element06_val[element06_col_inc])):
                        element06_row_inc = element06_row_inc + 1
                    if (len(col_value) == len(element07_val[element07_col_inc])):
                        element07_row_inc = element07_row_inc + 1
                    if (len(col_value) == len(element08_val[element08_col_inc])):
                        element08_row_inc = element08_row_inc + 1
                    if (len(col_value) == len(element09_val[element09_col_inc])):
                        element09_row_inc = element09_row_inc + 1
                    if (len(col_value) == len(applies_date_value[date_col_inc])):
                        date_row_inc = date_row_inc + 1
                    if (len(col_value) == len(applies_hour_value[hour_col_inc])):
                        hour_row_inc = hour_row_inc + 1
                    if (len(col_value) == len(publication_hour_value[publication_hour_col_inc])):
                        publication_hour_row_inc = publication_hour_row_inc + 1
                    if (len(col_value) == len(publication_date_value[publication_date_col_inc])):
                        publication_date_row_inc = publication_date_row_inc + 1 
                    if str(quality_positions) != 'n/a' and str(quality) != '':
                        if (len(col_value) == len(quality_val[quality_col_inc])):
                            quality_row_inc = quality_row_inc + 1     
                    
                if int(len(values)) == int(len(element01_val)):
                    element01_col_inc = element01_col_inc + 1
                if int(len(values)) == int(len(element02_val)):
                    element02_col_inc = element02_col_inc + 1
                if int(len(values)) == int(len(element03_val)):
                    element03_col_inc = element03_col_inc + 1
                if int(len(values)) == int(len(element04_val)):
                    element04_col_inc = element04_col_inc + 1
                if int(len(values)) == int(len(element05_val)):
                    element05_col_inc = element05_col_inc + 1
                if int(len(values)) == int(len(element06_val)):
                    element06_col_inc = element06_col_inc + 1
                if int(len(values)) == int(len(element07_val)):
                    element07_col_inc = element07_col_inc + 1
                if int(len(values)) == int(len(element08_val)):
                    element08_col_inc = element08_col_inc + 1
                if int(len(values)) == int(len(element09_val)):
                    element09_col_inc = element09_col_inc + 1
                if int(len(values)) == int(len(applies_date_value)):
                    date_col_inc = date_col_inc + 1
                if int(len(values)) == int(len(applies_hour_value)):
                    hour_col_inc = hour_col_inc + 1
                if (len(values) == len(publication_hour_value)):
                    publication_hour_col_inc = publication_hour_col_inc + 1
                if (len(values) == len(publication_date_value)):
                    publication_date_col_inc = publication_date_col_inc + 1 
                if str(quality_positions) != 'n/a' and str(quality) != '':
                    if (len(values) == len(quality_val)):
                        quality_col_inc = quality_col_inc + 1     
                    
                publication_date_row_inc,publication_hour_row_inc,element01_row_inc, element02_row_inc, element03_row_inc, element04_row_inc, element05_row_inc, element06_row_inc, element07_row_inc, element08_row_inc, element09_row_inc, date_row_inc, hour_row_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0

        return xml_dict, value_count,dateValidationList
    except Exception as e:
        error_log = e, str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
def special_char_replace(value):
    value = re.sub(r'\\xc3\\x80','À',str(value))
    value = re.sub(r'\\xc3\\x81','Á',str(value))
    value = re.sub(r'\\xc3\\x82','Â',str(value))
    value = re.sub(r'\\xc3\\x83','Ã',str(value))
    value = re.sub(r'\\xc3\\x84','Ä',str(value))
    value = re.sub(r'\\xc3\\x85','Å',str(value))
    value = re.sub(r'\\xc3\\x86','Æ',str(value))
    value = re.sub(r'\\xc3\\x87','Ç',str(value))
    value = re.sub(r'\\xc3\\x88','È',str(value))
    value = re.sub(r'\\xc3\\x89','É',str(value))
    value = re.sub(r'\\xc3\\x8a','Ê',str(value))
    value = re.sub(r'\\xc3\\x8b','Ë',str(value))
    value = re.sub(r'\\xc3\\x8c','Ì',str(value))
    value = re.sub(r'\\xc3\\x8d','Í',str(value))
    value = re.sub(r'\\xc3\\x8e','Î',str(value))
    value = re.sub(r'\\xc3\\x8f','Ï',str(value))
    value = re.sub(r'\\xc3\\x90','Ð',str(value))
    value = re.sub(r'\\xc3\\x91','Ñ',str(value))
    value = re.sub(r'\\xc3\\x92','Ò',str(value))
    value = re.sub(r'\\xc3\\x93','Ó',str(value))
    value = re.sub(r'\\xc3\\x94','Ô',str(value))
    value = re.sub(r'\\xc3\\x95','Õ',str(value))
    value = re.sub(r'\\xc3\\x96','Ö',str(value))
    value = re.sub(r'\\xc3\\x98','Ø',str(value))
    value = re.sub(r'\\xc3\\x99','Ù',str(value))
    value = re.sub(r'\\xc3\\x9a','Ú',str(value))
    value = re.sub(r'\\xc3\\x9b','Û',str(value))
    value = re.sub(r'\\xc3\\x9c','Ü',str(value))
    value = re.sub(r'\\xc3\\x9d','Ý',str(value))
    value = re.sub(r'\\xc3\\x9e','Þ',str(value))
    value = re.sub(r'\\xc3\\x9f','ß',str(value))
    value = re.sub(r'\\xc3\\xa0','à',str(value))
    value = re.sub(r'\\xc3\\xa1','á',str(value))
    value = re.sub(r'\\xc3\\xa2','â',str(value))
    value = re.sub(r'\\xc3\\xa3','ã',str(value))
    value = re.sub(r'\\xc3\\xa4','ä',str(value))
    value = re.sub(r'\\xc3\\xa5','å',str(value))
    value = re.sub(r'\\xc3\\xa6','æ',str(value))
    value = re.sub(r'\\xc3\\xa7','ç',str(value))
    value = re.sub(r'\\xc3\\xa7','ç',str(value))
    value = re.sub(r'\\xc3\\xa8','è',str(value))
    value = re.sub(r'\\xc3\\xa9','é',str(value))
    value = re.sub(r'\\xc3\\xaa','ê',str(value))
    value = re.sub(r'\\xc3\\xab','ë',str(value))
    value = re.sub(r'\\xc3\\xac','ì',str(value))
    value = re.sub(r'\\xc3\\xad','í',str(value))
    value = re.sub(r'\\xc3\\xae','î',str(value))
    value = re.sub(r'\\xc3\\xaf','ï',str(value))
    value = re.sub(r'\\xc3\\xb0','ð',str(value))
    value = re.sub(r'\\xc3\\xb1','ñ',str(value))
    value = re.sub(r'\\xc3\\xb2','ò',str(value))
    value = re.sub(r'\\xc3\\xb3','ó',str(value))
    value = re.sub(r'\\xc3\\xb4','ô',str(value))
    value = re.sub(r'\\xc3\\xb5','õ',str(value))
    value = re.sub(r'\\xc3\\xb6','ö',str(value))
    value = re.sub(r'\\xc3\\xb8','ø',str(value))
    value = re.sub(r'\\xc3\\xb9','ù',str(value))
    value = re.sub(r'\\xc3\\xba','ú',str(value))
    value = re.sub(r'\\xc3\\xbb','û',str(value))
    value = re.sub(r'\\xc3\\xbc','ü',str(value))
    value = re.sub(r'\\xc3\\xbd','ý',str(value))
    value = re.sub(r'\\xc3\\xbe','þ',str(value))
    value = re.sub(r'\\xc3\\xbf','ÿ',str(value))
    value = re.sub(r'\\xc4\\x80','Ā',str(value))
    value = re.sub(r'\\xc4\\x81','ā',str(value))
    value = re.sub(r'\\xc4\\x82','Ă',str(value))
    value = re.sub(r'\\xc4\\x83','ă',str(value))
    value = re.sub(r'\\xc4\\x84','Ą',str(value))
    value = re.sub(r'\\xc4\\x85','ą',str(value))
    value = re.sub(r'\\xc4\\x86','Ć',str(value))
    value = re.sub(r'\\xc4\\x87','ć',str(value))
    value = re.sub(r'\\xc4\\x88','Ĉ',str(value))
    value = re.sub(r'\\xc4\\x89','ĉ',str(value))
    value = re.sub(r'\\xc4\\x8a','Ċ',str(value))
    value = re.sub(r'\\xc4\\x8b','ċ',str(value))
    value = re.sub(r'\\xc4\\x8c','Č',str(value))
    value = re.sub(r'\\xc4\\x8d','č',str(value))
    value = re.sub(r'\\xc4\\x8e','Ď',str(value))
    value = re.sub(r'\\xc4\\x8f','ď',str(value))
    value = re.sub(r'\\xc4\\x90','Đ',str(value))
    value = re.sub(r'\\xc4\\x91','đ',str(value))
    value = re.sub(r'\\xc4\\x92','Ē',str(value))
    value = re.sub(r'\\xc4\\x93','ē',str(value))
    value = re.sub(r'\\xc4\\x94','Ĕ',str(value))
    value = re.sub(r'\\xc4\\x95','ĕ',str(value))
    value = re.sub(r'\\xc4\\x96','Ė',str(value))
    value = re.sub(r'\\xc4\\x97','ė',str(value))
    value = re.sub(r'\\xc4\\x98','Ę',str(value))
    value = re.sub(r'\\xc4\\x99','ę',str(value))
    value = re.sub(r'\\xc4\\x9a','Ě',str(value))
    value = re.sub(r'\\xc4\\x9b','ě',str(value))
    value = re.sub(r'\\xc4\\x9c','Ĝ',str(value))
    value = re.sub(r'\\xc4\\x9d','ĝ',str(value))
    value = re.sub(r'\\xc4\\x9e','Ğ',str(value))
    value = re.sub(r'\\xc4\\x9f','ğ',str(value))
    value = re.sub(r'\\xc4\\xa0','Ġ',str(value))
    value = re.sub(r'\\xc4\\xa1','ġ',str(value))
    value = re.sub(r'\\xc4\\xa2','Ģ',str(value))
    value = re.sub(r'\\xc4\\xa3','ģ',str(value))
    value = re.sub(r'\\xc4\\xa4','Ĥ',str(value))
    value = re.sub(r'\\xc4\\xa5','ĥ',str(value))
    value = re.sub(r'\\xc4\\xa6','Ħ',str(value))
    value = re.sub(r'\\xc4\\xa7','ħ',str(value))
    value = re.sub(r'\\xc4\\xa8','Ĩ',str(value))
    value = re.sub(r'\\xc4\\xa9','ĩ',str(value))
    value = re.sub(r'\\xc4\\xaa','Ī',str(value))
    value = re.sub(r'\\xc4\\xab','ī',str(value))
    value = re.sub(r'\\xc4\\xac','Ĭ',str(value))
    value = re.sub(r'\\xc4\\xad','ĭ',str(value))
    value = re.sub(r'\\xc4\\xae','Į',str(value))
    value = re.sub(r'\\xc4\\xaf','į',str(value))
    value = re.sub(r'\\xc4\\xb0','İ',str(value))
    value = re.sub(r'\\xc4\\xb1','ı',str(value))
    value = re.sub(r'\\xc4\\xb2','Ĳ',str(value))
    value = re.sub(r'\\xc4\\xb3','ĳ',str(value))
    value = re.sub(r'\\xc4\\xb4','Ĵ',str(value))
    value = re.sub(r'\\xc4\\xb5','ĵ',str(value))
    value = re.sub(r'\\xc4\\xb6','Ķ',str(value))
    value = re.sub(r'\\xc4\\xb7','ķ',str(value))
    value = re.sub(r'\\xc4\\xb8','ĸ',str(value))
    value = re.sub(r'\\xc4\\xb9','Ĺ',str(value))
    value = re.sub(r'\\xc4\\xba','ĺ',str(value))
    value = re.sub(r'\\xc4\\xbb','Ļ',str(value))
    value = re.sub(r'\\xc4\\xbc','ļ',str(value))
    value = re.sub(r'\\xc4\\xbd','Ľ',str(value))
    value = re.sub(r'\\xc4\\xbe','ľ',str(value))
    value = re.sub(r'\\xc4\\xbf','Ŀ',str(value))
    value = re.sub(r'\\xc5\\x80','ŀ',str(value))
    value = re.sub(r'\\xc5\\x81','Ł',str(value))
    value = re.sub(r'\\xc5\\x82','ł',str(value))
    value = re.sub(r'\\xc5\\x83','Ń',str(value))
    value = re.sub(r'\\xc5\\x84','ń',str(value))
    value = re.sub(r'\\xc5\\x85','Ņ',str(value))
    value = re.sub(r'\\xc5\\x86','ņ',str(value))
    value = re.sub(r'\\xc5\\x87','Ň',str(value))
    value = re.sub(r'\\xc5\\x88','ň',str(value))
    value = re.sub(r'\\xc5\\x89','ŉ',str(value))
    value = re.sub(r'\\xc5\\x8a','Ŋ',str(value))
    value = re.sub(r'\\xc5\\x8b','ŋ',str(value))
    value = re.sub(r'\\xc5\\x8c','Ō',str(value))
    value = re.sub(r'\\xc5\\x8d','ō',str(value))
    value = re.sub(r'\\xc5\\x8e','Ŏ',str(value))
    value = re.sub(r'\\xc5\\x8f','ŏ',str(value))
    value = re.sub(r'\\xc5\\x90','Ő',str(value))
    value = re.sub(r'\\xc5\\x91','ő',str(value))
    value = re.sub(r'\\xc5\\x92','Œ',str(value))
    value = re.sub(r'\\xc5\\x93','œ',str(value))
    value = re.sub(r'\\xc5\\x94','Ŕ',str(value))
    value = re.sub(r'\\xc5\\x95','ŕ',str(value))
    value = re.sub(r'\\xc5\\x96','Ŗ',str(value))
    value = re.sub(r'\\xc5\\x97','ŗ',str(value))
    value = re.sub(r'\\xc5\\x98','Ř',str(value))
    value = re.sub(r'\\xc5\\x99','ř',str(value))
    value = re.sub(r'\\xc5\\x9a','Ś',str(value))
    value = re.sub(r'\\xc5\\x9b','ś',str(value))
    value = re.sub(r'\\xc5\\x9c','Ŝ',str(value))
    value = re.sub(r'\\xc5\\x9d','ŝ',str(value))
    value = re.sub(r'\\xc5\\x9e','Ş',str(value))
    value = re.sub(r'\\xc5\\x9f','ş',str(value))
    value = re.sub(r'\\xc5\\xa0','Š',str(value))
    value = re.sub(r'\\xc5\\xa1','š',str(value))
    value = re.sub(r'\\xc5\\xa2','Ţ',str(value))
    value = re.sub(r'\\xc5\\xa3','ţ',str(value))
    value = re.sub(r'\\xc5\\xa4','Ť',str(value))
    value = re.sub(r'\\xc5\\xa5','ť',str(value))
    value = re.sub(r'\\xc5\\xa6','Ŧ',str(value))
    value = re.sub(r'\\xc5\\xa7','ŧ',str(value))
    value = re.sub(r'\\xc5\\xa8','Ũ',str(value))
    value = re.sub(r'\\xc5\\xa9','ũ',str(value))
    value = re.sub(r'\\xc5\\xaa','Ū',str(value))
    value = re.sub(r'\\xc5\\xab','ū',str(value))
    value = re.sub(r'\\xc5\\xac','Ŭ',str(value))
    value = re.sub(r'\\xc5\\xad','ŭ',str(value))
    value = re.sub(r'\\xc5\\xae','Ů',str(value))
    value = re.sub(r'\\xc5\\xaf','ů',str(value))
    value = re.sub(r'\\xc5\\xb0','Ű',str(value))
    value = re.sub(r'\\xc5\\xb1','ű',str(value))
    value = re.sub(r'\\xc5\\xb2','Ų',str(value))
    value = re.sub(r'\\xc5\\xb3','ų',str(value))
    value = re.sub(r'\\xc5\\xb4','Ŵ',str(value))
    value = re.sub(r'\\xc5\\xb5','ŵ',str(value))
    value = re.sub(r'\\xc5\\xb6','Ŷ',str(value))
    value = re.sub(r'\\xc5\\xb7','ŷ',str(value))
    value = re.sub(r'\\xc5\\xb8','Ÿ',str(value))
    value = re.sub(r'\\xc5\\xb9','Ź',str(value))
    value = re.sub(r'\\xc5\\xba','ź',str(value))
    value = re.sub(r'\\xc5\\xbb','Ż',str(value))
    value = re.sub(r'\\xc5\\xbc','ż',str(value))
    value = re.sub(r'\\xc5\\xbd','Ž',str(value))
    value = re.sub(r'\\xc5\\xbe','ž',str(value))
    value = re.sub(r'\\xc5\\xbf','ſ',str(value))
    value = re.sub(r'\\xc6\\x80','ƀ',str(value))
    value = re.sub(r'\\xc6\\x81','Ɓ',str(value))
    value = re.sub(r'\\xc6\\x82','Ƃ',str(value))
    value = re.sub(r'\\xc6\\x83','ƃ',str(value))
    value = re.sub(r'\\xc6\\x84','Ƅ',str(value))
    value = re.sub(r'\\xc6\\x85','ƅ',str(value))
    value = re.sub(r'\\xc6\\x86','Ɔ',str(value))
    value = re.sub(r'\\xc6\\x87','Ƈ',str(value))
    value = re.sub(r'\\xc6\\x88','ƈ',str(value))
    value = re.sub(r'\\xc6\\x89','Ɖ',str(value))
    value = re.sub(r'\\xc6\\x8a','Ɗ',str(value))
    value = re.sub(r'\\xc6\\x8b','Ƌ',str(value))
    value = re.sub(r'\\xc6\\x8c','ƌ',str(value))
    value = re.sub(r'\\xc6\\x8d','ƍ',str(value))
    value = re.sub(r'\\xc6\\x8e','Ǝ',str(value))
    value = re.sub(r'\\xc6\\x8f','Ə',str(value))
    value = re.sub(r'\\xc6\\x90','Ɛ',str(value))
    value = re.sub(r'\\xc6\\x91','Ƒ',str(value))
    value = re.sub(r'\\xc6\\x92','ƒ',str(value))
    value = re.sub(r'\\xc6\\x93','Ɠ',str(value))
    value = re.sub(r'\\xc6\\x94','Ɣ',str(value))
    value = re.sub(r'\\xc6\\x95','ƕ',str(value))
    value = re.sub(r'\\xc6\\x96','Ɩ',str(value))
    value = re.sub(r'\\xc6\\x97','Ɨ',str(value))
    value = re.sub(r'\\xc6\\x98','Ƙ',str(value))
    value = re.sub(r'\\xc6\\x99','ƙ',str(value))
    value = re.sub(r'\\xc6\\x9a','ƚ',str(value))
    value = re.sub(r'\\xc6\\x9b','ƛ',str(value))
    value = re.sub(r'\\xc6\\x9c','Ɯ',str(value))
    value = re.sub(r'\\xc6\\x9d','Ɲ',str(value))
    value = re.sub(r'\\xc6\\x9e','ƞ',str(value))
    value = re.sub(r'\\xc6\\x9f','Ɵ',str(value))
    value = re.sub(r'\\xc6\\xa0','Ơ',str(value))
    value = re.sub(r'\\xc6\\xa1','ơ',str(value))
    value = re.sub(r'\\xc6\\xa2','Ƣ',str(value))
    value = re.sub(r'\\xc6\\xa3','ƣ',str(value))
    value = re.sub(r'\\xc6\\xa4','Ƥ',str(value))
    value = re.sub(r'\\xc6\\xa5','ƥ',str(value))
    value = re.sub(r'\\xc6\\xa6','Ʀ',str(value))
    value = re.sub(r'\\xc6\\xa7','Ƨ',str(value))
    value = re.sub(r'\\xc6\\xa8','ƨ',str(value))
    value = re.sub(r'\\xc6\\xa9','Ʃ',str(value))
    value = re.sub(r'\\xc6\\xaa','ƪ',str(value))
    value = re.sub(r'\\xc6\\xab','ƫ',str(value))
    value = re.sub(r'\\xc6\\xac','Ƭ',str(value))
    value = re.sub(r'\\xc6\\xad','ƭ',str(value))
    value = re.sub(r'\\xc6\\xae','Ʈ',str(value))
    value = re.sub(r'\\xc6\\xaf','Ư',str(value))
    value = re.sub(r'\\xc6\\xb0','ư',str(value))
    value = re.sub(r'\\xc6\\xb1','Ʊ',str(value))
    value = re.sub(r'\\xc6\\xb2','Ʋ',str(value))
    value = re.sub(r'\\xc6\\xb3','Ƴ',str(value))
    value = re.sub(r'\\xc6\\xb4','ƴ',str(value))
    value = re.sub(r'\\xc6\\xb5','Ƶ',str(value))
    value = re.sub(r'\\xc6\\xb6','ƶ',str(value))
    value = re.sub(r'\\xc6\\xb7','Ʒ',str(value))
    value = re.sub(r'\\xc6\\xb8','Ƹ',str(value))
    value = re.sub(r'\\xc6\\xb9','ƹ',str(value))
    value = re.sub(r'\\xc6\\xba','ƺ',str(value))
    value = re.sub(r'\\xc6\\xbb','ƻ',str(value))
    value = re.sub(r'\\xc6\\xbc','Ƽ',str(value))
    value = re.sub(r'\\xc6\\xbd','ƽ',str(value))
    value = re.sub(r'\\xc6\\xbe','ƾ',str(value))
    value = re.sub(r'\\xc6\\xbf','ƿ',str(value))
    value = re.sub(r'\\xc7\\x80','ǀ',str(value))
    value = re.sub(r'\\xc7\\x81','ǁ',str(value))
    value = re.sub(r'\\xc7\\x82','ǂ',str(value))
    value = re.sub(r'\\xc7\\x83','ǃ',str(value))
    value = re.sub(r'\\xc7\\x84','Ǆ',str(value))
    value = re.sub(r'\\xc7\\x85','ǅ',str(value))
    value = re.sub(r'\\xc7\\x86','ǆ',str(value))
    value = re.sub(r'\\xc7\\x87','Ǉ',str(value))
    value = re.sub(r'\\xc7\\x88','ǈ',str(value))
    value = re.sub(r'\\xc7\\x89','ǉ',str(value))
    value = re.sub(r'\\xc7\\x8a','Ǌ',str(value))
    value = re.sub(r'\\xc7\\x8b','ǋ',str(value))
    value = re.sub(r'\\xc7\\x8c','ǌ',str(value))
    value = re.sub(r'\\xc7\\x8d','Ǎ',str(value))
    value = re.sub(r'\\xc7\\x8e','ǎ',str(value))
    value = re.sub(r'\\xc7\\x8f','Ǐ',str(value))
    value = re.sub(r'\\xc7\\x90','ǐ',str(value))
    value = re.sub(r'\\xc7\\x91','Ǒ',str(value))
    value = re.sub(r'\\xc7\\x92','ǒ',str(value))
    value = re.sub(r'\\xc7\\x93','Ǔ',str(value))
    value = re.sub(r'\\xc7\\x94','ǔ',str(value))
    value = re.sub(r'\\xc7\\x95','Ǖ',str(value))
    value = re.sub(r'\\xc7\\x96','ǖ',str(value))
    value = re.sub(r'\\xc7\\x97','Ǘ',str(value))
    value = re.sub(r'\\xc7\\x98','ǘ',str(value))
    value = re.sub(r'\\xc7\\x99','Ǚ',str(value))
    value = re.sub(r'\\xc7\\x9a','ǚ',str(value))
    value = re.sub(r'\\xc7\\x9b','Ǜ',str(value))
    value = re.sub(r'\\xc7\\x9c','ǜ',str(value))
    value = re.sub(r'\\xc7\\x9d','ǝ',str(value))
    value = re.sub(r'\\xc7\\x9e','Ǟ',str(value))
    value = re.sub(r'\\xc7\\x9f','ǟ',str(value))
    value = re.sub(r'\\xc7\\xa0','Ǡ',str(value))
    value = re.sub(r'\\xc7\\xa1','ǡ',str(value))
    value = re.sub(r'\\xc7\\xa2','Ǣ',str(value))
    value = re.sub(r'\\xc7\\xa3','ǣ',str(value))
    value = re.sub(r'\\xc7\\xa4','Ǥ',str(value))
    value = re.sub(r'\\xc7\\xa5','ǥ',str(value))
    value = re.sub(r'\\xc7\\xa6','Ǧ',str(value))
    value = re.sub(r'\\xc7\\xa7','ǧ',str(value))
    value = re.sub(r'\\xc7\\xa8','Ǩ',str(value))
    value = re.sub(r'\\xc7\\xa9','ǩ',str(value))
    value = re.sub(r'\\xc7\\xaa','Ǫ',str(value))
    value = re.sub(r'\\xc7\\xab','ǫ',str(value))
    value = re.sub(r'\\xc7\\xac','Ǭ',str(value))
    value = re.sub(r'\\xc7\\xad','ǭ',str(value))
    value = re.sub(r'\\xc7\\xae','Ǯ',str(value))
    value = re.sub(r'\\xc7\\xaf','ǯ',str(value))
    value = re.sub(r'\\xc7\\xb0','ǰ',str(value))
    value = re.sub(r'\\xc7\\xb1','Ǳ',str(value))
    value = re.sub(r'\\xc7\\xb2','ǲ',str(value))
    value = re.sub(r'\\xc7\\xb3','ǳ',str(value))
    value = re.sub(r'\\xc7\\xb4','Ǵ',str(value))
    value = re.sub(r'\\xc7\\xb5','ǵ',str(value))
    value = re.sub(r'\\xc7\\xb6','Ƕ',str(value))
    value = re.sub(r'\\xc7\\xb7','Ƿ',str(value))
    value = re.sub(r'\\xc7\\xb8','Ǹ',str(value))
    value = re.sub(r'\\xc7\\xb9','ǹ',str(value))
    value = re.sub(r'\\xc7\\xba','Ǻ',str(value))
    value = re.sub(r'\\xc7\\xbb','ǻ',str(value))
    value = re.sub(r'\\xc7\\xbc','Ǽ',str(value))
    value = re.sub(r'\\xc7\\xbd','ǽ',str(value))
    value = re.sub(r'\\xc7\\xbe','Ǿ',str(value))
    value = re.sub(r'\\xc7\\xbf','ǿ',str(value))
    value = re.sub(r'\\xd0\\x80','Ѐ',str(value))
    value = re.sub(r'\\xd0\\x81','Ё',str(value))
    value = re.sub(r'\\xd0\\x82','Ђ',str(value))
    value = re.sub(r'\\xd0\\x83','Ѓ',str(value))
    value = re.sub(r'\\xd0\\x84','Є',str(value))
    value = re.sub(r'\\xd0\\x85','Ѕ',str(value))
    value = re.sub(r'\\xd0\\x86','І',str(value))
    value = re.sub(r'\\xd0\\x87','Ї',str(value))
    value = re.sub(r'\\xd0\\x88','Ј',str(value))
    value = re.sub(r'\\xd0\\x89','Љ',str(value))
    value = re.sub(r'\\xd0\\x8a','Њ',str(value))
    value = re.sub(r'\\xd0\\x8b','Ћ',str(value))
    value = re.sub(r'\\xd0\\x8c','Ќ',str(value))
    value = re.sub(r'\\xd0\\x8d','Ѝ',str(value))
    value = re.sub(r'\\xd0\\x8e','Ў',str(value))
    value = re.sub(r'\\xd0\\x8f','Џ',str(value))
    value = re.sub(r'\\xd0\\x90','А',str(value))
    value = re.sub(r'\\xd0\\x91','Б',str(value))
    value = re.sub(r'\\xd0\\x92','В',str(value))
    value = re.sub(r'\\xd0\\x93','Г',str(value))
    value = re.sub(r'\\xd0\\x94','Д',str(value))
    value = re.sub(r'\\xd0\\x95','Е',str(value))
    value = re.sub(r'\\xd0\\x96','Ж',str(value))
    value = re.sub(r'\\xd0\\x97','З',str(value))
    value = re.sub(r'\\xd0\\x98','И',str(value))
    value = re.sub(r'\\xd0\\x99','Й',str(value))
    value = re.sub(r'\\xd0\\x9a','К',str(value))
    value = re.sub(r'\\xd0\\x9b','Л',str(value))
    value = re.sub(r'\\xd0\\x9c','М',str(value))
    value = re.sub(r'\\xd0\\x9d','Н',str(value))
    value = re.sub(r'\\xd0\\x9e','О',str(value))
    value = re.sub(r'\\xd0\\x9f','П',str(value))
    value = re.sub(r'\\xd0\\xa0','Р',str(value))
    value = re.sub(r'\\xd0\\xa1','С',str(value))
    value = re.sub(r'\\xd0\\xa2','Т',str(value))
    value = re.sub(r'\\xd0\\xa3','У',str(value))
    value = re.sub(r'\\xd0\\xa4','Ф',str(value))
    value = re.sub(r'\\xd0\\xa5','Х',str(value))
    value = re.sub(r'\\xd0\\xa6','Ц',str(value))
    value = re.sub(r'\\xd0\\xa7','Ч',str(value))
    value = re.sub(r'\\xd0\\xa8','Ш',str(value))
    value = re.sub(r'\\xd0\\xa9','Щ',str(value))
    value = re.sub(r'\\xd0\\xaa','Ъ',str(value))
    value = re.sub(r'\\xd0\\xab','Ы',str(value))
    value = re.sub(r'\\xd0\\xac','Ь',str(value))
    value = re.sub(r'\\xd0\\xad','Э',str(value))
    value = re.sub(r'\\xd0\\xae','Ю',str(value))
    value = re.sub(r'\\xd0\\xaf','Я',str(value))
    value = re.sub(r'\\xd0\\xb0','а',str(value))
    value = re.sub(r'\\xd0\\xb1','б',str(value))
    value = re.sub(r'\\xd0\\xb2','в',str(value))
    value = re.sub(r'\\xd0\\xb3','г',str(value))
    value = re.sub(r'\\xd0\\xb4','д',str(value))
    value = re.sub(r'\\xd0\\xb5','е',str(value))
    value = re.sub(r'\\xd0\\xb6','ж',str(value))
    value = re.sub(r'\\xd0\\xb7','з',str(value))
    value = re.sub(r'\\xd0\\xb8','и',str(value))
    value = re.sub(r'\\xd0\\xb9','й',str(value))
    value = re.sub(r'\\xd0\\xba','к',str(value))
    value = re.sub(r'\\xd0\\xbb','л',str(value))
    value = re.sub(r'\\xd0\\xbc','м',str(value))
    value = re.sub(r'\\xd0\\xbd','н',str(value))
    value = re.sub(r'\\xd0\\xbe','о',str(value))
    value = re.sub(r'\\xd0\\xbf','п',str(value))
    value = re.sub(r'\\xd1\\x80','р',str(value))
    value = re.sub(r'\\xd1\\x81','с',str(value))
    value = re.sub(r'\\xd1\\x82','т',str(value))
    value = re.sub(r'\\xd1\\x83','у',str(value))
    value = re.sub(r'\\xd1\\x84','ф',str(value))
    value = re.sub(r'\\xd1\\x85','х',str(value))
    value = re.sub(r'\\xd1\\x86','ц',str(value))
    value = re.sub(r'\\xd1\\x87','ч',str(value))
    value = re.sub(r'\\xd1\\x88','ш',str(value))
    value = re.sub(r'\\xd1\\x89','щ',str(value))
    value = re.sub(r'\\xd1\\x8a','ъ',str(value))
    value = re.sub(r'\\xd1\\x8b','ы',str(value))
    value = re.sub(r'\\xd1\\x8c','ь',str(value))
    value = re.sub(r'\\xd1\\x8d','э',str(value))
    value = re.sub(r'\\xd1\\x8e','ю',str(value))
    value = re.sub(r'\\xd1\\x8f','я',str(value))
    value = re.sub(r'\\xd1\\x90','ѐ',str(value))
    value = re.sub(r'\\xd1\\x91','ё',str(value))
    value = re.sub(r'\\xd1\\x92','ђ',str(value))
    value = re.sub(r'\\xd1\\x93','ѓ',str(value))
    value = re.sub(r'\\xd1\\x94','є',str(value))
    value = re.sub(r'\\xd1\\x95','ѕ',str(value))
    value = re.sub(r'\\xd1\\x96','і',str(value))
    value = re.sub(r'\\xd1\\x97','ї',str(value))
    value = re.sub(r'\\xd1\\x98','ј',str(value))
    value = re.sub(r'\\xd1\\x99','љ',str(value))
    value = re.sub(r'\\xd1\\x9a','њ',str(value))
    value = re.sub(r'\\xd1\\x9b','ћ',str(value))
    value = re.sub(r'\\xd1\\x9c','ќ',str(value))
    value = re.sub(r'\\xd1\\x9d','ѝ',str(value))
    value = re.sub(r'\\xd1\\x9e','ў',str(value))
    value = re.sub(r'\\xd1\\x9f','џ',str(value))
    value = re.sub(r'\\xd1\\xa0','Ѡ',str(value))
    value = re.sub(r'\\xd1\\xa1','ѡ',str(value))
    value = re.sub(r'\\xd1\\xa2','Ѣ',str(value))
    value = re.sub(r'\\xd1\\xa3','ѣ',str(value))
    value = re.sub(r'\\xd1\\xa4','Ѥ',str(value))
    value = re.sub(r'\\xd1\\xa5','ѥ',str(value))
    value = re.sub(r'\\xd1\\xa6','Ѧ',str(value))
    value = re.sub(r'\\xd1\\xa7','ѧ',str(value))
    value = re.sub(r'\\xd1\\xa8','Ѩ',str(value))
    value = re.sub(r'\\xd1\\xa9','ѩ',str(value))
    value = re.sub(r'\\xd1\\xaa','Ѫ',str(value))
    value = re.sub(r'\\xd1\\xab','ѫ',str(value))
    value = re.sub(r'\\xd1\\xac','Ѭ',str(value))
    value = re.sub(r'\\xd1\\xad','ѭ',str(value))
    value = re.sub(r'\\xd1\\xae','Ѯ',str(value))
    value = re.sub(r'\\xd1\\xaf','ѯ',str(value))
    value = re.sub(r'\\xd1\\xb0','Ѱ',str(value))
    value = re.sub(r'\\xd1\\xb1','ѱ',str(value))
    value = re.sub(r'\\xd1\\xb2','Ѳ',str(value))
    value = re.sub(r'\\xd1\\xb3','ѳ',str(value))
    value = re.sub(r'\\xd1\\xb4','Ѵ',str(value))
    value = re.sub(r'\\xd1\\xb5','ѵ',str(value))
    value = re.sub(r'\\xd1\\xb6','Ѷ',str(value))
    value = re.sub(r'\\xd1\\xb7','ѷ',str(value))
    value = re.sub(r'\\xd1\\xb8','Ѹ',str(value))
    value = re.sub(r'\\xd1\\xb9','ѹ',str(value))
    value = re.sub(r'\\xd1\\xba','Ѻ',str(value))
    value = re.sub(r'\\xd1\\xbb','ѻ',str(value))
    value = re.sub(r'\\xd1\\xbc','Ѽ',str(value))
    value = re.sub(r'\\xd1\\xbd','ѽ',str(value))
    value = re.sub(r'\\xd1\\xbe','Ѿ',str(value))
    value = re.sub(r'\\xd1\\xbf','ѿ',str(value))
    value = re.sub(r'\&iexcl\;','¡',str(value))
    value = re.sub(r'\&cent\;','¢',str(value))
    value = re.sub(r'\&pound\;','£',str(value))
    value = re.sub(r'\&curren\;','¤',str(value))
    value = re.sub(r'\&yen\;','¥',str(value))
    value = re.sub(r'\&brvbar\;','¦',str(value))
    value = re.sub(r'\&sect\;','§',str(value))
    value = re.sub(r'\&uml\;','¨',str(value))
    value = re.sub(r'\&copy\;','©',str(value))
    value = re.sub(r'\&ordf\;','ª',str(value))
    value = re.sub(r'\&laquo\;','«',str(value))
    value = re.sub(r'\&not\;','¬',str(value))
    value = re.sub(r'\&shy\;','',str(value))
    value = re.sub(r'\&reg\;','®',str(value))
    value = re.sub(r'\&macr\;','¯',str(value))
    value = re.sub(r'\&deg\;','°',str(value))
    value = re.sub(r'\&plusmn\;','±',str(value))
    value = re.sub(r'\&sup2\;','²',str(value))
    value = re.sub(r'\&sup3\;','³',str(value))
    value = re.sub(r'\&acute\;','´',str(value))
    value = re.sub(r'\&micro\;','µ',str(value))
    value = re.sub(r'\&para\;','¶',str(value))
    value = re.sub(r'\&middot\;','·',str(value))
    value = re.sub(r'\&cedil\;','¸',str(value))
    value = re.sub(r'\&sup1\;','¹',str(value))
    value = re.sub(r'\&ordm\;','º',str(value))
    value = re.sub(r'\&raquo\;','»',str(value))
    value = re.sub(r'\&frac14\;','¼',str(value))
    value = re.sub(r'\&frac12\;','½',str(value))
    value = re.sub(r'\&frac34\;','¾',str(value))
    value = re.sub(r'\&iquest\;','¿',str(value))
    value = re.sub(r'\&Agrave\;','À',str(value))
    value = re.sub(r'\&Aacute\;','Á',str(value))
    value = re.sub(r'\&Acirc\;','Â',str(value))
    value = re.sub(r'\&Atilde\;','Ã',str(value))
    value = re.sub(r'\&Auml\;','Ä',str(value))
    value = re.sub(r'\&Aring\;','Å',str(value))
    value = re.sub(r'\&AElig\;','Æ',str(value))
    value = re.sub(r'\&Ccedil\;','Ç',str(value))
    value = re.sub(r'\&Egrave\;','È',str(value))
    value = re.sub(r'\&Eacute\;','É',str(value))
    value = re.sub(r'\&Ecirc\;','Ê',str(value))
    value = re.sub(r'\&Euml\;','Ë',str(value))
    value = re.sub(r'\&Igrave\;','Ì',str(value))
    value = re.sub(r'\&Iacute\;','Í',str(value))
    value = re.sub(r'\&Icirc\;','Î',str(value))
    value = re.sub(r'\&Iuml\;','Ï',str(value))
    value = re.sub(r'\&ETH\;','Ð',str(value))
    value = re.sub(r'\&Ntilde\;','Ñ',str(value))
    value = re.sub(r'\&Ograve\;','Ò',str(value))
    value = re.sub(r'\&Oacute\;','Ó',str(value))
    value = re.sub(r'\&Ocirc\;','Ô',str(value))
    value = re.sub(r'\&Otilde\;','Õ',str(value))
    value = re.sub(r'\&Ouml\;','Ö',str(value))
    value = re.sub(r'\&times\;','×',str(value))
    value = re.sub(r'\&Oslash\;','Ø',str(value))
    value = re.sub(r'\&Ugrave\;','Ù',str(value))
    value = re.sub(r'\&Uacute\;','Ú',str(value))
    value = re.sub(r'\&Ucirc\;','Û',str(value))
    value = re.sub(r'\&Uuml\;','Ü',str(value))
    value = re.sub(r'\&Yacute\;','Ý',str(value))
    value = re.sub(r'\&THORN\;','Þ',str(value))
    value = re.sub(r'\&szlig\;','ß',str(value))
    value = re.sub(r'\&agrave\;','à',str(value))
    value = re.sub(r'\&aacute\;','á',str(value))
    value = re.sub(r'\&acirc\;','â',str(value))
    value = re.sub(r'\&atilde\;','ã',str(value))
    value = re.sub(r'\&auml\;','ä',str(value))
    value = re.sub(r'\&aring\;','å',str(value))
    value = re.sub(r'\&aelig\;','æ',str(value))
    value = re.sub(r'\&ccedil\;','ç',str(value))
    value = re.sub(r'\&egrave\;','è',str(value))
    value = re.sub(r'\&eacute\;','é',str(value))
    value = re.sub(r'\&ecirc\;','ê',str(value))
    value = re.sub(r'\&euml\;','ë',str(value))
    value = re.sub(r'\&igrave\;','ì',str(value))
    value = re.sub(r'\&iacute\;','í',str(value))
    value = re.sub(r'\&icirc\;','î',str(value))
    value = re.sub(r'\&iuml\;','ï',str(value))
    value = re.sub(r'\&eth\;','ð',str(value))
    value = re.sub(r'\&ntilde\;','ñ',str(value))
    value = re.sub(r'\&ograve\;','ò',str(value))
    value = re.sub(r'\&oacute\;','ó',str(value))
    value = re.sub(r'\&ocirc\;','ô',str(value))
    value = re.sub(r'\&otilde\;','õ',str(value))
    value = re.sub(r'\&ouml\;','ö',str(value))
    value = re.sub(r'\&divide\;','÷',str(value))
    value = re.sub(r'\&oslash\;','ø',str(value))
    value = re.sub(r'\&ugrave\;','ù',str(value))
    value = re.sub(r'\&uacute\;','ú',str(value))
    value = re.sub(r'\&ucirc\;','û',str(value))
    value = re.sub(r'\&uuml\;','ü',str(value))
    value = re.sub(r'\&yacute\;','ý',str(value))
    value = re.sub(r'\&thorn\;','þ',str(value))
    value = re.sub(r'\&yuml\;','ÿ',str(value))


    return value
def html_encode(value):
#     print "Before",value &#336;
    value = re.sub(r'\&amp\;',r'&',str(value))
    value = re.sub(r'\&([A-Za-z]+\;)',r'\1',str(value))
    value = re.sub(r'\&([0-9\W]+\;)',r'\1',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Aacute;','A',str(value))
    value = re.sub(r'Agrave;','A',str(value))
    value = re.sub(r'Agrave;','A',str(value))
    value = re.sub(r'Agrave;','A',str(value))
    value = re.sub(r'Agrave;','A',str(value))
    value = re.sub(r'Agrave;','A',str(value))
    value = re.sub(r'Acirc;','A',str(value))
    value = re.sub(r'Acirc;','A',str(value))
    value = re.sub(r'Acirc;','A',str(value))
    value = re.sub(r'Acirc;','A',str(value))
    value = re.sub(r'Acirc;','A',str(value))
    value = re.sub(r'Auml;','A',str(value))
    value = re.sub(r'Auml;','A',str(value))
    value = re.sub(r'Auml;','A',str(value))
    value = re.sub(r'Auml;','A',str(value))
    value = re.sub(r'Auml;','A',str(value))
    value = re.sub(r'#258;','A',str(value))
    value = re.sub(r'#256;','A',str(value))
    value = re.sub(r'Atilde;','A',str(value))
    value = re.sub(r'Atilde;','A',str(value))
    value = re.sub(r'Aring;','A',str(value))
    value = re.sub(r'Aring;','A',str(value))
    value = re.sub(r'Aring;','A',str(value))
    value = re.sub(r'#260;','A',str(value))
    value = re.sub(r'AElig;','Æ',str(value))
    value = re.sub(r'AElig;','Æ',str(value))
    value = re.sub(r'AElig;','Æ',str(value))
    value = re.sub(r'AElig;','Æ',str(value))
    value = re.sub(r'#262;','C',str(value))
    value = re.sub(r'#262;','C',str(value))
    value = re.sub(r'#262;','C',str(value))
    value = re.sub(r'#264;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'#268;','C',str(value))
    value = re.sub(r'Ccedil;','C',str(value))
    value = re.sub(r'Ccedil;','C',str(value))
    value = re.sub(r'Ccedil;','C',str(value))
    value = re.sub(r'Ccedil;','C',str(value))
    value = re.sub(r'Ccedil;','C',str(value))
    value = re.sub(r'#270;','D',str(value))
    value = re.sub(r'#270;','D',str(value))
    value = re.sub(r'#272;','D',str(value))
    value = re.sub(r'#272;','D',str(value))
    value = re.sub(r'#272;','D',str(value))
    value = re.sub(r'ETH;','D',str(value))
    value = re.sub(r'ETH;','D',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Eacute;','E',str(value))
    value = re.sub(r'Egrave;','E',str(value))
    value = re.sub(r'Egrave;','E',str(value))
    value = re.sub(r'Egrave;','E',str(value))
    value = re.sub(r'Egrave;','E',str(value))
    value = re.sub(r'Egrave;','E',str(value))
    value = re.sub(r'Ecirc;','E',str(value))
    value = re.sub(r'Ecirc;','E',str(value))
    value = re.sub(r'Ecirc;','E',str(value))
    value = re.sub(r'Euml;','E',str(value))
    value = re.sub(r'Euml;','E',str(value))
    value = re.sub(r'Euml;','E',str(value))
    value = re.sub(r'#282;','E',str(value))
    value = re.sub(r'#274;','E',str(value))
    value = re.sub(r'#280;','E',str(value))
    value = re.sub(r'#284;','G',str(value))
    value = re.sub(r'#286;','G',str(value))
    value = re.sub(r'#290;','G',str(value))
    value = re.sub(r'#292;','H',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Iacute;','I',str(value))
    value = re.sub(r'Igrave;','I',str(value))
    value = re.sub(r'Igrave;','I',str(value))
    value = re.sub(r'Igrave;','I',str(value))
    value = re.sub(r'#304;','I',str(value))
    value = re.sub(r'Icirc;','I',str(value))
    value = re.sub(r'Icirc;','I',str(value))
    value = re.sub(r'Icirc;','I',str(value))
    value = re.sub(r'Icirc;','I',str(value))
    value = re.sub(r'Iuml;','I',str(value))
    value = re.sub(r'Iuml;','I',str(value))
    value = re.sub(r'Iuml;','I',str(value))
    value = re.sub(r'Iuml;','I',str(value))
    value = re.sub(r'Iuml;','I',str(value))
    value = re.sub(r'#298;','I',str(value))
    value = re.sub(r'#296;','I',str(value))
    value = re.sub(r'#308;','J',str(value))
    value = re.sub(r'#310;','K',str(value))
    value = re.sub(r'#313;','L',str(value))
    value = re.sub(r'#317;','L',str(value))
    value = re.sub(r'#315;','L',str(value))
    value = re.sub(r'#321;','L',str(value))
    value = re.sub(r'#323;','N',str(value))
    value = re.sub(r'#327;','N',str(value))
    value = re.sub(r'#327;','N',str(value))
    value = re.sub(r'Ntilde;','N',str(value))
    value = re.sub(r'#325;','N',str(value))
    value = re.sub(r'#330;','N',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Oacute;','O',str(value))
    value = re.sub(r'Ograve;','O',str(value))
    value = re.sub(r'Ograve;','O',str(value))
    value = re.sub(r'Ograve;','O',str(value))
    value = re.sub(r'Ograve;','O',str(value))
    value = re.sub(r'Ocirc;','O',str(value))
    value = re.sub(r'Ocirc;','O',str(value))
    value = re.sub(r'Ocirc;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Ouml;','O',str(value))
    value = re.sub(r'Otilde;','O',str(value))
    value = re.sub(r'Otilde;','O',str(value))
    value = re.sub(r'#336;','O',str(value))
    value = re.sub(r'Oslash;','O',str(value))
    value = re.sub(r'Oslash;','O',str(value))
    value = re.sub(r'Oslash;','O',str(value))
    value = re.sub(r'OElig;','Œ',str(value))
    value = re.sub(r'#340;','R',str(value))
    value = re.sub(r'#344;','R',str(value))
    value = re.sub(r'#342;','R',str(value))
    value = re.sub(r'#346;','S',str(value))
    value = re.sub(r'#348;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#352;','S',str(value))
    value = re.sub(r'#350;','S',str(value))
    value = re.sub(r'#350;','S',str(value))
    value = re.sub(r'#356;','T',str(value))
    value = re.sub(r'#356;','T',str(value))
    value = re.sub(r'#354;','T',str(value))
    value = re.sub(r'THORN;','p',str(value))
    value = re.sub(r'#358;','T',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Uacute;','U',str(value))
    value = re.sub(r'Ugrave;','U',str(value))
    value = re.sub(r'Ugrave;','U',str(value))
    value = re.sub(r'Ugrave;','U',str(value))
    value = re.sub(r'Ugrave;','U',str(value))
    value = re.sub(r'Ucirc;','U',str(value))
    value = re.sub(r'Ucirc;','U',str(value))
    value = re.sub(r'Ucirc;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'Uuml;','U',str(value))
    value = re.sub(r'#364;','U',str(value))
    value = re.sub(r'#362;','U',str(value))
    value = re.sub(r'#360;','U',str(value))
    value = re.sub(r'#366;','U',str(value))
    value = re.sub(r'#368;','U',str(value))
    value = re.sub(r'Yacute;','Y',str(value))
    value = re.sub(r'Yacute;','Y',str(value))
    value = re.sub(r'Yacute;','Y',str(value))
    value = re.sub(r'Yacute;','Y',str(value))
    value = re.sub(r'#376;','Y',str(value))
    value = re.sub(r'#377;','Z',str(value))
    value = re.sub(r'#379;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'#381;','Z',str(value))
    value = re.sub(r'ordf;','a',str(value))
    value = re.sub(r'ordm;','o',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'aacute;','a',str(value))
    value = re.sub(r'agrave;','a',str(value))
    value = re.sub(r'agrave;','a',str(value))
    value = re.sub(r'agrave;','a',str(value))
    value = re.sub(r'agrave;','a',str(value))
    value = re.sub(r'agrave;','a',str(value))
    value = re.sub(r'acirc;','a',str(value))
    value = re.sub(r'acirc;','a',str(value))
    value = re.sub(r'acirc;','a',str(value))
    value = re.sub(r'acirc;','a',str(value))
    value = re.sub(r'acirc;','a',str(value))
    value = re.sub(r'auml;','a',str(value))
    value = re.sub(r'auml;','a',str(value))
    value = re.sub(r'auml;','a',str(value))
    value = re.sub(r'auml;','a',str(value))
    value = re.sub(r'auml;','a',str(value))
    value = re.sub(r'#259;','a',str(value))
    value = re.sub(r'#257;','a',str(value))
    value = re.sub(r'atilde;','a',str(value))
    value = re.sub(r'atilde;','a',str(value))
    value = re.sub(r'aring;','a',str(value))
    value = re.sub(r'aring;','a',str(value))
    value = re.sub(r'aring;','a',str(value))
    value = re.sub(r'#261;','a',str(value))
    value = re.sub(r'aelig;','æ',str(value))
    value = re.sub(r'aelig;','æ',str(value))
    value = re.sub(r'aelig;','æ',str(value))
    value = re.sub(r'aelig;','æ',str(value))
    value = re.sub(r'#263;','c',str(value))
    value = re.sub(r'#263;','c',str(value))
    value = re.sub(r'#263;','c',str(value))
    value = re.sub(r'#265;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'#269;','c',str(value))
    value = re.sub(r'ccedil;','c',str(value))
    value = re.sub(r'ccedil;','c',str(value))
    value = re.sub(r'ccedil;','c',str(value))
    value = re.sub(r'ccedil;','c',str(value))
    value = re.sub(r'ccedil;','c',str(value))
    value = re.sub(r'#271;','d',str(value))
    value = re.sub(r'#271;','d',str(value))
    value = re.sub(r'#273;','d',str(value))
    value = re.sub(r'#273;','d',str(value))
    value = re.sub(r'#273;','d',str(value))
    value = re.sub(r'eth;','d',str(value))
    value = re.sub(r'eth;','d',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'eacute;','e',str(value))
    value = re.sub(r'egrave;','e',str(value))
    value = re.sub(r'egrave;','e',str(value))
    value = re.sub(r'egrave;','e',str(value))
    value = re.sub(r'egrave;','e',str(value))
    value = re.sub(r'egrave;','e',str(value))
    value = re.sub(r'ecirc;','e',str(value))
    value = re.sub(r'ecirc;','e',str(value))
    value = re.sub(r'ecirc;','e',str(value))
    value = re.sub(r'euml;','e',str(value))
    value = re.sub(r'euml;','e',str(value))
    value = re.sub(r'euml;','e',str(value))
    value = re.sub(r'#283;','e',str(value))
    value = re.sub(r'#275;','e',str(value))
    value = re.sub(r'#281;','e',str(value))
    value = re.sub(r'#285;','g',str(value))
    value = re.sub(r'#287;','g',str(value))
    value = re.sub(r'#291;','g',str(value))
    value = re.sub(r'#293;','h',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'iacute;','i',str(value))
    value = re.sub(r'igrave;','i',str(value))
    value = re.sub(r'igrave;','i',str(value))
    value = re.sub(r'igrave;','i',str(value))
    value = re.sub(r'#305;','i',str(value))
    value = re.sub(r'icirc;','i',str(value))
    value = re.sub(r'icirc;','i',str(value))
    value = re.sub(r'icirc;','i',str(value))
    value = re.sub(r'icirc;','i',str(value))
    value = re.sub(r'iuml;','i',str(value))
    value = re.sub(r'iuml;','i',str(value))
    value = re.sub(r'iuml;','i',str(value))
    value = re.sub(r'iuml;','i',str(value))
    value = re.sub(r'iuml;','i',str(value))
    value = re.sub(r'#299;','i',str(value))
    value = re.sub(r'#297;','i',str(value))
    value = re.sub(r'#309;','j',str(value))
    value = re.sub(r'#311;','k',str(value))
    value = re.sub(r'#314;','l',str(value))
    value = re.sub(r'#318;','l',str(value))
    value = re.sub(r'#316;','l',str(value))
    value = re.sub(r'#322;','l',str(value))
    value = re.sub(r'#324;','n',str(value))
    value = re.sub(r'#328;','n',str(value))
    value = re.sub(r'#328;','n',str(value))
    value = re.sub(r'ntilde;','n',str(value))
    value = re.sub(r'#326;','n',str(value))
    value = re.sub(r'#331;','n',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'oacute;','o',str(value))
    value = re.sub(r'ograve;','o',str(value))
    value = re.sub(r'ograve;','o',str(value))
    value = re.sub(r'ograve;','o',str(value))
    value = re.sub(r'ograve;','o',str(value))
    value = re.sub(r'ocirc;','o',str(value))
    value = re.sub(r'ocirc;','o',str(value))
    value = re.sub(r'ocirc;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'uml;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'ouml;','o',str(value))
    value = re.sub(r'otilde;','o',str(value))
    value = re.sub(r'otilde;','o',str(value))
    value = re.sub(r'#337;','o',str(value))
    value = re.sub(r'oslash;','o',str(value))
    value = re.sub(r'oslash;','o',str(value))
    value = re.sub(r'oslash;','o',str(value))
    value = re.sub(r'oelig;','œ',str(value))
    value = re.sub(r'#341;','r',str(value))
    value = re.sub(r'#345;','r',str(value))
    value = re.sub(r'#343;','r',str(value))
    value = re.sub(r'#347;','s',str(value))
    value = re.sub(r'#349;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#353;','s',str(value))
    value = re.sub(r'#351;','s',str(value))
    value = re.sub(r'#351;','s',str(value))
    value = re.sub(r'#357;','t',str(value))
    value = re.sub(r'#357;','t',str(value))
    value = re.sub(r'#355;','t',str(value))
    value = re.sub(r'thorn;','p',str(value))
    value = re.sub(r'#359;','t',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'ugrave;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'uacute;','u',str(value))
    value = re.sub(r'ugrave;','u',str(value))
    value = re.sub(r'ugrave;','u',str(value))
    value = re.sub(r'ugrave;','u',str(value))
    value = re.sub(r'ugrave;','u',str(value))
    value = re.sub(r'ucirc;','u',str(value))
    value = re.sub(r'ucirc;','u',str(value))
    value = re.sub(r'ucirc;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'uuml;','u',str(value))
    value = re.sub(r'#365;','u',str(value))
    value = re.sub(r'#363;','u',str(value))
    value = re.sub(r'#361;','u',str(value))
    value = re.sub(r'#367;','u',str(value))
    value = re.sub(r'#369;','u',str(value))
    value = re.sub(r'yacute;','y',str(value))
    value = re.sub(r'yacute;','y',str(value))
    value = re.sub(r'yacute;','y',str(value))
    value = re.sub(r'yacute;','y',str(value))
    value = re.sub(r'yuml;','y',str(value))
    value = re.sub(r'#378;','z',str(value))
    value = re.sub(r'#380;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#382;','z',str(value))
    value = re.sub(r'#312;','k',str(value))
    value = re.sub(r'ordf;','a',str(value))
    value = re.sub(r'ordm;','o',str(value))
    value = re.sub(r'&#336;','O',str(value))
    value = re.sub(r'#337;','o',str(value))
    value = re.sub(r'À','A',str(value))
    value = re.sub(r'Á','A',str(value))
    value = re.sub(r'Â','A',str(value))
    value = re.sub(r'Ã','A',str(value))
    value = re.sub(r'Ä','A',str(value))
    value = re.sub(r'Å','A',str(value))
    value = re.sub(r'Æ','AE',str(value))
    value = re.sub(r'Ç','C',str(value))
    value = re.sub(r'È','E',str(value))
    value = re.sub(r'É','E',str(value))
    value = re.sub(r'Ê','E',str(value))
    value = re.sub(r'Ë','E',str(value))
    value = re.sub(r'Ì','I',str(value))
    value = re.sub(r'Í','I',str(value))
    value = re.sub(r'Î','I',str(value))
    value = re.sub(r'Ï','I',str(value))
    value = re.sub(r'Ð','D',str(value))
    value = re.sub(r'Ñ','N',str(value))
    value = re.sub(r'Ò','O',str(value))
    value = re.sub(r'Ó','O',str(value))
    value = re.sub(r'Ô','O',str(value))
    value = re.sub(r'Õ','O',str(value))
    value = re.sub(r'Ö','O',str(value))
    value = re.sub(r'Ø','O',str(value))
    value = re.sub(r'Ù','U',str(value))
    value = re.sub(r'Ú','U',str(value))
    value = re.sub(r'Û','U',str(value))
    value = re.sub(r'Ü','U',str(value))
    value = re.sub(r'Ý','Y',str(value))
    value = re.sub(r'Þ','DE',str(value))
    value = re.sub(r'ß','S',str(value))
    value = re.sub(r'à','a',str(value))
    value = re.sub(r'á','a',str(value))
    value = re.sub(r'â','a',str(value))
    value = re.sub(r'ã','a',str(value))
    value = re.sub(r'ä','a',str(value))
    value = re.sub(r'å','a',str(value))
    value = re.sub(r'æ','ae',str(value))
    value = re.sub(r'ç','c',str(value))
    value = re.sub(r'ç','c',str(value))
    value = re.sub(r'è','e',str(value))
    value = re.sub(r'é','e',str(value))
    value = re.sub(r'ê','e',str(value))
    value = re.sub(r'ë','e',str(value))
    value = re.sub(r'ì','i',str(value))
    value = re.sub(r'í','i',str(value))
    value = re.sub(r'î','i',str(value))
    value = re.sub(r'ï','i',str(value))
    value = re.sub(r'ð','o',str(value))
    value = re.sub(r'ñ','n',str(value))
    value = re.sub(r'ò','o',str(value))
    value = re.sub(r'ó','o',str(value))
    value = re.sub(r'ô','o',str(value))
    value = re.sub(r'õ','o',str(value))
    value = re.sub(r'ö','o',str(value))
    value = re.sub(r'ø','o',str(value))
    value = re.sub(r'ù','u',str(value))
    value = re.sub(r'ú','u',str(value))
    value = re.sub(r'û','u',str(value))
    value = re.sub(r'ü','u',str(value))
    value = re.sub(r'ý','y',str(value))
    value = re.sub(r'þ','fe',str(value))
    value = re.sub(r'ÿ','y',str(value))
    value = re.sub(r'Ā','A',str(value))
    value = re.sub(r'ā','a',str(value))
    value = re.sub(r'Ă','A',str(value))
    value = re.sub(r'ă','a',str(value))
    value = re.sub(r'Ą','A',str(value))
    value = re.sub(r'ą','a',str(value))
    value = re.sub(r'Ć','C',str(value))
    value = re.sub(r'ć','c',str(value))
    value = re.sub(r'Ĉ','C',str(value))
    value = re.sub(r'ĉ','c',str(value))
    value = re.sub(r'Ċ','C',str(value))
    value = re.sub(r'ċ','c',str(value))
    value = re.sub(r'Č','C',str(value))
    value = re.sub(r'č','c',str(value))
    value = re.sub(r'Ď','D',str(value))
    value = re.sub(r'ď','d',str(value))
    value = re.sub(r'Đ','D',str(value))
    value = re.sub(r'đ','d',str(value))
    value = re.sub(r'Ē','E',str(value))
    value = re.sub(r'ē','e',str(value))
    value = re.sub(r'Ĕ','E',str(value))
    value = re.sub(r'ĕ','e',str(value))
    value = re.sub(r'Ė','E',str(value))
    value = re.sub(r'ė','e',str(value))
    value = re.sub(r'Ę','E',str(value))
    value = re.sub(r'ę','e',str(value))
    value = re.sub(r'Ě','E',str(value))
    value = re.sub(r'ě','e',str(value))
    value = re.sub(r'Ĝ','G',str(value))
    value = re.sub(r'ĝ','g',str(value))
    value = re.sub(r'Ğ','G',str(value))
    value = re.sub(r'ğ','g',str(value))
    value = re.sub(r'Ġ','G',str(value))
    value = re.sub(r'ġ','g',str(value))
    value = re.sub(r'Ģ','G',str(value))
    value = re.sub(r'ģ','g',str(value))
    value = re.sub(r'Ĥ','H',str(value))
    value = re.sub(r'ĥ','h',str(value))
    value = re.sub(r'Ħ','H',str(value))
    value = re.sub(r'ħ','h',str(value))
    value = re.sub(r'Ĩ','I',str(value))
    value = re.sub(r'ĩ','i',str(value))
    value = re.sub(r'Ī','I',str(value))
    value = re.sub(r'ī','i',str(value))
    value = re.sub(r'Ĭ','I',str(value))
    value = re.sub(r'ĭ','i',str(value))
    value = re.sub(r'Į','I',str(value))
    value = re.sub(r'į','i',str(value))
    value = re.sub(r'İ','I',str(value))
    value = re.sub(r'ı','i',str(value))
    value = re.sub(r'Ĳ','IJ',str(value))
    value = re.sub(r'ĳ','ij',str(value))
    value = re.sub(r'Ĵ','J',str(value))
    value = re.sub(r'ĵ','j',str(value))
    value = re.sub(r'Ķ','K',str(value))
    value = re.sub(r'ķ','k',str(value))
    value = re.sub(r'ĸ','k',str(value))
    value = re.sub(r'Ĺ','L',str(value))
    value = re.sub(r'ĺ','l',str(value))
    value = re.sub(r'Ļ','L',str(value))
    value = re.sub(r'ļ','l',str(value))
    value = re.sub(r'Ľ','L',str(value))
    value = re.sub(r'ľ','l',str(value))
    value = re.sub(r'Ŀ','L',str(value))
    value = re.sub(r'ŀ','l',str(value))
    value = re.sub(r'Ł','L',str(value))
    value = re.sub(r'ł','l',str(value))
    value = re.sub(r'Ń','N',str(value))
    value = re.sub(r'ń','n',str(value))
    value = re.sub(r'Ņ','N',str(value))
    value = re.sub(r'ņ','n',str(value))
    value = re.sub(r'Ň','N',str(value))
    value = re.sub(r'ň','n',str(value))
    value = re.sub(r'ŉ','n',str(value))
    value = re.sub(r'Ŋ','n',str(value))
    value = re.sub(r'ŋ','n',str(value))
    value = re.sub(r'Ō','O',str(value))
    value = re.sub(r'ō','o',str(value))
    value = re.sub(r'Ŏ','O',str(value))
    value = re.sub(r'ŏ','o',str(value))
    value = re.sub(r'Ő','O',str(value))
    value = re.sub(r'ő','o',str(value))
    value = re.sub(r'Œ','OE',str(value))
    value = re.sub(r'œ','oe',str(value))
    value = re.sub(r'Ŕ','R',str(value))
    value = re.sub(r'ŕ','r',str(value))
    value = re.sub(r'Ŗ','R',str(value))
    value = re.sub(r'ŗ','r',str(value))
    value = re.sub(r'Ř','R',str(value))
    value = re.sub(r'ř','r',str(value))
    value = re.sub(r'Ś','S',str(value))
    value = re.sub(r'ś','s',str(value))
    value = re.sub(r'Ŝ','S',str(value))
    value = re.sub(r'ŝ','s',str(value))
    value = re.sub(r'Ş','S',str(value))
    value = re.sub(r'ş','s',str(value))
    value = re.sub(r'Š','S',str(value))
    value = re.sub(r'š','s',str(value))
    value = re.sub(r'Ţ','T',str(value))
    value = re.sub(r'ţ','t',str(value))
    value = re.sub(r'Ť','T',str(value))
    value = re.sub(r'ť','t',str(value))
    value = re.sub(r'Ŧ','T',str(value))
    value = re.sub(r'ŧ','t',str(value))
    value = re.sub(r'Ũ','U',str(value))
    value = re.sub(r'ũ','u',str(value))
    value = re.sub(r'Ū','U',str(value))
    value = re.sub(r'ū','u',str(value))
    value = re.sub(r'Ŭ','U',str(value))
    value = re.sub(r'ŭ','u',str(value))
    value = re.sub(r'Ů','U',str(value))
    value = re.sub(r'ů','u',str(value))
    value = re.sub(r'Ű','U',str(value))
    value = re.sub(r'ű','u',str(value))
    value = re.sub(r'Ų','U',str(value))
    value = re.sub(r'ų','u',str(value))
    value = re.sub(r'Ŵ','W',str(value))
    value = re.sub(r'ŵ','w',str(value))
    value = re.sub(r'Ŷ','Y',str(value))
    value = re.sub(r'ŷ','y',str(value))
    value = re.sub(r'Ÿ','Y',str(value))
    value = re.sub(r'Ź','Z',str(value))
    value = re.sub(r'ź','z',str(value))
    value = re.sub(r'Ż','Z',str(value))
    value = re.sub(r'ż','z',str(value))
    value = re.sub(r'Ž','Z',str(value))
    value = re.sub(r'ž','z',str(value))
    value = re.sub(r'ſ','S',str(value))
    value = re.sub(r'ƀ','b',str(value))
    value = re.sub(r'Ɓ','B',str(value))
    value = re.sub(r'Ƃ','b',str(value))
    value = re.sub(r'ƃ','b',str(value))
    value = re.sub(r'Ƅ','b',str(value))
    value = re.sub(r'ƅ','b',str(value))
    value = re.sub(r'Ɔ','O',str(value))
    value = re.sub(r'Ƈ','C',str(value))
    value = re.sub(r'ƈ','c',str(value))
    value = re.sub(r'Ɖ','D',str(value))
    value = re.sub(r'Ɗ','D',str(value))
    value = re.sub(r'Ƌ','D',str(value))
    value = re.sub(r'ƌ','d',str(value))
    value = re.sub(r'ƍ','ƍ',str(value))
    value = re.sub(r'Ǝ','E',str(value))
    value = re.sub(r'Ə','e',str(value))
    value = re.sub(r'Ɛ','E',str(value))
    value = re.sub(r'Ƒ','F',str(value))
    value = re.sub(r'ƒ','f',str(value))
    value = re.sub(r'Ɠ','G',str(value))
    value = re.sub(r'Ɣ','Ɣ',str(value))
    value = re.sub(r'ƕ','h',str(value))
    value = re.sub(r'Ɩ','l',str(value))
    value = re.sub(r'Ɨ','i',str(value))
    value = re.sub(r'Ƙ','K',str(value))
    value = re.sub(r'ƙ','k',str(value))
    value = re.sub(r'ƚ','I',str(value))
    value = re.sub(r'ƛ','ƛ',str(value))
    value = re.sub(r'Ɯ','W',str(value))
    value = re.sub(r'Ɲ','N',str(value))
    value = re.sub(r'ƞ','n',str(value))
    value = re.sub(r'Ɵ','O',str(value))
    value = re.sub(r'Ơ','O',str(value))
    value = re.sub(r'ơ','o',str(value))
    value = re.sub(r'Ƣ','Ƣ',str(value))
    value = re.sub(r'ƣ','ƣ',str(value))
    value = re.sub(r'Ƥ','P',str(value))
    value = re.sub(r'ƥ','p',str(value))
    value = re.sub(r'Ʀ','R',str(value))
    value = re.sub(r'Ƨ','S',str(value))
    value = re.sub(r'ƨ','s',str(value))
    value = re.sub(r'Ʃ','Ʃ',str(value))
    value = re.sub(r'ƪ','ƪ',str(value))
    value = re.sub(r'ƫ','t',str(value))
    value = re.sub(r'Ƭ','T',str(value))
    value = re.sub(r'ƭ','t',str(value))
    value = re.sub(r'Ʈ','T',str(value))
    value = re.sub(r'Ư','U',str(value))
    value = re.sub(r'ư','u',str(value))
    value = re.sub(r'Ʊ','Ʊ',str(value))
    value = re.sub(r'Ʋ','U',str(value))
    value = re.sub(r'Ƴ','Y',str(value))
    value = re.sub(r'ƴ','y',str(value))
    value = re.sub(r'Ƶ','Z',str(value))
    value = re.sub(r'ƶ','z',str(value))
    value = re.sub(r'Ʒ','Ʒ',str(value))
    value = re.sub(r'Ƹ','Ƹ',str(value))
    value = re.sub(r'ƹ','ƹ',str(value))
    value = re.sub(r'ƺ','ƺ',str(value))
    value = re.sub(r'ƻ','ƻ',str(value))
    value = re.sub(r'Ƽ','Ƽ',str(value))
    value = re.sub(r'ƽ','ƽ',str(value))
    value = re.sub(r'ƾ','ƾ',str(value))
    value = re.sub(r'ƿ','ƿ',str(value))
    value = re.sub(r'ǀ','ǀ',str(value))
    value = re.sub(r'ǁ','ǁ',str(value))
    value = re.sub(r'ǂ','ǂ',str(value))
    value = re.sub(r'ǃ','ǃ',str(value))
    value = re.sub(r'Ǆ','DZ',str(value))
    value = re.sub(r'ǅ','Dz',str(value))
    value = re.sub(r'ǆ','dz',str(value))
    value = re.sub(r'Ǉ','LJ',str(value))
    value = re.sub(r'ǈ','Lj',str(value))
    value = re.sub(r'ǉ','lj',str(value))
    value = re.sub(r'Ǌ','NJ',str(value))
    value = re.sub(r'ǋ','Nj',str(value))
    value = re.sub(r'ǌ','nj',str(value))
    value = re.sub(r'Ǎ','A',str(value))
    value = re.sub(r'ǎ','a',str(value))
    value = re.sub(r'Ǐ','I',str(value))
    value = re.sub(r'ǐ','i',str(value))
    value = re.sub(r'Ǒ','O',str(value))
    value = re.sub(r'ǒ','o',str(value))
    value = re.sub(r'Ǔ','U',str(value))
    value = re.sub(r'ǔ','u',str(value))
    value = re.sub(r'Ǖ','U',str(value))
    value = re.sub(r'ǖ','u',str(value))
    value = re.sub(r'Ǘ','U',str(value))
    value = re.sub(r'ǘ','u',str(value))
    value = re.sub(r'Ǚ','U',str(value))
    value = re.sub(r'ǚ','u',str(value))
    value = re.sub(r'Ǜ','U',str(value))
    value = re.sub(r'ǜ','u',str(value))
    value = re.sub(r'ǝ','e',str(value))
    value = re.sub(r'Ǟ','A',str(value))
    value = re.sub(r'ǟ','a',str(value))
    value = re.sub(r'Ǡ','A',str(value))
    value = re.sub(r'ǡ','a',str(value))
    value = re.sub(r'Ǣ','AE',str(value))
    value = re.sub(r'ǣ','ae',str(value))
    value = re.sub(r'Ǥ','G',str(value))
    value = re.sub(r'ǥ','g',str(value))
    value = re.sub(r'Ǧ','G',str(value))
    value = re.sub(r'ǧ','g',str(value))
    value = re.sub(r'Ǩ','K',str(value))
    value = re.sub(r'ǩ','k',str(value))
    value = re.sub(r'Ǫ','Ǫ',str(value))
    value = re.sub(r'ǫ','ǫ',str(value))
    value = re.sub(r'Ǭ','Ǭ',str(value))
    value = re.sub(r'ǭ','ǭ',str(value))
    value = re.sub(r'Ǯ','EZH',str(value))
    value = re.sub(r'ǯ','ezh',str(value))
    value = re.sub(r'ǰ','j',str(value))
    value = re.sub(r'Ǳ','DZ',str(value))
    value = re.sub(r'ǲ','Dz',str(value))
    value = re.sub(r'ǳ','dz',str(value))
    value = re.sub(r'Ǵ','G',str(value))
    value = re.sub(r'ǵ','g',str(value))
    value = re.sub(r'Ƕ','HWAIR',str(value))
    value = re.sub(r'Ƿ','WYNN',str(value))
    value = re.sub(r'Ǹ','N',str(value))
    value = re.sub(r'ǹ','n',str(value))
    value = re.sub(r'Ǻ','A',str(value))
    value = re.sub(r'ǻ','a',str(value))
    value = re.sub(r'Ǽ','AE',str(value))
    value = re.sub(r'ǽ','ae',str(value))
    value = re.sub(r'Ǿ','O',str(value))
    value = re.sub(r'ǿ','o',str(value))
    value = re.sub(r'Ѐ','E',str(value))
    value = re.sub(r'Ё','E',str(value))
    value = re.sub(r'Ђ','h',str(value))
    value = re.sub(r'Ѓ','r',str(value))
    value = re.sub(r'Є','E',str(value))
    value = re.sub(r'Ѕ','S',str(value))
    value = re.sub(r'І','I',str(value))
    value = re.sub(r'Ї','i',str(value))
    value = re.sub(r'Ј','J',str(value))
    value = re.sub(r'Љ','Љ',str(value))
    value = re.sub(r'Њ','H',str(value))
    value = re.sub(r'Ћ','h',str(value))
    value = re.sub(r'Ќ','K',str(value))
    value = re.sub(r'Ѝ','N',str(value))
    value = re.sub(r'Ў','Y',str(value))
    value = re.sub(r'Џ','Џ',str(value))
    value = re.sub(r'А','A',str(value))
    value = re.sub(r'Б','b',str(value))
    value = re.sub(r'В','B',str(value))
    value = re.sub(r'Г','R',str(value))
    value = re.sub(r'Д','A',str(value))
    value = re.sub(r'Е','E',str(value))
    value = re.sub(r'Ж','Ж',str(value))
    value = re.sub(r'З','З',str(value))
    value = re.sub(r'И','N',str(value))
    value = re.sub(r'Й','N',str(value))
    value = re.sub(r'К','k',str(value))
    value = re.sub(r'Л','Л',str(value))
    value = re.sub(r'М','M',str(value))
    value = re.sub(r'Н','H',str(value))
    value = re.sub(r'О','O',str(value))
    value = re.sub(r'П','П',str(value))
    value = re.sub(r'Р','P',str(value))
    value = re.sub(r'С','C',str(value))
    value = re.sub(r'Т','T',str(value))
    value = re.sub(r'У','y',str(value))
    value = re.sub(r'Ф','Ф',str(value))
    value = re.sub(r'Х','X',str(value))
    value = re.sub(r'Ц','Ц',str(value))
    value = re.sub(r'Ч','Ч',str(value))
    value = re.sub(r'Ш','Ш',str(value))
    value = re.sub(r'Щ','Щ',str(value))
    value = re.sub(r'Ъ','b',str(value))
    value = re.sub(r'Ы','b',str(value))
    value = re.sub(r'Ь','b',str(value))
    value = re.sub(r'Э','Э',str(value))
    value = re.sub(r'Ю','Ю',str(value))
    value = re.sub(r'Я','R',str(value))
    value = re.sub(r'а','a',str(value))
    value = re.sub(r'б','б',str(value))
    value = re.sub(r'в','B',str(value))
    value = re.sub(r'г','r',str(value))
    value = re.sub(r'д','A',str(value))
    value = re.sub(r'е','e',str(value))
    value = re.sub(r'ж','ж',str(value))
    value = re.sub(r'з','з',str(value))
    value = re.sub(r'и','N',str(value))
    value = re.sub(r'й','N',str(value))
    value = re.sub(r'к','k',str(value))
    value = re.sub(r'л','л',str(value))
    value = re.sub(r'м','m',str(value))
    value = re.sub(r'н','H',str(value))
    value = re.sub(r'о','o',str(value))
    value = re.sub(r'п','n',str(value))
    value = re.sub(r'р','p',str(value))
    value = re.sub(r'с','c',str(value))
    value = re.sub(r'т','T',str(value))
    value = re.sub(r'у','y',str(value))
    value = re.sub(r'ф','o',str(value))
    value = re.sub(r'х','x',str(value))
    value = re.sub(r'ц','u',str(value))
    value = re.sub(r'ч','u',str(value))
    value = re.sub(r'ш','w',str(value))
    value = re.sub(r'щ','w',str(value))
    value = re.sub(r'ъ','b',str(value))
    value = re.sub(r'ы','b',str(value))
    value = re.sub(r'ь','b',str(value))
    value = re.sub(r'э','e',str(value))
    value = re.sub(r'ю','ю',str(value))
    value = re.sub(r'я','R',str(value))
    value = re.sub(r'ѐ','e',str(value))
    value = re.sub(r'ё','e',str(value))
    value = re.sub(r'ђ','n',str(value))
    value = re.sub(r'ѓ','r',str(value))
    value = re.sub(r'є','e',str(value))
    value = re.sub(r'ѕ','s',str(value))
    value = re.sub(r'і','i',str(value))
    value = re.sub(r'ї','i',str(value))
    value = re.sub(r'ј','j',str(value))
    value = re.sub(r'љ','b',str(value))
    value = re.sub(r'њ','h',str(value))
    value = re.sub(r'ћ','h',str(value))
    value = re.sub(r'ќ','k',str(value))
    value = re.sub(r'ѝ','n',str(value))
    value = re.sub(r'ў','y',str(value))
    value = re.sub(r'џ','u',str(value))
    value = re.sub(r'Ѡ','Ѡ',str(value))
    value = re.sub(r'ѡ','w',str(value))
    value = re.sub(r'Ѣ','b',str(value))
    value = re.sub(r'ѣ','b',str(value))
    value = re.sub(r'Ѥ','Ѥ',str(value))
    value = re.sub(r'ѥ','ѥ',str(value))
    value = re.sub(r'Ѧ','Ѧ',str(value))
    value = re.sub(r'ѧ','ѧ',str(value))
    value = re.sub(r'Ѩ','Ѩ',str(value))
    value = re.sub(r'ѩ','ѩ',str(value))
    value = re.sub(r'Ѫ','Ѫ',str(value))
    value = re.sub(r'ѫ','ѫ',str(value))
    value = re.sub(r'Ѭ','Ѭ',str(value))
    value = re.sub(r'ѭ','ѭ',str(value))
    value = re.sub(r'Ѯ','Ѯ',str(value))
    value = re.sub(r'ѯ','ѯ',str(value))
    value = re.sub(r'Ѱ','Ѱ',str(value))
    value = re.sub(r'ѱ','ѱ',str(value))
    value = re.sub(r'Ѳ','O',str(value))
    value = re.sub(r'ѳ','o',str(value))
    value = re.sub(r'Ѵ','V',str(value))
    value = re.sub(r'ѵ','v',str(value))
    value = re.sub(r'Ѷ','V',str(value))
    value = re.sub(r'ѷ','v',str(value))
    value = re.sub(r'Ѹ','Ѹ',str(value))
    value = re.sub(r'ѹ','ѹ',str(value))
    value = re.sub(r'Ѻ','O',str(value))
    value = re.sub(r'ѻ','o',str(value))
    value = re.sub(r'Ѽ','Ѽ',str(value))
    value = re.sub(r'ѽ','ѽ',str(value))
    value = re.sub(r'Ѿ','Ѿ',str(value))
    value = re.sub(r'ѿ','w',str(value))
    value = re.sub(r'¡','i',str(value))
    value = re.sub(r'¢','c',str(value))
    value = re.sub(r'£','£',str(value))
    value = re.sub(r'¤','¤',str(value))
    value = re.sub(r'¥','¥',str(value))
    value = re.sub(r'¦','¦',str(value))
    value = re.sub(r'§','§',str(value))
    value = re.sub(r'¨','¨',str(value))
    value = re.sub(r'©','©',str(value))
    value = re.sub(r'ª','ª',str(value))
    value = re.sub(r'«','«',str(value))
    value = re.sub(r'¬','¬',str(value))
    value = re.sub(r' -','-',str(value))
    value = re.sub(r'®','®',str(value))
    value = re.sub(r'¯','¯',str(value))
    value = re.sub(r'°','°',str(value))
    value = re.sub(r'±','±',str(value))
    value = re.sub(r'²','²',str(value))
    value = re.sub(r'³','³',str(value))
    value = re.sub(r'´','´',str(value))
    value = re.sub(r'µ','µ',str(value))
    value = re.sub(r'¶','¶',str(value))
    value = re.sub(r'·','·',str(value))
    value = re.sub(r'¸','¸',str(value))
    value = re.sub(r'¹','¹',str(value))
    value = re.sub(r'º','º',str(value))
    value = re.sub(r'»','»',str(value))
    value = re.sub(r'¼','¼',str(value))
    value = re.sub(r'½','½',str(value))
    value = re.sub(r'¾','¾',str(value))
    value = re.sub(r'¿','¿',str(value))
    value = re.sub(r'À','A',str(value))
    value = re.sub(r'Á','A',str(value))
    value = re.sub(r'Â','A',str(value))
    value = re.sub(r'Ã','A',str(value))
    value = re.sub(r'Ä','A',str(value))
    value = re.sub(r'Å','A',str(value))
    value = re.sub(r'Æ','AE',str(value))
    value = re.sub(r'Ç','C',str(value))
    value = re.sub(r'È','E',str(value))
    value = re.sub(r'É','E',str(value))
    value = re.sub(r'Ê','E',str(value))
    value = re.sub(r'Ë','E',str(value))
    value = re.sub(r'Ì','I',str(value))
    value = re.sub(r'Í','I',str(value))
    value = re.sub(r'Î','I',str(value))
    value = re.sub(r'Ï','I',str(value))
    value = re.sub(r'Ð','D',str(value))
    value = re.sub(r'Ñ','N',str(value))
    value = re.sub(r'Ò','O',str(value))
    value = re.sub(r'Ó','O',str(value))
    value = re.sub(r'Ô','O',str(value))
    value = re.sub(r'Õ','O',str(value))
    value = re.sub(r'Ö','O',str(value))
    value = re.sub(r'×','x',str(value))
    value = re.sub(r'Ø','O',str(value))
    value = re.sub(r'Ù','U',str(value))
    value = re.sub(r'Ú','U',str(value))
    value = re.sub(r'Û','U',str(value))
    value = re.sub(r'Ü','U',str(value))
    value = re.sub(r'Ý','Y',str(value))
    value = re.sub(r'Þ','b',str(value))
    value = re.sub(r'ß','B',str(value))
    value = re.sub(r'à','a',str(value))
    value = re.sub(r'á','a',str(value))
    value = re.sub(r'â','a',str(value))
    value = re.sub(r'ã','a',str(value))
    value = re.sub(r'ä','a',str(value))
    value = re.sub(r'å','a',str(value))
    value = re.sub(r'æ','a',str(value))
    value = re.sub(r'ç','c',str(value))
    value = re.sub(r'è','e',str(value))
    value = re.sub(r'é','e',str(value))
    value = re.sub(r'ê','e',str(value))
    value = re.sub(r'ë','e',str(value))
    value = re.sub(r'ì','i',str(value))
    value = re.sub(r'í','i',str(value))
    value = re.sub(r'î','i',str(value))
    value = re.sub(r'ï','i',str(value))
    value = re.sub(r'ð','o',str(value))
    value = re.sub(r'ñ','n',str(value))
    value = re.sub(r'ò','o',str(value))
    value = re.sub(r'ó','o',str(value))
    value = re.sub(r'ô','o',str(value))
    value = re.sub(r'õ','o',str(value))
    value = re.sub(r'ö','o',str(value))
    value = re.sub(r'÷','÷',str(value))
    value = re.sub(r'ø','o',str(value))
    value = re.sub(r'ù','u',str(value))
    value = re.sub(r'ú','u',str(value))
    value = re.sub(r'û','u',str(value))
    value = re.sub(r'ü','u',str(value))
    value = re.sub(r'ý','y',str(value))
    value = re.sub(r'þ','þ',str(value))
    value = re.sub(r'ÿ','y',str(value))
#     value = re.sub(r'([A-Za-z]+)\;',r'\1',str(value))
#     value = re.sub(r'aacute','a',str(value))
#     value = re.sub(r'micro','u',str(value))
#     value = re.sub(r'Agrave','A',str(value))
#     value = re.sub(r'Aacute','A',str(value))
#     value = re.sub(r'Acirc','A',str(value))
#     value = re.sub(r'Atilde','A',str(value))
#     value = re.sub(r'Auml','A',str(value))
#     value = re.sub(r'Aring','A',str(value))
#     value = re.sub(r'AElig','E',str(value))
#     value = re.sub(r'Ccedil','C',str(value))
#     value = re.sub(r'Egrave','E',str(value))
#     value = re.sub(r'Eacute','E',str(value))
#     value = re.sub(r'Ecirc','E',str(value))
#     value = re.sub(r'Euml','E',str(value))
#     value = re.sub(r'Igrave','I',str(value))
#     value = re.sub(r'Iacute','I',str(value))
#     value = re.sub(r'Icirc','I',str(value))
#     value = re.sub(r'Iuml','I',str(value))
#     value = re.sub(r'ETH','D',str(value))
#     value = re.sub(r'Ntilde','N',str(value))
#     value = re.sub(r'Ograve','O',str(value))
#     value = re.sub(r'Oacute','O',str(value))
#     value = re.sub(r'Ocirc','O',str(value))
#     value = re.sub(r'Otilde','O',str(value))
#     value = re.sub(r'Ouml','O',str(value))
#     value = re.sub(r'times','x',str(value))
#     value = re.sub(r'Oslash','O',str(value))
#     value = re.sub(r'Ugrave','U',str(value))
#     value = re.sub(r'Uacute','U',str(value))
#     value = re.sub(r'Ucirc','U',str(value))
#     value = re.sub(r'Uuml','U',str(value))
#     value = re.sub(r'Yacute','Y',str(value))
#     value = re.sub(r'THORN','p',str(value))
#     value = re.sub(r'szlig','B',str(value))
#     value = re.sub(r'agrave','a',str(value))
#     value = re.sub(r'aacute','a',str(value))
#     value = re.sub(r'acirc','a',str(value))
#     value = re.sub(r'atilde','a',str(value))
#     value = re.sub(r'auml','a',str(value))
#     value = re.sub(r'aring','a',str(value))
#     value = re.sub(r'aelig','ae',str(value))
#     value = re.sub(r'ccedil','c',str(value))
#     value = re.sub(r'egrave','e',str(value))
#     value = re.sub(r'eacute','e',str(value))
#     value = re.sub(r'ecirc','e',str(value))
#     value = re.sub(r'euml','e',str(value))
#     value = re.sub(r'igrave','i',str(value))
#     value = re.sub(r'iacute','i',str(value))
#     value = re.sub(r'icirc','i',str(value))
#     value = re.sub(r'iuml','i',str(value))
#     value = re.sub(r'eth','o',str(value))
#     value = re.sub(r'ntilde','n',str(value))
#     value = re.sub(r'ograve','o',str(value))
#     value = re.sub(r'oacute','o',str(value))
#     value = re.sub(r'ocirc','o',str(value))
#     value = re.sub(r'otilde','o',str(value))
#     value = re.sub(r'ouml','o',str(value))
#     value = re.sub(r'divide','÷',str(value))
#     value = re.sub(r'oslash','o',str(value))
#     value = re.sub(r'ugrave','u',str(value))
#     value = re.sub(r'uacute','u',str(value))
#     value = re.sub(r'ucirc','u',str(value))
#     value = re.sub(r'uuml','u',str(value))
#     value = re.sub(r'yacute','y',str(value))
#     value = re.sub(r'thorn','p',str(value))
#     value = re.sub(r'yuml','y',str(value))
    

#     print "After",value html_encode(
    return value
def special_char_to_normal(value):
    value = re.sub(r'\\xc3\\x80','A',str(value))
    value = re.sub(r'\\xc3\\x81','A',str(value))
    value = re.sub(r'\\xc3\\x82','A',str(value))
    value = re.sub(r'\\xc3\\x83','A',str(value))
    value = re.sub(r'\\xc3\\x84','A',str(value))
    value = re.sub(r'\\xc3\\x85','A',str(value))
    value = re.sub(r'\\xc3\\x86','A',str(value))
    value = re.sub(r'\\xc3\\x87','C',str(value))
    value = re.sub(r'\\xc3\\x88','E',str(value))
    value = re.sub(r'\\xc3\\x89','E',str(value))
    value = re.sub(r'\\xc3\\x8a','E',str(value))
    value = re.sub(r'\\xc3\\x8b','E',str(value))
    value = re.sub(r'\\xc3\\x8c','I',str(value))
    value = re.sub(r'\\xc3\\x8d','I',str(value))
    value = re.sub(r'\\xc3\\x8e','I',str(value))
    value = re.sub(r'\\xc3\\x8f','I',str(value))
    value = re.sub(r'\\xc3\\x90','D',str(value))
    value = re.sub(r'\\xc3\\x91','N',str(value))
    value = re.sub(r'\\xc3\\x92','O',str(value))
    value = re.sub(r'\\xc3\\x93','O',str(value))
    value = re.sub(r'\\xc3\\x94','O',str(value))
    value = re.sub(r'\\xc3\\x95','O',str(value))
    value = re.sub(r'\\xc3\\x96','O',str(value))
    value = re.sub(r'\\xc3\\x98','O',str(value))
    value = re.sub(r'\\xc3\\x99','U',str(value))
    value = re.sub(r'\\xc3\\x9a','U',str(value))
    value = re.sub(r'\\xc3\\x9b','U',str(value))
    value = re.sub(r'\\xc3\\x9c','U',str(value))
    value = re.sub(r'\\xc3\\x9d','Y',str(value))
    value = re.sub(r'\\xc3\\x9e','DE',str(value))
    value = re.sub(r'\\xc3\\x9f','S',str(value))
    value = re.sub(r'\\xc3\\xa0','a',str(value))
    value = re.sub(r'\\xc3\\xa1','a',str(value))
    value = re.sub(r'\\xc3\\xa2','a',str(value))
    value = re.sub(r'\\xc3\\xa3','a',str(value))
    value = re.sub(r'\\xc3\\xa4','a',str(value))
    value = re.sub(r'\\xc3\\xa5','a',str(value))
    value = re.sub(r'\\xc3\\xa6','ae',str(value))
    value = re.sub(r'\\xc3\\xa7','c',str(value))
    value = re.sub(r'\\xc3\\xa7','c',str(value))
    value = re.sub(r'\\xc3\\xa8','e',str(value))
    value = re.sub(r'\\xc3\\xa9','e',str(value))
    value = re.sub(r'\\xc3\\xaa','e',str(value))
    value = re.sub(r'\\xc3\\xab','e',str(value))
    value = re.sub(r'\\xc3\\xac','i',str(value))
    value = re.sub(r'\\xc3\\xad','i',str(value))
    value = re.sub(r'\\xc3\\xae','i',str(value))
    value = re.sub(r'\\xc3\\xaf','i',str(value))
    value = re.sub(r'\\xc3\\xb0','o',str(value))
    value = re.sub(r'\\xc3\\xb1','n',str(value))
    value = re.sub(r'\\xc3\\xb2','o',str(value))
    value = re.sub(r'\\xc3\\xb3','o',str(value))
    value = re.sub(r'\\xc3\\xb4','o',str(value))
    value = re.sub(r'\\xc3\\xb5','o',str(value))
    value = re.sub(r'\\xc3\\xb6','o',str(value))
    value = re.sub(r'\\xc3\\xb8','o',str(value))
    value = re.sub(r'\\xc3\\xb9','u',str(value))
    value = re.sub(r'\\xc3\\xba','u',str(value))
    value = re.sub(r'\\xc3\\xbb','u',str(value))
    value = re.sub(r'\\xc3\\xbc','u',str(value))
    value = re.sub(r'\\xc3\\xbd','y',str(value))
    value = re.sub(r'\\xc3\\xbe','fe',str(value))
    value = re.sub(r'\\xc3\\xbf','y',str(value))
    value = re.sub(r'\\xc4\\x80','A',str(value))
    value = re.sub(r'\\xc4\\x81','a',str(value))
    value = re.sub(r'\\xc4\\x82','A',str(value))
    value = re.sub(r'\\xc4\\x83','a',str(value))
    value = re.sub(r'\\xc4\\x84','A',str(value))
    value = re.sub(r'\\xc4\\x85','a',str(value))
    value = re.sub(r'\\xc4\\x86','C',str(value))
    value = re.sub(r'\\xc4\\x87','c',str(value))
    value = re.sub(r'\\xc4\\x88','C',str(value))
    value = re.sub(r'\\xc4\\x89','c',str(value))
    value = re.sub(r'\\xc4\\x8a','C',str(value))
    value = re.sub(r'\\xc4\\x8b','c',str(value))
    value = re.sub(r'\\xc4\\x8c','C',str(value))
    value = re.sub(r'\\xc4\\x8d','c',str(value))
    value = re.sub(r'\\xc4\\x8e','D',str(value))
    value = re.sub(r'\\xc4\\x8f','d',str(value))
    value = re.sub(r'\\xc4\\x90','D',str(value))
    value = re.sub(r'\\xc4\\x91','d',str(value))
    value = re.sub(r'\\xc4\\x92','E',str(value))
    value = re.sub(r'\\xc4\\x93','e',str(value))
    value = re.sub(r'\\xc4\\x94','E',str(value))
    value = re.sub(r'\\xc4\\x95','e',str(value))
    value = re.sub(r'\\xc4\\x96','E',str(value))
    value = re.sub(r'\\xc4\\x97','e',str(value))
    value = re.sub(r'\\xc4\\x98','E',str(value))
    value = re.sub(r'\\xc4\\x99','e',str(value))
    value = re.sub(r'\\xc4\\x9a','E',str(value))
    value = re.sub(r'\\xc4\\x9b','e',str(value))
    value = re.sub(r'\\xc4\\x9c','G',str(value))
    value = re.sub(r'\\xc4\\x9d','g',str(value))
    value = re.sub(r'\\xc4\\x9e','G',str(value))
    value = re.sub(r'\\xc4\\x9f','g',str(value))
    value = re.sub(r'\\xc4\\xa0','G',str(value))
    value = re.sub(r'\\xc4\\xa1','g',str(value))
    value = re.sub(r'\\xc4\\xa2','G',str(value))
    value = re.sub(r'\\xc4\\xa3','g',str(value))
    value = re.sub(r'\\xc4\\xa4','H',str(value))
    value = re.sub(r'\\xc4\\xa5','h',str(value))
    value = re.sub(r'\\xc4\\xa6','H',str(value))
    value = re.sub(r'\\xc4\\xa7','h',str(value))
    value = re.sub(r'\\xc4\\xa8','I',str(value))
    value = re.sub(r'\\xc4\\xa9','i',str(value))
    value = re.sub(r'\\xc4\\xaa','I',str(value))
    value = re.sub(r'\\xc4\\xab','i',str(value))
    value = re.sub(r'\\xc4\\xac','I',str(value))
    value = re.sub(r'\\xc4\\xad','i',str(value))
    value = re.sub(r'\\xc4\\xae','I',str(value))
    value = re.sub(r'\\xc4\\xaf','i',str(value))
    value = re.sub(r'\\xc4\\xb0','I',str(value))
    value = re.sub(r'\\xc4\\xb1','i',str(value))
    value = re.sub(r'\\xc4\\xb2','IJ',str(value))
    value = re.sub(r'\\xc4\\xb3','ij',str(value))
    value = re.sub(r'\\xc4\\xb4','J',str(value))
    value = re.sub(r'\\xc4\\xb5','j',str(value))
    value = re.sub(r'\\xc4\\xb6','K',str(value))
    value = re.sub(r'\\xc4\\xb7','k',str(value))
    value = re.sub(r'\\xc4\\xb8','k',str(value))
    value = re.sub(r'\\xc4\\xb9','L',str(value))
    value = re.sub(r'\\xc4\\xba','l',str(value))
    value = re.sub(r'\\xc4\\xbb','L',str(value))
    value = re.sub(r'\\xc4\\xbc','l',str(value))
    value = re.sub(r'\\xc4\\xbd','L',str(value))
    value = re.sub(r'\\xc4\\xbe','l',str(value))
    value = re.sub(r'\\xc4\\xbf','L',str(value))
    value = re.sub(r'\\xc5\\x80','l',str(value))
    value = re.sub(r'\\xc5\\x81','L',str(value))
    value = re.sub(r'\\xc5\\x82','l',str(value))
    value = re.sub(r'\\xc5\\x83','N',str(value))
    value = re.sub(r'\\xc5\\x84','n',str(value))
    value = re.sub(r'\\xc5\\x85','N',str(value))
    value = re.sub(r'\\xc5\\x86','n',str(value))
    value = re.sub(r'\\xc5\\x87','N',str(value))
    value = re.sub(r'\\xc5\\x88','n',str(value))
    value = re.sub(r'\\xc5\\x89','n',str(value))
    value = re.sub(r'\\xc5\\x8a','n',str(value))
    value = re.sub(r'\\xc5\\x8b','n',str(value))
    value = re.sub(r'\\xc5\\x8c','O',str(value))
    value = re.sub(r'\\xc5\\x8d','o',str(value))
    value = re.sub(r'\\xc5\\x8e','O',str(value))
    value = re.sub(r'\\xc5\\x8f','o',str(value))
    value = re.sub(r'\\xc5\\x90','O',str(value))
    value = re.sub(r'\\xc5\\x91','o',str(value))
    value = re.sub(r'\\xc5\\x92','OE',str(value))
    value = re.sub(r'\\xc5\\x93','oe',str(value))
    value = re.sub(r'\\xc5\\x94','R',str(value))
    value = re.sub(r'\\xc5\\x95','r',str(value))
    value = re.sub(r'\\xc5\\x96','R',str(value))
    value = re.sub(r'\\xc5\\x97','r',str(value))
    value = re.sub(r'\\xc5\\x98','R',str(value))
    value = re.sub(r'\\xc5\\x99','r',str(value))
    value = re.sub(r'\\xc5\\x9a','S',str(value))
    value = re.sub(r'\\xc5\\x9b','s',str(value))
    value = re.sub(r'\\xc5\\x9c','S',str(value))
    value = re.sub(r'\\xc5\\x9d','s',str(value))
    value = re.sub(r'\\xc5\\x9e','S',str(value))
    value = re.sub(r'\\xc5\\x9f','s',str(value))
    value = re.sub(r'\\xc5\\xa0','S',str(value))
    value = re.sub(r'\\xc5\\xa1','s',str(value))
    value = re.sub(r'\\xc5\\xa2','T',str(value))
    value = re.sub(r'\\xc5\\xa3','t',str(value))
    value = re.sub(r'\\xc5\\xa4','T',str(value))
    value = re.sub(r'\\xc5\\xa5','t',str(value))
    value = re.sub(r'\\xc5\\xa6','T',str(value))
    value = re.sub(r'\\xc5\\xa7','t',str(value))
    value = re.sub(r'\\xc5\\xa8','U',str(value))
    value = re.sub(r'\\xc5\\xa9','u',str(value))
    value = re.sub(r'\\xc5\\xaa','U',str(value))
    value = re.sub(r'\\xc5\\xab','u',str(value))
    value = re.sub(r'\\xc5\\xac','U',str(value))
    value = re.sub(r'\\xc5\\xad','u',str(value))
    value = re.sub(r'\\xc5\\xae','U',str(value))
    value = re.sub(r'\\xc5\\xaf','u',str(value))
    value = re.sub(r'\\xc5\\xb0','U',str(value))
    value = re.sub(r'\\xc5\\xb1','u',str(value))
    value = re.sub(r'\\xc5\\xb2','U',str(value))
    value = re.sub(r'\\xc5\\xb3','u',str(value))
    value = re.sub(r'\\xc5\\xb4','W',str(value))
    value = re.sub(r'\\xc5\\xb5','w',str(value))
    value = re.sub(r'\\xc5\\xb6','Y',str(value))
    value = re.sub(r'\\xc5\\xb7','y',str(value))
    value = re.sub(r'\\xc5\\xb8','Y',str(value))
    value = re.sub(r'\\xc5\\xb9','Z',str(value))
    value = re.sub(r'\\xc5\\xba','z',str(value))
    value = re.sub(r'\\xc5\\xbb','Z',str(value))
    value = re.sub(r'\\xc5\\xbc','z',str(value))
    value = re.sub(r'\\xc5\\xbd','Z',str(value))
    value = re.sub(r'\\xc5\\xbe','z',str(value))
    value = re.sub(r'\\xc5\\xbf','S',str(value))
    value = re.sub(r'\\xc6\\x80','b',str(value))
    value = re.sub(r'\\xc6\\x81','B',str(value))
    value = re.sub(r'\\xc6\\x82','b',str(value))
    value = re.sub(r'\\xc6\\x83','b',str(value))
    value = re.sub(r'\\xc6\\x84','b',str(value))
    value = re.sub(r'\\xc6\\x85','b',str(value))
    value = re.sub(r'\\xc6\\x86','O',str(value))
    value = re.sub(r'\\xc6\\x87','C',str(value))
    value = re.sub(r'\\xc6\\x88','c',str(value))
    value = re.sub(r'\\xc6\\x89','D',str(value))
    value = re.sub(r'\\xc6\\x8a','D',str(value))
    value = re.sub(r'\\xc6\\x8b','D',str(value))
    value = re.sub(r'\\xc6\\x8c','d',str(value))
    value = re.sub(r'\\xc6\\x8d','ƍ',str(value))
    value = re.sub(r'\\xc6\\x8e','Ǝ',str(value))
    value = re.sub(r'\\xc6\\x8f','Ə',str(value))
    value = re.sub(r'\\xc6\\x90','Ɛ',str(value))
    value = re.sub(r'\\xc6\\x91','Ƒ',str(value))
    value = re.sub(r'\\xc6\\x92','ƒ',str(value))
    value = re.sub(r'\\xc6\\x93','Ɠ',str(value))
    value = re.sub(r'\\xc6\\x94','Ɣ',str(value))
    value = re.sub(r'\\xc6\\x95','ƕ',str(value))
    value = re.sub(r'\\xc6\\x96','Ɩ',str(value))
    value = re.sub(r'\\xc6\\x97','Ɨ',str(value))
    value = re.sub(r'\\xc6\\x98','Ƙ',str(value))
    value = re.sub(r'\\xc6\\x99','ƙ',str(value))
    value = re.sub(r'\\xc6\\x9a','ƚ',str(value))
    value = re.sub(r'\\xc6\\x9b','ƛ',str(value))
    value = re.sub(r'\\xc6\\x9c','Ɯ',str(value))
    value = re.sub(r'\\xc6\\x9d','Ɲ',str(value))
    value = re.sub(r'\\xc6\\x9e','ƞ',str(value))
    value = re.sub(r'\\xc6\\x9f','Ɵ',str(value))
    value = re.sub(r'\\xc6\\xa0','Ơ',str(value))
    value = re.sub(r'\\xc6\\xa1','ơ',str(value))
    value = re.sub(r'\\xc6\\xa2','Ƣ',str(value))
    value = re.sub(r'\\xc6\\xa3','ƣ',str(value))
    value = re.sub(r'\\xc6\\xa4','Ƥ',str(value))
    value = re.sub(r'\\xc6\\xa5','ƥ',str(value))
    value = re.sub(r'\\xc6\\xa6','Ʀ',str(value))
    value = re.sub(r'\\xc6\\xa7','Ƨ',str(value))
    value = re.sub(r'\\xc6\\xa8','ƨ',str(value))
    value = re.sub(r'\\xc6\\xa9','Ʃ',str(value))
    value = re.sub(r'\\xc6\\xaa','ƪ',str(value))
    value = re.sub(r'\\xc6\\xab','ƫ',str(value))
    value = re.sub(r'\\xc6\\xac','Ƭ',str(value))
    value = re.sub(r'\\xc6\\xad','ƭ',str(value))
    value = re.sub(r'\\xc6\\xae','Ʈ',str(value))
    value = re.sub(r'\\xc6\\xaf','Ư',str(value))
    value = re.sub(r'\\xc6\\xb0','ư',str(value))
    value = re.sub(r'\\xc6\\xb1','Ʊ',str(value))
    value = re.sub(r'\\xc6\\xb2','Ʋ',str(value))
    value = re.sub(r'\\xc6\\xb3','Ƴ',str(value))
    value = re.sub(r'\\xc6\\xb4','ƴ',str(value))
    value = re.sub(r'\\xc6\\xb5','Ƶ',str(value))
    value = re.sub(r'\\xc6\\xb6','ƶ',str(value))
    value = re.sub(r'\\xc6\\xb7','Ʒ',str(value))
    value = re.sub(r'\\xc6\\xb8','Ƹ',str(value))
    value = re.sub(r'\\xc6\\xb9','ƹ',str(value))
    value = re.sub(r'\\xc6\\xba','ƺ',str(value))
    value = re.sub(r'\\xc6\\xbb','ƻ',str(value))
    value = re.sub(r'\\xc6\\xbc','Ƽ',str(value))
    value = re.sub(r'\\xc6\\xbd','ƽ',str(value))
    value = re.sub(r'\\xc6\\xbe','ƾ',str(value))
    value = re.sub(r'\\xc6\\xbf','ƿ',str(value))
    value = re.sub(r'\\xc7\\x80','ǀ',str(value))
    value = re.sub(r'\\xc7\\x81','ǁ',str(value))
    value = re.sub(r'\\xc7\\x82','ǂ',str(value))
    value = re.sub(r'\\xc7\\x83','ǃ',str(value))
    value = re.sub(r'\\xc7\\x84','DZ',str(value))
    value = re.sub(r'\\xc7\\x85','Dz',str(value))
    value = re.sub(r'\\xc7\\x86','dz',str(value))
    value = re.sub(r'\\xc7\\x87','LJ',str(value))
    value = re.sub(r'\\xc7\\x88','Lj',str(value))
    value = re.sub(r'\\xc7\\x89','lj',str(value))
    value = re.sub(r'\\xc7\\x8a','NJ',str(value))
    value = re.sub(r'\\xc7\\x8b','Nj',str(value))
    value = re.sub(r'\\xc7\\x8c','nj',str(value))
    value = re.sub(r'\\xc7\\x8d','A',str(value))
    value = re.sub(r'\\xc7\\x8e','a',str(value))
    value = re.sub(r'\\xc7\\x8f','I',str(value))
    value = re.sub(r'\\xc7\\x90','i',str(value))
    value = re.sub(r'\\xc7\\x91','O',str(value))
    value = re.sub(r'\\xc7\\x92','o',str(value))
    value = re.sub(r'\\xc7\\x93','U',str(value))
    value = re.sub(r'\\xc7\\x94','u',str(value))
    value = re.sub(r'\\xc7\\x95','U',str(value))
    value = re.sub(r'\\xc7\\x96','u',str(value))
    value = re.sub(r'\\xc7\\x97','U',str(value))
    value = re.sub(r'\\xc7\\x98','u',str(value))
    value = re.sub(r'\\xc7\\x99','U',str(value))
    value = re.sub(r'\\xc7\\x9a','u',str(value))
    value = re.sub(r'\\xc7\\x9b','U',str(value))
    value = re.sub(r'\\xc7\\x9c','u',str(value))
    value = re.sub(r'\\xc7\\x9d','e',str(value))
    value = re.sub(r'\\xc7\\x9e','A',str(value))
    value = re.sub(r'\\xc7\\x9f','a',str(value))
    value = re.sub(r'\\xc7\\xa0','A',str(value))
    value = re.sub(r'\\xc7\\xa1','a',str(value))
    value = re.sub(r'\\xc7\\xa2','AE',str(value))
    value = re.sub(r'\\xc7\\xa3','ae',str(value))
    value = re.sub(r'\\xc7\\xa4','G',str(value))
    value = re.sub(r'\\xc7\\xa5','g',str(value))
    value = re.sub(r'\\xc7\\xa6','G',str(value))
    value = re.sub(r'\\xc7\\xa7','g',str(value))
    value = re.sub(r'\\xc7\\xa8','K',str(value))
    value = re.sub(r'\\xc7\\xa9','k',str(value))
    value = re.sub(r'\\xc7\\xaa','Ǫ',str(value))
    value = re.sub(r'\\xc7\\xab','ǫ',str(value))
    value = re.sub(r'\\xc7\\xac','Ǭ',str(value))
    value = re.sub(r'\\xc7\\xad','ǭ',str(value))
    value = re.sub(r'\\xc7\\xae','EZH',str(value))
    value = re.sub(r'\\xc7\\xaf','ezh',str(value))
    value = re.sub(r'\\xc7\\xb0','j',str(value))
    value = re.sub(r'\\xc7\\xb1','DZ',str(value))
    value = re.sub(r'\\xc7\\xb2','Dz',str(value))
    value = re.sub(r'\\xc7\\xb3','dz',str(value))
    value = re.sub(r'\\xc7\\xb4','G',str(value))
    value = re.sub(r'\\xc7\\xb5','g',str(value))
    value = re.sub(r'\\xc7\\xb6','HWAIR',str(value))
    value = re.sub(r'\\xc7\\xb7','WYNN',str(value))
    value = re.sub(r'\\xc7\\xb8','N',str(value))
    value = re.sub(r'\\xc7\\xb9','n',str(value))
    value = re.sub(r'\\xc7\\xba','A',str(value))
    value = re.sub(r'\\xc7\\xbb','a',str(value))
    value = re.sub(r'\\xc7\\xbc','AE',str(value))
    value = re.sub(r'\\xc7\\xbd','ae',str(value))
    value = re.sub(r'\\xc7\\xbe','O',str(value))
    value = re.sub(r'\\xc7\\xbf','o',str(value))
    return value


def xml_generation(datasourceid,ET,document,xml_dict,encode_replace):
    try:
        dSource=''
        customList = []
        custom_dict = defaultdict(list)
        for key in xml_dict:
            xml_time_set = str(key).split('|')
            tag_time_serious=xml_time_set[0]
            last_date=xml_time_set[1]
            first_date=xml_time_set[2]
            frequency_type=xml_time_set[3]
            tag_xref=xml_time_set[4]
            element01,element02,element03,element04,element05,element06,element07,element08,element09='','','','','','','','',''
            if str(encode_replace) == 'yes':
                element01=special_char_replace(xml_time_set[5])
                element02=special_char_replace(xml_time_set[6])
                element03=special_char_replace(xml_time_set[7])
                element04=special_char_replace(xml_time_set[8])
                element05=special_char_replace(xml_time_set[9])
                element06=special_char_replace(xml_time_set[10])
                element07=special_char_replace(xml_time_set[11])
                element08=special_char_replace(xml_time_set[12])
                element09=special_char_replace(xml_time_set[13])
            if str(encode_replace) == 'yes1':
                element01=special_char_to_normal(xml_time_set[5])
                element02=special_char_to_normal(xml_time_set[6])
                element03=special_char_to_normal(xml_time_set[7])
                element04=special_char_to_normal(xml_time_set[8])
                element05=special_char_to_normal(xml_time_set[9])
                element06=special_char_to_normal(xml_time_set[10])
                element07=special_char_to_normal(xml_time_set[11])
                element08=special_char_to_normal(xml_time_set[12])
                element09=special_char_to_normal(xml_time_set[13])
            else:
                element01=xml_time_set[5]
                element02=xml_time_set[6]
                element03=xml_time_set[7]
                element04=xml_time_set[8]
                element05=xml_time_set[9]
                element06=xml_time_set[10]
                element07=xml_time_set[11]
                element08=xml_time_set[12]
                element09=xml_time_set[13]
            data_source=xml_time_set[14]
            dSource = data_source
            time_series = ET.SubElement(document, 'time_series')
            time_series.set("last_date", last_date)
            time_series.set("first_date", first_date)
            time_series.set("frequency_type", frequency_type)
            xref = ET.SubElement(time_series, tag_xref)
            if str(element09) != 'n/a' and str(element09) != '':
                xref.set("element09", str(element09).strip())
            if str(element08) != 'n/a' and str(element08) != '':
                xref.set("element08", str(element08).strip())
            if str(element07) != 'n/a' and str(element07) != '':
                xref.set("element07", str(element07).strip())
            if str(element06) != 'n/a' and str(element06) != '':
                xref.set("element06", str(element06).strip())
            if str(element05) != 'n/a' and str(element05) != '':
                xref.set("element05", str(element05).strip())
            if str(element04) != 'n/a' and str(element04) != '':
                xref.set("element04", str(element04).strip())
            if str(element03) != 'n/a' and str(element03) != '':
                xref.set("element03", str(element03).strip())
            if str(element02) != 'n/a' and str(element02) != '':
                xref.set("element02", str(element02).strip())
            if str(element01) != 'n/a' and str(element01) != '':
                xref.set("element01", str(element01).strip())
            xref.set("data_source", data_source)

            for xml_val_list in xml_dict[key]:
                xml_datum_set = str(xml_val_list).split('|')
                tag_datum = xml_datum_set[0]
                applies_temp_time = xml_datum_set[1]
                publication_temp_time = xml_datum_set[2]
                value_format = xml_datum_set[3]
                quality = xml_datum_set[4]
                if str(data_source) == 'EEX' and re.search(r'^(?:0|0\.0)$', str(value_format)):
                    xmldata = ET.SubElement(time_series, 'datum')
                    xmldata.set("value", str(value_format))
                    xmldata.set("quality", str(quality))
                    xmldata.set("publication_datetime", str(publication_temp_time))
                    xmldata.set("applies_to_datetime", str(applies_temp_time))
                elif str(data_source) == 'EEX':
                    customList.append(xml_dict)
                    custom_dict.setdefault(key, []).append(xml_val_list)
                else:
                    xmldata = ET.SubElement(time_series, 'datum')
                    xmldata.set("value", str(value_format))
                    xmldata.set("quality", str(quality))
                    xmldata.set("publication_datetime", str(publication_temp_time))
                    xmldata.set("applies_to_datetime", str(applies_temp_time))
        if str(dSource) == 'EEX' and len(customList) > 0:
            for key in custom_dict:
                xml_time_set = str(key).split('|')
                tag_time_serious = xml_time_set[0]
                last_date = xml_time_set[1]
                first_date = xml_time_set[2]
                frequency_type = xml_time_set[3]
                tag_xref = xml_time_set[4]
                element01 = xml_time_set[5]
                element02 = xml_time_set[6]
                element03 = xml_time_set[7]
                element04 = xml_time_set[8]
                element05 = xml_time_set[9]
                element06 = xml_time_set[10]
                element07 = xml_time_set[11]
                element08 = xml_time_set[12]
                element09 = xml_time_set[13]
                data_source = xml_time_set[14]
                time_series = ET.SubElement(document, 'time_series')
                time_series.set("last_date", last_date)
                time_series.set("first_date", first_date)
                time_series.set("frequency_type", frequency_type)
                xref = ET.SubElement(time_series, tag_xref)
                if str(element09) != 'n/a':
                    xref.set("element09", str(element09).strip())
                if str(element08) != 'n/a':
                    xref.set("element08", str(element08).strip())
                if str(element07) != 'n/a':
                    xref.set("element07", str(element07).strip())
                if str(element06) != 'n/a':
                    xref.set("element06", str(element06).strip())
                if str(element05) != 'n/a':
                    xref.set("element05", str(element05).strip())
                if str(element04) != 'n/a':
                    xref.set("element04", str(element04).strip())
                if str(element03) != 'n/a':
                    xref.set("element03", str(element03).strip())
                if str(element02) != 'n/a':
                    xref.set("element02", str(element02).strip())
                if str(element01) != 'n/a':
                    xref.set("element01", str(element01).strip())
                xref.set("data_source", data_source)

                for xml_val_list in custom_dict[key]:
                    xml_datum_set = str(xml_val_list).split('|')
                    tag_datum = xml_datum_set[0]
                    applies_temp_time = xml_datum_set[1]
                    publication_temp_time = xml_datum_set[2]
                    value_format = xml_datum_set[3]
                    quality = xml_datum_set[4]
                    xmldata = ET.SubElement(time_series, 'datum')
                    xmldata.set("value", str(value_format))
                    xmldata.set("quality", str(quality))
                    xmldata.set("publication_datetime", str(publication_temp_time))
                    xmldata.set("applies_to_datetime", str(applies_temp_time))
    except Exception as e:
        error_log = e, str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
    return ET

def date_validation_func(datasourceid,dateValidationFormat,dateValidationList):
#     print "datasourceid",datasourceid
#     print "dateValidationFormat",dateValidationFormat
#     print "dateValidationList",dateValidationList
    try:
        date_validation=dateValidationFormat
    
        startdate,enddate='',''
        
        if str(date_validation) == '{DD}':
            current_date = time.strftime('%Y-%m-%d')
            startdate=current_date
            enddate=current_date
        elif 'DD-' in date_validation:
            dateRegex = re.findall(r'\{DD(\W\d+)\}', date_validation, re.I)
            PreviousDay = now + relativedelta(days=int(dateRegex[0]))
            
            temp_time = PreviousDay.strftime('%Y-%m-%d')
            startdate = temp_time
            enddate=temp_time
        elif 'DD+' in date_validation:
            dateRegex = re.findall(r'\{DD(\W\d+)\}', date_validation, re.I)
            PreviousDay = now + relativedelta(days=int(dateRegex[0]))
            temp_time = PreviousDay.strftime('%Y-%m-%d')
            startdate=temp_time
            enddate = temp_time
        elif 'M-1' in date_validation:
            PreviousDay = now + relativedelta(days=-30)
            temp_time_month = PreviousDay.strftime('%m') 
            temp_time_year = PreviousDay.strftime('%Y') 
            temp_time = str(temp_time_year)+"-"+str(temp_time_month)+"-"+'01'
            startdate = temp_time
            enddate=time.strftime('%Y-%m-%d')
         
        elif 'M+1' in date_validation:
            PreviousDay = now + relativedelta(days=+30)
            temp_time = PreviousDay.strftime('%Y-%m-%d')
            startdate=time.strftime('%Y-%m-%d')
            enddate = temp_time
        
        d1 = datetime.strptime(startdate, "%Y-%m-%d")
        d2 = datetime.strptime(enddate, "%Y-%m-%d") 
        
        date_range=[]
        delta =abs((d2 - d1).days)
        for x in range(0, delta+1):
            
            PreviousDay = d1 + relativedelta(days=int(x))
            date_range.append(PreviousDay.strftime('%Y-%m-%d'))
        
        print dateValidationList
        print date_range
        validationStatus = set(date_range) - set(dateValidationList)
        return len(validationStatus)
    except Exception as e:
        error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
        print error_log
        Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
        sys.exit()
        
def main(Config):
    from xml.etree import ElementTree as ET
    datasourceid = Config.dsId

    '''
    download raw file
    '''
    
    raw_file = str(Config.get('filename', 'extractfilename'))
    # print raw_file
    raw_file_t = raw_file
    s3path_download = 'data/raw/' + str(Config.dsName).lower() + '/' + str(Config.mName).lower() + '/1.0/' + str(raw_file)
    raw_file = str(tempFilePath) + str(raw_file)
    # try:
        # Fundalytics_Utility.s3_filedownload(raw_file, datasourceid, s3path_download, 'Transform-Module', Config)
    # except Exception as e:
        # error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
        # Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
        # sys.exit()

    ''' Read the control file and get the required variables '''

    machine_name = Config.machineName
    domain_name = Config.machineName
    data_source = Config.get('default', 'T_DATASOURCE')
    daylight_saving = Config.get('default', 'T_DAYLIGHTSAVING')

    '''
    Generate XML node dataset and sub node source

    '''

    document = ET.Element('dataset')
    source = ET.SubElement(document, 'source')

    source.set("daylight_saving", daylight_saving)
    source.set("source_file_name", raw_file_t)
    source.set("data_source", data_source)
    source.set("domain_name", domain_name)
    source.set("machine_name", machine_name)

    process_error = '0'
    sectionName = 'T-' + str(Config.dsName) + '-' + Config.mName + '-'
    session = Config.sections()
    value_count = 0
    dateValidationList=[]
    first_date = now.strftime("%Y-%m-%dT%H:%M:%S.0000000")
    last_date = now.strftime("%Y-%m-%dT%H:%M:%S.0000000")
    publicationformat_date = strftime("%Y-%m-%dT%H:%M:%S.0000000", gmtime())
    xml_dict = defaultdict(list)
    req_sesssion = (x for x in session if sectionName in x)
    for session_bck in req_sesssion:
        # print session_bck
        file_type = Config.get(session_bck, 'FILETYPE')

        ''' Condition for raw file type '''

        try:
            if str(file_type) == 'HTMLTable':
                xml_dict, value_count,dateValidationList = html_table_format(ET, Config, document, data_source, datasourceid, raw_file,sectionName, session_bck, value_count, xml_dict, first_date,last_date, publicationformat_date,dateValidationList)
            elif str(file_type) == 'CSVFormat':
                xml_dict, value_count,dateValidationList = csv_format(ET, Config, document, data_source, datasourceid, raw_file,sectionName, session_bck, value_count, xml_dict, first_date,last_date, publicationformat_date,dateValidationList)
            elif str(file_type) == 'Excel':
                xml_dict, value_count,dateValidationList = excel_format(ET, Config, document, data_source, datasourceid, raw_file,sectionName, session_bck, value_count, xml_dict, first_date,last_date, publicationformat_date,dateValidationList)
            else:
                pass
        except Exception as e:
            process_error = 1
            error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
            print error_log
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
            sys.exit()
    # os.remove(raw_file)
    validationStatus = ''
    backFillingStatus = ''
    try:
        backFillingStatus = Config.get("backfill_data-" + str(Config.mName), str(Config.dsName) + "IsBackFill")
    except:
        backFillingStatus='NO'
    if str(backFillingStatus) == 'YES':
        validationStatus=0
    else:
        try:
            dateValidationList=list(set(dateValidationList))
            dateValidationFormat=''
            dateValidationFormattempList=[]
            dateValidationSectionName = 'E-' + str(Config.dsName) + '-' + Config.mName + '-'
            req_sesssion = (x for x in session if dateValidationSectionName in x)
            for session_bck in req_sesssion:
                try:
                    dateValidationFormat = Config.get(session_bck, 'T_DATEVALIDATIONFORMAT')
                    dateValidationFormattempList.append(str(dateValidationFormat))
                except:
                    pass
            print "dateValidationFormat",dateValidationList
            dateValidationFormattempList=list(set(dateValidationFormattempList))
            if 'today' in str(Config.scraperParameterName) and len(dateValidationFormattempList) > 1:
                dateValidationFormat='{DD}'
            elif 'past' in str(Config.scraperParameterName) and len(dateValidationFormattempList) > 1:
                dateValidationFormat='{DD-1}'
            if str(dateValidationFormat) != 'n/a' and str(dateValidationFormat) != '':
    #             print "Inside Function"
                validationStatus = date_validation_func(datasourceid,dateValidationFormat,dateValidationList)
            else:
    #             print "Outside Function"
                validationStatus=0
            # print "validationStatus",validationStatus
        except Exception as e:
            print "Error", e
            validationStatus=0
    if int(validationStatus) != 0:
        Fundalytics_Utility.date_validation_status(datasourceid,'Failure',value_count)
        raw_file_rm = str(Config.get('filename', 'extractfilename'))
        #raw_file_rm = 'Ibex_Block_Products_20160831_0343.html'
        sourcefileremove = 'data/raw/' + str(Config.dsName).lower() + '/' + str(Config.mName).lower() + '/1.0/' + str(raw_file_rm)
        Fundalytics_Utility.s3_removefile(datasourceid,sourcefileremove,'Transform-S3-File-Remove-Function',Config)
        print "Date Validation Failed for " + str(datasourceid)
    else:
        Fundalytics_Utility.date_validation_status(datasourceid,'Success',value_count)
        
        if int(process_error) == 0:
            encodereplace=''
            try:
                encodereplace = Config.get('default', 'T_ENCODEREPLACE')
            except:
                encodereplace ='no'
            xml_dict = collections.OrderedDict(xml_dict)
            ET = xml_generation(datasourceid,ET, document, xml_dict,encodereplace)
    
            ''' Generate cooked XML and save it '''
            xml_file = ''
    
            if '.xml' not in str(raw_file):
                raw_file1 = os.path.splitext(raw_file)[0]
                xml_file = str(raw_file1).replace('-', '_') + ".xml"
            else:
                xml_file = str(raw_file).replace('-', '_') + ".xml"
            try:
    
                et = ET.ElementTree(document)
                f = BytesIO()
                et.write(f, encoding='utf-8', xml_declaration=True)
                #html_encode
                if str(encodereplace) =='encode':
                    with codecs.open(xml_file, mode='wb', encoding='utf-8') as f1:
                        f1.write(html_encode(special_char_replace(f.getvalue().decode().encode('utf-8'))))
                        f1.close()
                else:
                    with codecs.open(xml_file, mode='wb', encoding='utf-8') as f1:
                        f1.write(special_char_replace(f.getvalue().decode().encode('utf-8')))
                        f1.close()
    
            except Exception as e:
                error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
                print error_log
                Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
                sys.exit()
    
            s3path_upload = 'data/cooked/' + str(Config.dsName).lower() + '/' + str(Config.mName).lower() + '/1.0/'
    
            # try:
            #     Fundalytics_Utility.s3_fileupload(xml_file, datasourceid, s3path_upload, 'Transform-Module', Config)
            # except Exception as e:
            #     error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
            #     print error_log
            #     Fundalytics_Utility.log(datasourceid, 'Transform-Module', error_log, 'Error', '')
            #     sys.exit()
            xml_file_temp = xml_file
            xml_file = xml_file.replace(tempFilePath, '')
            redis_key = str(datasourceid) + '|' + str(s3path_upload) + str(xml_file)
    
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', '', 'Transformed', str(s3path_upload) + str(xml_file))
            # os.remove(xml_file_temp)
            Fundalytics_Utility.count_update(datasourceid, value_count)
            Fundalytics_Utility.redis_connection(datasourceid, redis_key)
            Config.add_section('statustr')
            Config.set("statustr", "transformStatus", "1")
            print "Transform Completed for " + str(datasourceid)
            return Config
        else:
            print "Error on transform module for" + str(datasourceid)
            Fundalytics_Utility.log(datasourceid, 'Transform-Module', 'Error on transform module', 'Error', '')
            return Config