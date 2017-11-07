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
# Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/argus_media/study_transform/Fundalytics_Utility.py')
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/04/Fundalytics_Utility.py')
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import ast
import ftputil
import urllib2,cookielib
import xlsxwriter
from datetime import date, timedelta
from urlparse import urlparse
import itertools
from xlrd import open_workbook
from xlutils import copy

date_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))

# tempFilePath = "D:/argus_media/study_transform/temp/"
tempFilePath = "D:/01_2017/04/temp/"
if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)


def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x: not isinstance(x, (str, list, tuple)) or x,
                  (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))


###########################################'''To find the Extract_type of the url,we wre passing content_type and url to scrape'''#############################################

def downloading_file(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType, get_url_to_scrape,
                     method, control, content_type, response_content, response,rawFile_time):
    '''
    :GET: files will be downloaded
    :GET_BY: files will move to navigation function
    :return: raw file to main page
    '''
    try:

        '''json url is downloaded'''
        if content_type in ('json'):
            json_file = response.json()
            try:
                if (control.get(scraperParameterName, 'JSON_REPLACEMENT')) != 'n/a':
                    json_file=eval(control.get(scraperParameterName, 'JSON_REPLACEMENT'))

            except:
                json_file=json_file
            rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, 'json', control, json_file,get_url_to_scrape,rawFile_time)

            '''XML ,XLS ,CSV and PDF URL's will be  directly Downloaded '''
        elif content_type in ('xml', 'csv', 'pdf', 'xls', 'xlsx'):
            rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, content_type, control,
                                   response_content, 'n/a',rawFile_time)


            '''HTML files will be  downloaded '''
        elif content_type in ('jsp', 'htm', 'html'):
            if scraperType == 'html':
                html_file = response_content
                soup = BeautifulSoup(html_file, "html.parser")
                ''' If Extraction method is Get/Get_By in the control file this function will be called  '''
                if method == 'GET':
                    limits = int(control.get(scraperParameterName, 'LIMITS'))
                    table = soup.find_all('table', limit=limits)
                    rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control,
                                           table, 'n/a',rawFile_time)

                    ''' If there is  any Navigation in the control file Navigation Function will be called '''
                elif method == 'GET_BY':
                    if (control.get(scraperParameterName, 'E_NAVL1')) != 'n/a':
                        rawFile = navigation_function(DataSourceID, datasourceName, marketName, scraperParameterName,scraperType, get_url_to_scrape, method, control, html_file, soup,control.get(scraperParameterName, 'E_NAVL1').split('|'),rawFile_time)

            elif scraperType in ('xls', 'pdf', 'xml', 'csv', 'xlsx'):
                if method == 'GET_BY':
                    if (control.get(scraperParameterName, 'E_NAVL1')) != 'n/a':
                        rawFile = navigation_function(DataSourceID, datasourceName, marketName, scraperParameterName,scraperType, get_url_to_scrape, method, control, response_content, '',control.get(scraperParameterName, 'E_NAVL1').split('|'),rawFile_time)
                else:
                    rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control,response_content, '',rawFile_time)


        return rawFile

    except Exception as e:
        # print e
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


#######################################################'''Regex function'''################################################################################
def Regex_function(regex,content):
    regex_content = re.findall(regex, content, re.I)

    if regex_content:
        raw_file = regex_content[0]
    else:
        raw_file = ''
    return raw_file
#################################################################'''url formed by regex'''###############################################################################################
def rgexURL(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,get_url_to_scrape, method, control, html_file, soup, split_nav,rawFile_time):
    try:

        if 'REGEX' in str(split_nav[1]):
            urlRegex = split_nav[1].replace('REGEX{', '').replace('}', '')
            regexContent = re.findall(urlRegex, html_file, re.I)
            # print "regexContent:",regexContent
            for regexUrl in regexContent:
                try:
                    if isinstance(regexUrl, tuple):
                        regexUrlContent = regexUrl[0]
                        publishTime = regexUrl[1]
                        control.set("default", str(scraperParameterName) + "PUBLISHED", publishTime)
                    else:
                        regexUrlContent = regexUrl

                    homeUrl = urlparse(get_url_to_scrape)
                    base = homeUrl[0] + '://' + homeUrl[1]
                    if 'http:' in regexUrlContent:
                        baseUrl = regexUrlContent
                    elif 'www.' in regexUrlContent:
                        baseUrl = regexUrlContent
                    else:
                        regexUrlContent = '/' + regexUrlContent
                        regexUrlContent = re.sub(r'//', '/', regexUrlContent)
                        baseUrl = base + regexUrlContent

                    try:
                        if 'GET' in split_nav[2]:
                            # print "baseUrl:",baseUrl
                            response = requests.get(baseUrl)
                            # res_content = response.content
                            content = response.content
                            status = response.status_code
                            res_content = check_status(baseUrl, status, content, DataSourceID)
                            raw_file = file_writing(DataSourceID, datasourceName, marketName, scraperParameterName,
                                                    scraperType, control,
                                                    res_content, 'n/a', rawFile_time)
                        elif 'POST' in split_nav[2]:
                            headerPostion = str(split_nav[2].replace('POST(', '').replace(')', ''))
                            head = ast.literal_eval(headerPostion)
                            raw_file = post_method(DataSourceID, datasourceName, marketName, scraperParameterName,
                                                   scraperType,
                                                   control, baseUrl, head, rawFile_time)

                    except Exception as e:
                        Fundalytics_Utility.log(DataSourceID, 'Extract',
                                                str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno), 'Error', '')
                        sys.exit()
                except:
                    control.set("default", str(scraperParameterName) + "PUBLISHED", 'n/a')
        return raw_file
    except Exception as e:
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        sys.exit()
#################################################################'''url formed by next page navigation'''###################################################################
def nextPageURL(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,get_url_to_scrape, method, control, html_file, soup, split_nav, rawFile_time):
    try:
        raw_data = ''
        try:
            dateUrl=split_nav[2].replace('DATE{', '').replace('}', '')
            dateUrlList = re.findall(dateUrl, get_url_to_scrape)
            control.set("default", str(scraperParameterName) + "DATEURL", dateUrlList[0])
        except:
            control.set("default", str(scraperParameterName) + "DATEURL", 'n/a')
        pageNo = int(get_url_to_scrape[-1])
        while True:
            url = get_url_to_scrape[:-1] + str(pageNo)
            try:
                response = requests.get(url)
                content = response.content
                status = response.status_code
                response_content=check_status(url, status, content, DataSourceID)

                if control.get(scraperParameterName, 'E_NAVL2')!='n/a':
                    page=control.get(scraperParameterName, 'E_NAVL2').split('|')
                    if page[0]=='REGEX':
                        raw_file_content = re.findall(page[1], response_content, re.I)
                        raw_data = raw_data + raw_file_content[0]

                total_url = re.findall(split_nav[1].replace('REGEX{', '').replace('}', ''), response_content)

                if total_url:
                    pageNo += 1
                else:
                    break
            except:
                break

        raw_file = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control, raw_data, 'n/a',rawFile_time)

        return raw_file
    except Exception as e:
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        sys.exit()


######################################################  ''' navigation type will be class name, regex and url'''############################################################
'''Navigation type based on class, Regex and "URL'''

def navigation_function(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,
                             get_url_to_scrape, method, control, html_file, soup, split_nav,rawFile_time):
    '''

    CLASSNAME : Extract given classname using beautifulsoap
    REGEX     : Extract content from regex
    URL:REGEX : Extract url using regex and  check url is get or post method
    NAVIGATION: page navigation content will be extracted
    :return: raw file to main page
    '''

    try:
        class_regex_url = split_nav[0]

        '''navigation with class name'''
        if class_regex_url == 'CLASSNAME':
            class_name = split_nav[1]
            limits = 1
            limits = int(control.get(scraperParameterName, 'LIMITS'))
            table = soup.find_all('table', {'class': class_name}, limit=limits)
            raw_file = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, 'HTML', control, table, 'n/a',rawFile_time)

            '''navigation with Regex'''
        elif class_regex_url == 'REGEX':
            regex = split_nav[1]
            regex_content=Regex_function(regex,html_file)
            if regex_content:
                    raw_file = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control, regex_content,'n/a',rawFile_time)
            else:
                raw_file=''

            '''navigation with Url'''
        elif class_regex_url == 'URL':
            raw_file=rgexURL(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,get_url_to_scrape, method, control, html_file, soup, split_nav,rawFile_time)


        elif class_regex_url == 'NAVIGATION':
            raw_file = nextPageURL(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,get_url_to_scrape, method, control, html_file, soup, split_nav, rawFile_time)


        return raw_file
    except Exception as e:
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        sys.exit()


#######################################################post method extraction###################################
'''If Extraction method is post in the control file this function will be called '''


def post_method(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType, control, url, head,rawFile_time):
    '''

     :post data, post url, headers, cookies is processed and checking output content is by get or post method
     :return: raw file to main page
    '''
    try:
        con = requests.get(url)
        con_content = con.content
        status = con.status_code
        '''check whether url is working with status and getting response content'''
        checked_response_content = check_status(url, status, con_content, DataSourceID)

        post_data = control.get(scraperParameterName, 'E_POSTCONTENT')
        post_data = date_function(DataSourceID,post_data,control,datasourceName,marketName)


        post_url = control.get(scraperParameterName, 'E_POSTURL')
        post_url = date_function(DataSourceID,post_url,control,datasourceName,marketName)

        header = date_function(DataSourceID,str(head),control,datasourceName,marketName)
        header = ast.literal_eval(header)

        '''Requesting content by post method'''
        post_response = requests.post(url=post_url, data=post_data, cookies=con.cookies, headers=header)
        post_content = post_response.content
        # content = response.content
        status = post_response.status_code
        response_content = check_status(post_url, status, post_content, DataSourceID)


        if (control.get(scraperParameterName, 'E_NAVL1')) != 'n/a':


            splitNav = control.get(scraperParameterName, 'E_NAVL1').split('|')
            # splitNav = control.get(scraperParameterName, 'E_NAVL1')
            rawFile=navigation_function(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,url, 'post', control, post_content,'', splitNav, rawFile_time)

        else:
            '''Getting content type and fileName to write a file'''
            type = url_content_type(url, con, scraperType)
            if scraperType == 'html':
                rawFile_contentType = type

            elif scraperType in ('xls', 'pdf', 'xml', 'csv', 'xlsx'):
                rawFile_contentType = scraperType

            rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, rawFile_contentType, control,post_content, 'n/a',rawFile_time)

        return rawFile

    except Exception as e:
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        sys.exit()


###########################csv to excel function ############################################################
def csv_function(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, raw_content, rawFileName, backFillEnd,control):


    if '-none' in scraperParameterName:
        tag = scraperParameterName
        if backFillEnd!='':
            tag1 = str(backFillEnd)
        else:
            try:
                if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                    dateUrl = (control.get(scraperParameterName, 'URL_DATE')).split('|')
                    dateUrlList = re.findall(dateUrl[1],date_function(DataSourceID, control.get(scraperParameterName, 'URL'),control, datasourceName, marketName))
                    tag1 = str(dateUrlList[0])
                else:
                    raise Exception
            except:
                tag1 = str(cur_date)
            # tag1 = str(cur_date)
        with open(rawFileName, 'ab') as txt:
            txt.write(str(tag) + "\n")
            txt.write(tag1 + "\n")
            for row in raw_content:
                txt.write(str(row))
        txt.close()
    else:
        rawFileName = str(tempFilePath) + str(scraperParameterName) + '.csv'

        with open(rawFileName, 'wb') as txt:
            txt.write(str(raw_content))

    return rawFileName


###########################writting files and pushing to s3############################################################
def file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control, raw_content, Ivalue,rawFile_time):
    try:
        '''
        creating file name for Raw file
        '''
        try:
            if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                backFillEnd = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
                # date_time = str(backFillEnd.strftime('%Y%m%d_%H%M%S'))
                backFillEnd = str(backFillEnd.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                raise Exception
        except Exception as e:
            backFillEnd = ''
            # date_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

        # rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        rawFileName = tempFilePath + str(rawFile_time.replace('-', '_')) + '.' + str(scraperType)

        tag, tag1 = '', ''
        if str(scraperType) in ('xls', 'xlsx'):

            rawFileName = tempFilePath + str(scraperParameterName) + '.' + scraperType
            # print "xls rawFileName:",rawFileName
            with open(rawFileName, 'wb') as txt:
                txt.write(str(raw_content))

            workbook = open_workbook(rawFileName)
            # print workbook.sheet_names()
            # sys.exit()
            new_workbook = copy.copy(workbook)
            sheetName = control.get(scraperParameterName, 'E_XLS_SHEETNAME')
            sheetNameDate = date_function(DataSourceID,sheetName,control,datasourceName,marketName)
            # print "sheetNameDate:",sheetNameDate
            new_workbook._Workbook__worksheets = [worksheet for worksheet in new_workbook._Workbook__worksheets if re.match(sheetNameDate, worksheet.name)]
            new_workbook.save(rawFileName)

        elif 'json' in str(scraperType):
            try:
                if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                    dateUrl = (control.get(scraperParameterName, 'URL_DATE')).split('|')
                    dateUrlList = re.findall(dateUrl[1], Ivalue)
                    urlDate=str(dateUrlList[0])
            except:
                urlDate = str(cur_date)
            with open(rawFileName, "ab")as f:
                f.write(str(urlDate))
                f.write(str(raw_content))

        elif 'csv' in str(scraperType):
            rawFileName = csv_function(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, raw_content,rawFileName, backFillEnd,control)

        else:
            # print "Entering html session:"

            tag = '<h1>' + scraperParameterName + '</h1>'
            try:
                if control.get("default", str(scraperParameterName) + "DATEURL") != 'n/a':
                    tag1 = '<h2>' + str(control.get("default", str(scraperParameterName) + "DATEURL")) + '</h2>'
            except:
                if backFillEnd != '':
                    tag1 ='<h2>'+ str(backFillEnd)+ '</h2>'
                else:
                    tag1 = '<h2>' + str(cur_date) + '</h2>'



            raw_content= str(raw_content).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace('&quot;','"').replace('&#39', "'").replace('&nbsp;', " ")
            # print raw_content

            try:
                if control.get(scraperParameterName, 'VALUE_NORMALIZE') != 'n/a':
                    normalize_loop =control.get(scraperParameterName, 'VALUE_NORMALIZE').split('#')
                    for loop in normalize_loop:
                        normalize = str(loop).split('|')
                        raw_content = re.sub(normalize[0], normalize[1], raw_content)
            except:
                pass

            with open(rawFileName, 'ab') as txt:
                txt.write(str(tag) + "\n")
                try:
                    if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                        dateUrl = (control.get(scraperParameterName, 'URL_DATE')).split('|')
                        dateUrlList = re.findall(dateUrl[1],date_function(DataSourceID, control.get(scraperParameterName, 'URL'),control, datasourceName, marketName))
                        tag1 = '<h2>' + dateUrlList[0] + '</h2>'
                except:
                    pass
                txt.write(tag1 + "\n")
                for row in raw_content:
                    txt.write(str(row))

        return rawFileName
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


#################################################checking whether given url status and throwing it############################################
''' Exception Handling in the Request method based on the response '''


def check_status(url, status, response, DataSourceID):
    '''

    checking status of the website and three attempts for 500 status url
    :return: response content
    '''
    try:
        # print "status:",status
        if status in xrange(200, 399):
            return response
        elif status in xrange(500, 511):
            attempt = 0
            while attempt < 3:
                res = requests.get(url)
                response = res.content
                if res.status_code == '200':
                    return response
                else:
                    attempt += 1
                    time.sleep(5)
            raise Exception
        elif status in xrange(400, 451):
            # print "incorrect url"
            raise Exception
    except Exception as e:
        Fundalytics_Utility.log(DataSourceID, 'Extract', str("Website down|"+str(e)) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        sys.exit()


#############################to get content type of the url and check with scraper type, to extract corresponding file###################
''' To  check the url Extension / header  type to find the file type'''


def url_content_type(url, response, scraperType):
    ''' content_type got from the url header '''
    header_type = response.headers['content-type']

    type_name = re.match(r'[^>]*?\/(\w+)+\;?', header_type)
    content_type_header = type_name.group(1)

    if re.search(scraperType, str(content_type_header)):
        stype = str(scraperType).split('|')[0]
        content_type = stype
    elif content_type_header not in ('aspx', 'octet', 'php', 'plain', 'vnd','x','force'):
        content_type = content_type_header
    else:
        content_type = scraperType

    # if content_type in ('aspx', 'octet', 'php','plain','vnd'):
    #   content_type = scraperType

    return content_type


##########################################'''ftp url'''####################################################
'''ftp function with detailed url'''


def ftp_function(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType, control, url,rawFile_time):
    try:

        rawFileList = []
        if 'ftp:///' in url:
            # Connection information
            ftp_credencials = control.get(scraperParameterName, 'FTP_CREDENTIALS')
            # print ftp_credencials
            positions = ast.literal_eval(ftp_credencials)
            server = positions.get('server')
            username = positions.get('username')
            password = positions.get('password')
            directory = url.replace('ftp://', '')
            filematch = '*.'+str(scraperType)

            # Establish the connection
            try:

                ftp = ftplib.FTP(server)
                ftp.login(username, password)


                # Change to the proper directory..
                # try:
                ftp.cwd(directory)
            except Exception as e:
                Fundalytics_Utility.log(DataSourceID, 'Extract', str("ftp site down|" + str(datasourceName) + str(e)) + ' line no: ' + str(
                    sys.exc_traceback.tb_lineno), 'Error', '')
                sys.exit()


            # Loop through matching files and download each one individually
            y = 0

            for csvFileName in ftp.nlst(filematch):
                try:

                    if (control.get(scraperParameterName, 'E_NAVL1')) != 'n/a':
                        split_nav1 = control.get(scraperParameterName, 'E_NAVL1').split('|')
                        regexForFile = date_function(DataSourceID,split_nav1[1],control,datasourceName,marketName)
                    else:
                        regexForFile = date_function(DataSourceID,url,control,datasourceName,marketName)
                        # print "regexForFile:",regexForFile

                    Regex_content = re.findall(regexForFile, csvFileName, re.I)
                    # print "Regex_content:",Regex_content


                    if len(Regex_content) > 0:
                        # print "Regex_content:",Regex_content
                        rawFileName = tempFilePath + str(scraperParameterName) + str(y) + '.'+str(scraperType)
                        fhandle = open(csvFileName, 'wb')
                        # print 'Getting ' + csvFileName
                        # raw_input("file checking")
                        ftp.retrbinary('RETR ' + csvFileName, fhandle.write)
                        fhandle.close()
                        os.rename(csvFileName, rawFileName)
                        rawFileList.append(rawFileName)
                        y = y + 1
                except Exception as e:
                    Fundalytics_Utility.log(DataSourceID, 'Extract', str("Expected file is not found|" + str(datasourceName)+str(e)) + ' line no: ' + str(
                        sys.exc_traceback.tb_lineno), 'Error', '')
                    sys.exit()

        else:

            '''if navigation present in this ftp take the file name using regex'''
            if (control.get(scraperParameterName, 'E_NAVL1')) != 'n/a':
                res = urllib2.urlopen(url)
                res_content = res.read()

                '''Getting regex from control file'''
                split_nav1 = control.get(scraperParameterName, 'E_NAVL1').split('|')
                regexForFile = date_function(DataSourceID,split_nav1[1],control,datasourceName,marketName)
                '''getting last fileName from the website'''
                Regex_content = re.findall(regexForFile, res_content, re.I)


                for i, regex_filename in enumerate(Regex_content):
                    '''get content from the updated url'''
                    updated_url = url + '/' + str(regex_filename)
                    response = urllib2.urlopen(updated_url)
                    response_content = response.read()
                    rawFile = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control,
                                           response_content, i,rawFile_time)
                    rawFileList.append(str(rawFile))

            else:

                try:
                    response = urllib2.urlopen(url)
                    status = response.getcode()
                    # print "status ftp:", status
                    content = response.read()
                    response_content = check_status(url, status, content, DataSourceID)
                except Exception as e:
                    Fundalytics_Utility.log(DataSourceID, 'Extract',str("Expected file is not found|" +str(datasourceName)+ str(e)) + ' line no: ' + str(sys.exc_traceback.tb_lineno), 'Error', '')
                    sys.exit()

                rawFileList = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control,
                                           response_content, '',rawFile_time)

        return rawFileList

    except Exception as e:
        print str(e)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()

##########################################'''Session maintenance in the url'''###############################################
def sessionfile(DataSourceID, datasourceName, marketName, scraperParameterName,
                                                       scraperType, get_url_to_scrape, method, control, content_type,
                                                       checked_response_content, response,dictID,s,rawFile_time):
    try:
        sessionNav1 = control.get(scraperParameterName, 'E_NAVL1').split('|')
        if sessionNav1[0] == 'URL':
            session = str(sessionNav1[1].replace('SESSION{', '').replace('}', ''))
            if 'URL' in session:
                sessionUrl = str(session.replace('URL#', '').replace('#', ''))
                # print "session URL::", sessionUrl
            elif 'REGEX' in session:
                regex = str(session.replace('REGEX#', '').replace('#', ''))
                regexUrl = re.findall(regex, checked_response_content, re.I)
                with open("content.txt","wb") as f:
                    f.write(str(checked_response_content))
                # print "regexUrl:",regexUrl
                homeUrl = urlparse(get_url_to_scrape)
                base = homeUrl[0] + '://' + homeUrl[1]
                print "base",base,regexUrl
                if 'http:' in regexUrl[0]:
                    baseUrl = regexUrl[0]
                elif 'www.' in regexUrl[0]:
                    baseUrl = regexUrl[0]
                else:
                    regexUrl = '/' + regexUrl[0]
                    regexUrl = re.sub(r'//', '/', regexUrl)
                    sessionUrl = base + regexUrl
            # print "sessionUrl:",sessionUrl
            if 'GET' in sessionNav1[2]:
                # print "sessionNav1[2]:",sessionNav1[2]
                head = eval(str(sessionNav1[2].replace('GET(', '').replace(')', '')))
                # print "head:",type(head)
                header = date_function(DataSourceID, str(head), control, datasourceName, marketName)
                # print "header:",header
                header = ast.literal_eval(header)
                # print "header:",header
                response = s.get(sessionUrl, headers=header, verify=False)
                # response_content = response.content
                content = response.content
                status = response.status_code
                response_content = check_status(sessionUrl, status, content, DataSourceID)

                raw_file = file_writing(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,control,response_content,'n/a',rawFile_time)
            elif 'POST' in sessionNav1[2]:
                head = str(sessionNav1[2].replace('POST(', '').replace(')', ''))
                header = ast.literal_eval(head)
                post_data = control.get(scraperParameterName, 'E_POSTCONTENT')
                post_data = date_function(DataSourceID,post_data,control,datasourceName,marketName)

                post_url = control.get(scraperParameterName, 'E_POSTURL')
                post_url = date_function(DataSourceID,post_url,control,datasourceName,marketName)

                header = date_function(DataSourceID,str(head),control,datasourceName,marketName)
                header = ast.literal_eval(header)

                '''Requesting content by post method'''
                post_response = s.post(url=sessionUrl, data=post_data, cookies=response.cookies, headers=header,verify=False)
                # response = s.get(sessionUrl, headers=header, verify=False)
                postResponse_content = post_response.content
                content = response.content
                status = response.status_code
                postResponse_content = check_status(sessionUrl, status, postResponse_content, DataSourceID)
                raw_file = file_writing(DataSourceID,datasourceName, marketName, scraperParameterName, scraperType, control,
                                        postResponse_content,
                                        'n/a',rawFile_time)
        return raw_file

    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()

##########################################'''EEx backfill function'''####################################################
def eexBackFill(DataSourceID, url, control, datasourceName, marketName, backFillEnd):
    try:

        startDate = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')

        '''Date change in url'''
        if re.findall(r'\{DD(\W)(\d+)\}', str(url)):
            dateRegex = re.findall(r'\{DD(\W\d+)\}', url, re.I)
            for regex in dateRegex:
                # startDate = datetime.strptime(str(backFillEnd), '%Y-%m-%d')
                PreviousDay = startDate + relativedelta(days=int(regex))
                day_value = "{DD\\" + regex + "}"
                url = re.sub(str(day_value), str(PreviousDay.strftime('%d')), url)
                month_value = "{MM\\" + regex + "}"
                url = re.sub(month_value, PreviousDay.strftime('%m'), url)
                year_value = "{YYYY\\" + regex + "}"
                url = re.sub(year_value, PreviousDay.strftime('%Y'), url)

        '''if {DD}{MM}{YYYY} in the url,It will be replaced with backFillStart or backFillEnd date'''
        url = url.replace('{YYYY}', str(startDate.strftime('%Y')))
        url = url.replace('{DD}', str(startDate.strftime("%d")))
        url = url.replace('{MM}', str(startDate.strftime("%m")))

        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()


##########################################'''single Date backfill'''####################################################
def singleDate_backFill(DataSourceID,url,control,datasourceName,marketName,backFillEnd):
    try:

        startDate = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
        if str(datasourceName) == 'eex':
            url = eexBackFill(DataSourceID, url, control, datasourceName, marketName, backFillEnd)
        else:
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
            url = url.replace('{HH:MIN}', time.strftime("%H:%M"))
        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()




##########################################'''back filling function'''######################################################
def backfilling(DataSourceID,url,control,datasourceName,marketName):
    try:

        backFillStart = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillFrom")
        backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
        if str(backFillStart) == str(backFillEnd):
            url=singleDate_backFill(DataSourceID,url,control,datasourceName,marketName,backFillEnd)
        elif str(backFillStart) != str(backFillEnd):
            # print ""

            EndDate = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
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

                        url = url.replace('{YYYY}', str(EndDate.strftime('%Y')))
                        url = url.replace('{DD}', str(EndDate.strftime("%d")))
                        url = url.replace('{MM}', str(EndDate.strftime("%m")))
                    elif '+' in List[0]:
                        url = url.replace('{YYYY}', str(startDate.strftime('%Y')))
                        url = url.replace('{DD}', str(startDate.strftime("%d")))
                        url = url.replace('{MM}', str(startDate.strftime("%m")))


                        day_value = "{DD\\" + List[0] + List[1] + "}"
                        url = re.sub(str(day_value), str(EndDate.strftime('%d')), url)
                        month_value = "{MM\\" + List[0] + List[1] + "}"
                        url = re.sub(str(month_value), str(EndDate.strftime('%m')), url)
                        year_value = "{YYYY\\" + List[0] + List[1] + "}"
                        url = re.sub(str(year_value), str(EndDate.strftime('%Y')), url)

            url = url.replace('{HH:MIN}', time.strftime("%H:%M"))
            Interval = control.get('backfilling-' + str(marketName), 'E_INTERVAL')
            if int(Interval) > 1:
                Interval = EndDate
            elif int(Interval) == 1:
                Interval = startDate
            url = url.replace('{YYYY}', str(Interval.strftime('%Y')))
            url = url.replace('{DD}', str(Interval.strftime("%d")))
            url = url.replace('{MM}', str(Interval.strftime("%m")))
            if re.search(r'\{MONTH(\W)(\d+)', str(url)) or '{MONTH}' in url:
                url = MonthChange(DataSourceID, url, control, datasourceName, marketName)

        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()
##########################################'''Month change in the url'''####################################################
def MonthChange(DataSourceID,url,control,datasourceName,marketName):
    try:

        ItalianMonth = {'01': 'Gennaio', '02': 'Febbraio', '03': 'Marzo', '04': 'Aprile', '05': 'Maggio',
                        '06': 'Giugno','07': 'Luglio ', '08': 'Agosto', '09': 'Settembre', '10': 'ottobre', '11': 'novembre','12': 'dicembre'}
        RomanianMonth = {'01': 'ianuarie', '02': 'februarie', '03': 'martie', '04': 'aprilie', '05': 'mai',
                         '06': 'iunie', '07': 'iulie ', '08': 'august', '09': 'septembrie', '10': 'octombrie','11': 'noiembrie', '12': 'decembrie'}

        if re.search(r'\{MONTH(\W)(\d+)', str(url)):
            monthNo = re.findall(r'\{MONTH(\W\d+)', url, re.I)
            for no in monthNo:
                try:
                    if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                        backFillStart = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillFrom")
                        now = datetime.strptime(str(backFillStart), '%Y-%m-%d %H:%M:%S')
                    else:
                        raise Exception
                except Exception as e:
                    now = datetime.now()

                previousMonth = now + relativedelta(months=int(no))
                monthName = "{MONTH" + str(no) + '}'
                yearMonth = "{YYYY" + str(no) + '}'
                if yearMonth not in url:
                    Pcases = str((previousMonth.strftime("%b")).upper()) + '|' + \
                             str((previousMonth.strftime("%b")).lower()) + '|' + \
                             str(titlecase(previousMonth.strftime("%b"))) + '|' + \
                             str((previousMonth.strftime("%B")).upper()) + '|' + \
                             str((previousMonth.strftime("%B")).lower()) + '|' + \
                             str(titlecase(previousMonth.strftime("%B"))) + '|'+ \
                             str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower()) + '|'+ \
                             str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower())[0:3] + '|' + \
                             str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper()) + '|'+ \
                             str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper()) [0:3] + '|' + \
                             str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m")))))+ '|' + \
                             str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m")))))[0:3]

                    url = url.replace(monthName, Pcases)
                    # print url

                else:
                    previousMonthName = str(previousMonth.strftime("%B")).upper() + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")).upper() + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%B")).lower() + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")).lower() + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%B")) + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")) + '  ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).lower()) + '  ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).lower())[0:3] + '  ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).upper()) + '  ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).upper())[0:3] + '  ' + yearMonth + '|' + \
                                        titlecase(ItalianMonth.get(str(previousMonth.strftime("%m"))))[0:3] + '  ' + yearMonth + '|' + \
                                        titlecase(ItalianMonth.get(str(previousMonth.strftime("%m")))) + '  ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%B")).upper() + ' ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")).upper() + ' ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%B")).lower() + ' ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")).lower() + ' ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%B")) + ' ' + yearMonth + '|' + \
                                        str(previousMonth.strftime("%b")) + ' ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).lower()) + ' ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).lower())[0:3] + ' ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).upper()) + ' ' + yearMonth + '|' + \
                                        str(ItalianMonth.get(str(previousMonth.strftime("%m"))).upper())[0:3] + ' ' + yearMonth + '|' + \
                                        titlecase(ItalianMonth.get(str(previousMonth.strftime("%m"))))[0:3] + ' ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower()) + ' ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower())[0:3] + ' ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper()) + '|' + ' ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper())[0:3] + ' ' + yearMonth + '|' + \
                                        str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m"))))) + ' ' + yearMonth + '|' + \
                                        str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m")))))[0:3]+ ' ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower()) + '  ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).lower())[0:3] + '  ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper()) + '  ' + yearMonth + '|' + \
                                        str(RomanianMonth.get(str(previousMonth.strftime("%m"))).upper())[0:3] + '  ' + yearMonth + '|' + \
                                        str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m"))))) + '  ' + yearMonth + '|' + \
                                        str(titlecase(RomanianMonth.get(str(previousMonth.strftime("%m")))))[0:3] + '  ' + yearMonth + '|' + \
                                        titlecase(ItalianMonth.get(str(previousMonth.strftime("%m"))))
                    # print "previousMonthName:", previousMonthName
                    if '+' in monthName:
                        monthName = "{MONTH\\" + str(no) + '}'
                    url = re.sub(monthName, previousMonthName, url)
                    url = re.sub(yearMonth, str(previousMonth.strftime("%Y")), url)

        if '{MONTH}' in url:
            # now1 = datetime.now()
            # time = now1 + relativedelta(months=int(no))
            cases = str((time.strftime("%b")).upper()) + '|' + str(
                (time.strftime("%b")).lower()) + '|' + str(titlecase(time.strftime("%b"))) + '|' + str(
                (time.strftime("%B")).upper()) + '|' + str((time.strftime("%B")).lower()) + '|' + str(
                titlecase(time.strftime("%B")))+'|'+ \
                        str(RomanianMonth.get(str(time.strftime("%m"))).lower()) + '|'+ \
                     str(RomanianMonth.get(str(time.strftime("%m"))).lower())[0:3] + '|' + \
                     str(RomanianMonth.get(str(time.strftime("%m"))).upper()) + '|'+ \
                     str(RomanianMonth.get(str(time.strftime("%m"))).upper()) [0:3] + '|' + \
                     str(titlecase(RomanianMonth.get(str(time.strftime("%m")))))+ '|' + \
                     str(titlecase(RomanianMonth.get(str(time.strftime("%m")))))[0:3]

            if '{YYYY}' in url:
                monthName = str(ItalianMonth.get(str(time.strftime("%m"))).lower())[0:3] + '  {YYYY}|' + str(
                    ItalianMonth.get(str(time.strftime("%m"))).upper())[0:3] + '  {YYYY}|' + \
                    titlecase(ItalianMonth.get(str(time.strftime("%m"))))[0:3] + '  {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).lower()) + '  {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).upper()) + '  {YYYY}|' + \
                    titlecase(ItalianMonth.get(str(time.strftime("%m")))) + '  {YYYY}|' + \
                    time.strftime("%B") + '  {YYYY}|' +\
                    str(time.strftime("%B")).lower() + '  {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).lower())[0:3] + ' {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).upper())[0:3] + ' {YYYY}|' + \
                    titlecase(ItalianMonth.get(str(time.strftime("%m"))))[0:3] + ' {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).lower()) + ' {YYYY}|' + \
                    str(ItalianMonth.get(str(time.strftime("%m"))).upper()) + ' {YYYY}|' + \
                    titlecase(ItalianMonth.get(str(time.strftime("%m")))) + ' {YYYY}|' + \
                    time.strftime("%B") + ' {YYYY}|' + \
                    str(time.strftime("%B")).lower() + ' {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).lower()) + '  {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).lower())[0:3] + '  {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).upper()) +'  {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).upper())[0:3] + '  {YYYY}|' + \
                    str(titlecase(RomanianMonth.get(str(time.strftime("%m"))))) + '  {YYYY}|' + \
                    str(titlecase(RomanianMonth.get(str(time.strftime("%m")))))[0:3]+ '  {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).lower()) + ' {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).lower())[0:3] + ' {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).upper()) + ' {YYYY}|' + \
                    str(RomanianMonth.get(str(time.strftime("%m"))).upper())[0:3] + ' {YYYY}|' + \
                    str(titlecase(RomanianMonth.get(str(time.strftime("%m"))))) + ' {YYYY}|' + \
                    str(titlecase(RomanianMonth.get(str(time.strftime("%m")))))[0:3] + ' {YYYY}|' +time.strftime("%b")
                # print "monthName:",monthName
                url = url.replace('{MONTH}', monthName).replace('{YYYY}', time.strftime("%Y"))

            else:
                url = url.replace('{MONTH}', cases)
        # print url
        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()

##########################################'''dateTry'''#################################################################
def datetry_function(DataSourceID,url,control,datasourceName,marketName,dateTry):
    try:

        if re.search(r'\{DD(\W)(\d+)\}', str(url)):
            dateRegex = re.findall(r'\{DD(\W\d+)\}', url, re.I)
            # print "dateRegex:",dateRegex
            ModifiedDateRegex = int(dateRegex[0]) - int(dateTry)
            # print "ModifiedDateRegex:",ModifiedDateRegex
            if '-' not in str(ModifiedDateRegex):
                ModifiedDateRegex ='+'+str(ModifiedDateRegex)
            # raw_input('datetry:')
            for regex in dateRegex:
                day_value = "{DD\\" + str(regex) + "}"
                dayTry_value=  "{DD" + str(ModifiedDateRegex).strip() + "}"
                # print"dayTry_value_reg",dayTry_value
                url = re.sub(str(day_value), str(dayTry_value).strip(), url)
                month_value = "{MM\\" + regex + "}"
                monthTry_value = "{MM" +  str(ModifiedDateRegex) + "}"
                url = re.sub(str(month_value), str(monthTry_value).strip(), url)
                year_value = "{YYYY\\" + regex + "}"
                yearTry_value = "{YYYY" +  str(ModifiedDateRegex) + "}"
                url = re.sub(str(year_value), str(yearTry_value).strip(), url)
        if '{DD}' in url:
            loopDate="{DD" + '-' + str(dateTry) +"}"
            url=url.replace('{DD}', loopDate)
            loopMonth = "{MM" + '-' + str(dateTry) + "}"
            url = url.replace('{MM}', loopMonth)
            loopYear = "{YYYY" + '-' + str(dateTry) + "}"
            url = url.replace('{YYYY}', loopYear)

        # url = re.sub(r'\s+\s*','',str(url))
        # print "datetry url:",url

        return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()
##########################################'''to find date in the url'''####################################################
'''url with date'''

def date_function(DataSourceID,url,control,datasourceName,marketName):
    try:
        if '{YYYY}' and '{MM}' and '{DD}' or '{YY}' or '{DD-' or '{ITA-MNAME}' or '{HH:MIN}' or '{ENG-MNAME}' or '{YYYY-' or '{MM-' or '{MM+' or '{YYYY+' in url:
            try:
                if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill")=='YES':
                    url=backfilling(DataSourceID, url, control, datasourceName, marketName)
                else:
                    raise Exception

            except Exception as e:
                try:
                    if control.get('backfilling-' + str(marketName), 'E_BACKDATEDDATA')=='YES':
                        dateTry = control.get('BackDatedData-' + str(marketName), str(datasourceName) + "BackData")
                        # print "E_BACKDATEDDATA flow:",dateTry
                        url = datetry_function(DataSourceID,url,control,datasourceName,marketName,str(dateTry))
                    else:
                        raise Exception
                except Exception as e:
                    pass
                    # sys.exit()


                # print "url after date try:",url
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

                if re.search(r'\{MONTH(\W)(\d+)', str(url)) or '{MONTH}' in url:
                    url=MonthChange(DataSourceID,url,control,datasourceName,marketName)

                url = url.replace('{MM}', time.strftime("%m"))
                if re.search(r'\{YYYY(\W)(\d+)', str(url)):
                    yearRegex = re.findall(r'\{YYYY(\W\d+)\}', url, re.I)
                    for regex in yearRegex:
                        PreviousYear = now + relativedelta(years=int(regex))
                        yearValue = "{YYYY\\" + str(regex) + '}'
                        url = re.sub(yearValue, PreviousYear.strftime('%Y'), url)

                url = url.replace('{YYYY}', time.strftime("%Y"))

                url = url.replace('{HH:MIN}', time.strftime("%H:%M"))


                # print "normal flow url:",url
                return url
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        sys.exit()
######################Merging file#########################################
def mergeFile(DataSourceID, datasourceName, marketName, spName, control, fileList):

    try:

        try:
            if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill")=='YES':
                backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                backFillEnd = datetime.strptime(str(backFillEnd),'%Y-%m-%d %H:%M:%S')
                date_time = str(backFillEnd.strftime('%Y%m%d_%H%M%S'))
            else:
                raise Exception
        except Exception as e:
            date_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

        '''csv to csv'''
        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        # rawFileName = tempFilePath + str(rawFile_time).replace('-', '_') + ".xlsx"

        wb = xlwt.Workbook()
        # wb = xlsxwriter.Workbook(rawFileName)

        # wb = xlwt.Workbook()
        for scraper_parameters in spName:
            scraperParameterName = 'E-' + str(datasourceName) + '-' + str(marketName) + '-' + str(scraper_parameters).strip()


            if control.get(scraperParameterName, 'E_CSV_VALUES_REGEX') != 'n/a':

                csvRegex = control.get(scraperParameterName, 'E_CSV_VALUES_REGEX')
                csvValue = csvRegex.replace('REGEX{', '').replace('}', '')

                rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".csv"

                c = csv.writer(open(rawFileName, "ab"))

                for files in fileList:

                    if str(scraperParameterName) in files:

                        spamReader = csv.reader(open(files, 'rb'))
                        for row in spamReader:
                            if re.search(str(csvValue), str(row[0])) is not None:
                                c.writerow(row)
            else:
                '''csv to excel'''
                rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"

                '''Creating workbook'''
                i = 0
                for files in fileList:

                    if str(scraper_parameters) in files:

                        if '.csv' in files:
                            deLimiter = control.get('default', 'E_DELIMITER')
                            spamReader = csv.reader(open(files, 'rb'), delimiter=(deLimiter.replace('VAL','').replace('{','').replace('}','')).strip())
                            name_regex_length = re.search(r'[^<]*?E\-[^<]+\-\s*([^<]*?\-[^<]+)$\s*', files, re.I)
                            f_short_name = name_regex_length.group(1)
                            sheetname=str(scraper_parameters)
                            print "sheetname:",sheetname
                            ws = wb.add_sheet(str(sheetname))
                            try:
                                if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                                    # print "url date"
                                    dateUrl = (control.get(scraperParameterName, 'URL_DATE')).split('|')
                                    dateUrlList = re.findall(dateUrl[1], date_function(DataSourceID,control.get(scraperParameterName,'URL'), control,datasourceName, marketName))
                                    # print "dateUrlList:", dateUrlList
                                    ws.write(0, 0, dateUrlList[0])
                            except:
                                pass
                            # ws = wb.add_worksheet(str(scraper_parameters))
                            for rowx, row in enumerate(spamReader):
                                for colx, value in enumerate(row):
                                    try:
                                        if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                                            ws.write(rowx + 1, colx,unicode(value, errors="ignore"))
                                        else:
                                            raise Exception
                                    except:
                                        ws.write(rowx, colx, unicode(value, errors="ignore"))
                                    # ws.write(rowx, colx, unicode(value, errors="ignore"))

                        elif '.xls' in files or '.xlsx' in files:

                            insheet = xlrd.open_workbook(files)
                            input_list_sheet = insheet.sheets()
                            sheet_count = len(insheet.sheets())
                            for c in range(sheet_count):
                                sh = insheet.sheet_by_index(c)
                                if (sh.nrows > 0):
                                    sheet_name = str(scraper_parameters) + str(i)
                                    outsheet = wb.add_sheet(sheet_name)
                                    # outsheet = wb.add_worksheet(sheet_name)
                                    i = i + 1
                                    try:
                                        if (control.get(scraperParameterName, 'URL_DATE')) != 'n/a':
                                            dateUrl = (control.get(scraperParameterName, 'URL_DATE')).split('|')
                                            dateUrlList = re.findall(dateUrl[1], date_function(DataSourceID,control.get(scraperParameterName,'URL'), control,datasourceName,marketName))
                                            outsheet.write(0, 0, dateUrlList[0])
                                            for row_idx in xrange(sh.nrows):
                                                for col_idx in xrange(sh.ncols):
                                                    outsheet.write(row_idx + 1, col_idx,
                                                                   sh.cell_value(row_idx, col_idx))
                                        else:
                                            raise Exception
                                    except:
                                        for row_idx in xrange(sh.nrows):
                                            for col_idx in xrange(sh.ncols):
                                                outsheet.write(row_idx, col_idx, sh.cell_value(row_idx, col_idx))

                                    try:
                                        if control.get("default", str(scraperParameterName) + "PUBLISHED") != 'n/a':
                                            outsheet.write(row_idx + 1, col_idx, str(
                                                control.get("default", str(scraperParameterName) + "PUBLISHED")))
                                    except:
                                        pass
                wb.save(rawFileName)
                # wb.close()

        return rawFileName, True
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        return 'n/a', False
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

        List = []
        rawFile = ''

        '''creating file name'''
        try:
            if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                backFillEnd = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
                date_time = str(backFillEnd.strftime('%Y%m%d_%H%M%S'))
                backFillEnd = str(backFillEnd.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                raise Exception
        except Exception as e:
            backFillEnd = ''
            date_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time

        '''looping through the scraper parameter name'''
        for scraper_parameters in spName:
            scraperParameterName = 'E-' + str(datasourceName) + '-' + str(marketName) + '-' + str(
                scraper_parameters).strip()
            # print scraperParameterName

            '''getting url from scraperparameter'''
            get_url_to_scrape_date = control.get(scraperParameterName, 'URL')
            # print get_url_to_scrape_date


            '''calling date function and return the updated url (Embed date within the URL)'''
            get_url_to_scrape = date_function(DataSourceID,get_url_to_scrape_date,control,datasourceName,marketName)
            # print "main url to get response:",get_url_to_scrape

            method = control.get(scraperParameterName, 'E_METHOD').split('|')

            scraperType = control.get(scraperParameterName, 'SCRAPERTYPE').lower()


            if 'ftp' in get_url_to_scrape:
                rawFile = ftp_function(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,
                                       control, get_url_to_scrape,rawFile_time)

                List.append(rawFile)

            else:
                '''E_method will download the corresponding file by calling 3 functions and push it to raw file'''
                if method[0] in ("GET", 'GET_BY'):
                    cookie_file = '/tmp/cookies'
                    cj = cookielib.LWPCookieJar(cookie_file)

                    s = requests.Session()
                    s.cookies = cj
                    s = requests.Session()
                    head = method[1]
                    header = ast.literal_eval(head)

                    try:
                        if method[2]:
                            verify = ast.literal_eval(method[2])
                            response = s.get(get_url_to_scrape, headers=header, verify=verify)
                    except:
                        response = s.get(get_url_to_scrape, headers=header)

                    response_content = response.content
                    status = response.status_code
                    ck = s.cookies.get_dict()
                    # print "ck:",ck
                    try:
                        if str(ck)!='{}':
                            dictID = ck.get(control.get(scraperParameterName, 'DICT_ID'))
                            # print "dictID:", dictID
                            checked_response_content = check_status(get_url_to_scrape, status, response_content,
                                                                    DataSourceID)
                            '''finding the content type of the url'''

                            content_type = url_content_type(get_url_to_scrape, response, scraperType)
                            # print content_type
                            '''downloading the extracted file and pushed to s3'''
                            rawFile = sessionfile(DataSourceID, datasourceName, marketName, scraperParameterName,
                                                       scraperType, get_url_to_scrape, method[0], control, content_type,
                                                       checked_response_content, response,dictID,s,rawFile_time)

                            List.append(rawFile)

                        elif  str(ck)=='{}':
                            raise Exception
                    except:

                        '''check whether url is working with status and getting response content'''
                        checked_response_content = check_status(get_url_to_scrape, status, response_content, DataSourceID)
                        '''finding the content type of the url'''

                        content_type = url_content_type(get_url_to_scrape, response, scraperType)
                        # print content_type


                        '''downloading the extracted file and pushed to s3'''

                        rawFile = downloading_file(DataSourceID, datasourceName, marketName, scraperParameterName,scraperType, get_url_to_scrape, method[0], control, content_type,checked_response_content, response,rawFile_time)

                        List.append(rawFile)


                elif method[0] == "POST":
                    head = method[1]
                    rawFile = post_method(DataSourceID, datasourceName, marketName, scraperParameterName, scraperType,control, get_url_to_scrape, head,rawFile_time)
                    List.append(rawFile)

        # print "List", List

        '''Removing empty list '''
        List = remove_empty(List)

        '''Joining all List'''
        if sum(isinstance(i, list) for i in List) != 0:
            fileList = list(itertools.chain.from_iterable(List))
        else:
            fileList = List
        # print "fileList:", fileList
        '''Removing Duplications in the List'''
        fileList = list(set(fileList))

        # print "fileList:", fileList
        successStatus = 1
        s3File = ''

        '''If FileList is 1 returning that file to s3'''
        if len(fileList) == 1:

            xlsFile, csvFile = '', ''

            if '.xls' in str(fileList[0]) or '.xlsx' in str(fileList[0]):
                xlsFile = fileList[0]
            elif '.csv' in str(fileList[0]):
                csvFile = fileList[0]
                # print "csvFile:",csvFile

            if len(xlsFile) > 0:
                cookedFile, status = mergeFile(DataSourceID, datasourceName, marketName, spName, control, fileList)
                if cookedFile != 'n/a':
                    s3File = cookedFile
                else:
                    successStatus = 0
                    print 'fileList Error for lenth ==1'
            elif len(csvFile) > 0:
                if 'eex' in datasourceName:
                    cookedFile, status = mergeFile(DataSourceID, datasourceName, marketName, spName, control, fileList)
                    if cookedFile != 'n/a':
                        s3File = cookedFile
                    else:
                        successStatus = 0
                else:
                    try:
                        if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                            backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                            backFillEnd = datetime.strptime(str(backFillEnd), '%Y-%m-%d %H:%M:%S')
                            date_time = str(backFillEnd.strftime('%Y%m%d_%H%M%S'))
                        else:
                            raise Exception
                    except Exception as e:
                        date_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
                    # date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
                    rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
                    rawFileName = tempFilePath + str(rawFile_time).replace('-', '_') + '.csv'
                    os.rename(csvFile, rawFileName)
                    s3File = rawFileName
            else:
                s3File = fileList[0]

        elif len(fileList) > 1:
            '''File merging takes place '''
            cookedFile, status = mergeFile(DataSourceID, datasourceName, marketName, spName, control, fileList)
            if cookedFile != 'n/a':
                s3File = cookedFile
            else:
                successStatus = 0
                print 'fileList Error for length >1'
        elif len(fileList) < 1:
            successStatus = 0
            print "fileList error for length ,1"

        print "s3File:", s3File
        if len(s3File)==0:
            Fundalytics_Utility.log(DataSourceID, 'Extract',str("Expected file is not found|" + str(datasourceName)) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
            sys.exit()


        if successStatus == 1:

            # Fundalytics_Utility.s3_fileupload(s3File, DataSourceID, s3path_upload, 'Extract', control)

            # print "Uploaded Completed"

            Fundalytics_Utility.log(DataSourceID, 'Extract-Module', '', 'Extracted',
                                    str(s3path_upload) + str(str(s3File).replace(tempFilePath, '')))
            control.add_section('status')

            control.add_section('filename')
            control.set("filename", "extractfilename", str(s3File).replace(tempFilePath, ''))
            # try:
                # os.remove(tempFilePath)
            # except:
                # pass
            # try:
                # for filename in fileList:
                    # os.remove(filename)
            # except:
                # pass
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
