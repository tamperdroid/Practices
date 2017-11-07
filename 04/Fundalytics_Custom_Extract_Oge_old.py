# -*- coding: utf-8 -*-
'''
    Project : "ArgusMedia"
    Module Name: Fundalytics_Custom_Extract_gas_filter.py
    Created Date: 2016-07-13
    Scope: To download and push the file into s3 raw folder.

    Version:V1: 2016-09-29
    Details:
'''

import requests
import re
import time
from datetime import datetime
import titlecase
import ast
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import json
import ConfigParser
import sys,os,imp,xlrd,itertools
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/Arul/Python-projects/Argus-media/Intergeration_v3-local/Fundalytics_Utility.py')
# Fundalytics_Utility = imp.load_source('Fundalytics_Utility', '/home/merit/argusmedia/Fundalytics_Utility.py')
# import Fundalytics_Utility
import titlecase,csv
import cookielib,glob,xlwt,xlsxwriter
from titlecase import titlecase
from datetime import date, timedelta
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))

tempFilePath="D:/Arul/Python-projects/Argus-media/Intergeration_v3-local/"
# tempFilePath = "/home/merit/argusmedia/temp/"

if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)

def getcontent(DataSourceID,url,datasourceName, marketName, scraperType,scraperParameterName):
    try:
        home_url = url
        # home_url='https://transparencybo.open-grid-europe.com/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=Fg2WdlFONAEAx3YAAEBpdUUDPEqSdH7y&sIDType=CUID&user=INET_USER'
        s = requests.Session()

        con = s.get(home_url, verify=False)
        home_con = con.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        # Get openDocument.faces url
        Application_Parameters_list = re.findall('getUrlWithApplicationParameters\s*\(\"\s*[\.\/]+([^>]*?)\"\s*\)',
                                                 str(home_con), re.IGNORECASE)
        Application_Parameters = ''
        if (Application_Parameters_list):
            Application_Parameters = Application_Parameters_list[0]

        nextposturl = 'https://transparencybo.open-grid-europe.com/BOE/' + Application_Parameters;
        Post_cont1 = 'isApplication=true&appKind=OpenDocument&iDocID=Fg2WdlFONAEAx3YAAEBpdUUDPEqSdH7y&sIDType=CUID&user=INET_USER'
        Headers1 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "https://transparencybo.open-grid-europe.com/BOE/OpenDocument/opendoc/openDocument.jsp?iDocID=Fg2WdlFONAEAx3YAAEBpdUUDPEqSdH7y",
                    "Content-Type": "application/x-www-form-urlencoded"}
        nextpostcont = s.post(nextposturl, data=Post_cont1, headers=Headers1, verify=False);
        Post_Content1 = nextpostcont.content

        # Get "DocID"
        iDocID_List = re.findall('\"iDocID\"\s*value\=\s*\"([^>]*?)\"', str(Post_Content1), re.IGNORECASE)
        iDocID = ''
        if (iDocID_List):
            iDocID = iDocID_List[0]

        # Get "bttoken"
        bttoken_List = re.findall('bttoken\"\s*value\=\"([^<]*?)\"', str(Post_Content1), re.IGNORECASE)
        bttoken = ''
        if (bttoken_List):
            bttoken = bttoken_List[0]

        nextsharepostcont_part1 = 'iDocID=' + iDocID + '&sIDType=CUID&isApplication=true&bttoken=' + bttoken + '&appKind=OpenDocument&user=INET_USER'

        nextshareposturl = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/OpenDocument/opendoc/openDocument.faces?logonSuccessful=true&shareId=0';
        Headers2 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/OpenDocument/opendoc/openDocument.faces",
                    "Content-Type": "application/x-www-form-urlencoded"}

        nextsharepostcont = s.post(nextshareposturl, data=nextsharepostcont_part1, headers=Headers2, verify=False);
        Post_Content2 = nextsharepostcont.content

        # Get "bttoken"
        bttoken2_list = re.findall('bttoken\=([\w]+)\&', str(Post_Content2), re.IGNORECASE)
        bttoken2 = ''
        if (bttoken2_list):
            bttoken2 = bttoken2_list[0]

        # Get "appCUID"
        appCUID_list = re.findall('appCUID\s*\=\s*\"([^\"]*?)\"\;', str(Post_Content2), re.IGNORECASE)
        appCUID = ''
        if (appCUID_list):
            appCUID = appCUID_list[0]

        webiview_url = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/WebiView.do'
        webiview_post_cont = 'bypassLatestInstance=true&cafWebSesInit=true&bttoken=' + bttoken2 + '&appKind=OpenDocument&appCUID=' + appCUID + '&service=%2FOpenDocument%2FappService.do&loc=de&pvl=de_DE&actId=4174&objIds=48144&containerId=47996&shareId=0&isApplication=true&bttoken=' + bttoken2 + '&logonSuccessful=true&user=INET_USER&pref=maxOpageU%3D10%3BmaxOpageUt%3D200%3BmaxOpageC%3D10%3Btz%3DEurope%2FBerlin%3BmUnit%3Dinch%3BshowFilters%3Dtrue%3BsmtpFrom%3Dtrue%3BpromptForUnsavedData%3Dtrue%3B'

        Headers3 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": nextshareposturl,
                    "Content-Type": "application/x-www-form-urlencoded"}

        webiview_content = s.post(webiview_url, data=webiview_post_cont, headers=Headers3, verify=False)
        Post_Content3 = webiview_content.content

        appurl = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/viewDocument.jsp'

        view_doc_post_Cont = 'id=48144&bypassLatestInstance=true&cafWebSesInit=true&bttoken=' + bttoken2 + '&appKind=OpenDocument&appCUID=' + appCUID + '&service=%2FOpenDocument%2FappService.do&loc=de&pvl=de_DE&actId=4174&objIds=48144&containerId=47996&shareId=1&isApplication=true&logonSuccessful=true&user=INET_USER&pref=maxOpageU%3D10%3BmaxOpageUt%3D200%3BmaxOpageC%3D10%3Btz%3DEurope%2FBerlin%3BmUnit%3Dinch%3BshowFilters%3Dtrue%3BsmtpFrom%3Dtrue%3BpromptForUnsavedData%3Dtrue%3B&kind=Webi&iventrystore=widtoken&ViewType=H&entSession=CE_ENTERPRISESESSION&lang=de'

        Headers4 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/WebiView.do",
                    "Content-Type": "application/x-www-form-urlencoded"}

        appurlcont = s.post(appurl, data=view_doc_post_Cont, headers=Headers4, verify=False)
        Post_Content4 = appurlcont.content

        # Get "strEntry"
        strEntry_list = re.findall('strEntry\"\s*\:\s*\"([^>]*?)\"\s*\,', str(Post_Content4), re.IGNORECASE)
        strEntry = ''
        if (strEntry_list):
            strEntry = strEntry_list[0]

        report_url1 = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/report.jsp?iViewerID=1&sEntry=' + strEntry + '&iReport=0&iReportID=1&sPageMode=&sReportMode=Analysis&iPage=&iFoldPanel=0&zoom=100&isInteractive=false&isStructure=false&sBid=';
        Headers5 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": appurl}

        reportcontent1 = s.get(report_url1, headers=Headers5, verify=False)
        report1_cont = reportcontent1.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        report_url2 = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/viewReport.jsp?iViewerID=1&sEntry=' + strEntry + '&iReport=0&iReportID=1&sPageMode=&sReportMode=Analysis&iPage=&iFoldPanel=0&zoom=100&isInteractive=false&isStructure=false&sBid=';
        Headers6 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": report_url1}

        reportcontent2 = s.get(report_url2, headers=Headers6, verify=False)
        report2_cont = reportcontent2.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        refresh_url1 = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/refreshDocument.jsp?iViewerID=1&sEntry=' + strEntry + '&iReport=0&iReportID=1&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&isStructure=false&nbPage=NaN&sEmptyLab=%5BEMPTY_VALUE%5D&sUndoEnabled=false';
        Headers7 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": appurl}

        refreshcontent2 = s.get(refresh_url1, headers=Headers7, verify=False)
        refresh_cont = refreshcontent2.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        # Get "strEntry"
        strEntry_list = re.findall('sEntry\=([\w]+)', str(refresh_cont), re.IGNORECASE)
        strEntry2 = ''
        if (strEntry_list):
            strEntry2 = strEntry_list[0]

        report_url3 = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/report.jsp?iViewerID=1&sEntry=' + strEntry2 + '&iReport=0&iReportID=1&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&isStructure=false&nbPage=NaN&sEmptyLab=%5BEMPTY_VALUE%5D&sUndoEnabled=false'
        Headers8 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Cookie": "JSESSIONID=" + JsessionID + "; SessionID=" + SessionID,
                    "Referer": refresh_url1}

        refresh_url_cont = s.get(report_url3, headers=Headers8, verify=False)
        report3_cont = refresh_url_cont.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        report_url4 = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/viewReport.jsp?iViewerID=1&sEntry=' + strEntry2 + '&iReport=0&iReportID=1&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&isStructure=false&nbPage=NaN&sEmptyLab=%5BEMPTY_VALUE%5D&sUndoEnabled=false'

        Headers9 = {"Host": "transparencybo.open-grid-europe.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Cookie": "JSESSIONID=" + JsessionID + "; SessionID=" + SessionID,
                    "Referer": report_url3}

        refresh_url_cont = s.get(report_url4, headers=Headers9, verify=False)
        report4_cont = refresh_url_cont.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        select_xls = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/viewer/downloadPDForXLS.jsp?iViewerID=1&sEntry=' + strEntry2 + '&iReport=0&iReportID=1&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&isStructure=false&doctype=wid&viewType=XO&saveReport=N'
        Headers10 = {"Host": "transparencybo.open-grid-europe.com",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Language": "en-US,en;q=0.5",
                     "Accept-Encoding": "gzip, deflate, br",
                     "Cookie": "JSESSIONID=" + JsessionID + "; SessionID=" + SessionID,
                     "Referer": appurl}

        refresh_url_cont = s.get(select_xls, headers=Headers10, verify=False)
        selectxls_cont = refresh_url_cont.content
        ck = s.cookies.get_dict()
        SessionID = ck.get("SessionID")
        JsessionID = ck.get("JSESSIONID")

        xls_url = 'https://transparencybo.open-grid-europe.com/BOE/OpenDocument/1608031852/AnalyticalReporting/webiDHTML/DownloadPDForXLS/T2.1-SB-02_v1.00_EN.xlsx';
        Headers11 = {"Host": "transparencybo.open-grid-europe.com",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Language": "en-US,en;q=0.5",
                     "Accept-Encoding": "gzip, deflate, br",
                     "Referer": select_xls}

        refresh_url_cont = s.get(xls_url, headers=Headers11, verify=False)
        xls_cont = refresh_url_cont.content

        Temp_rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_Temp_' + date_time
        Temp_rawFileName = tempFilePath + str(Temp_rawFile_time).replace('-', '_') + '.' + scraperType

        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        rawFileName = tempFilePath + str(rawFile_time).replace('-', '_') + '.' + scraperType

        with open(Temp_rawFileName, 'ab') as f:
            f.write(xls_cont)

        insheet = xlrd.open_workbook(Temp_rawFileName)
        input_list_sheet = insheet.sheet_names()
        # Sheet_Name = insheet.sheet_name()
        print "Sheet_Name:", input_list_sheet
        print "rawFileName:", rawFileName

        wb = xlsxwriter.Workbook(rawFileName)
        outsheet = wb.add_worksheet(input_list_sheet[0])

        sh = insheet.sheet_by_name(input_list_sheet[0])

        for col_idx in range(0, sh.ncols):
            for row_idx in range(0, sh.nrows):
                Value = sh.cell_value(row_idx, col_idx)
                # print "Value:", row_idx, col_idx, Value
                if (col_idx == 1):
                    Value = str(Value).replace('00:00 - 01:00', '24:00 - 25:00')
                    Value = str(Value).replace('01:00 - 02:00', '25:00 - 26:00')
                    Value = str(Value).replace('02:00 - 03:00', '26:00 - 27:00')
                    Value = str(Value).replace('03:00 - 04:00', '27:00 - 28:00')
                    Value = str(Value).replace('04:00 - 05:00', '28:00 - 29:00')
                    Value = str(Value).replace('05:00 - 06:00', '29:00 - 30:00')
                outsheet.write(row_idx, col_idx, Value)

        wb.close()
        os.remove(Temp_rawFileName)
        return rawFileName
    except Exception as e:
        print str(e) + str(sys.exc_traceback.tb_lineno)
        # print"error********"
        print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error', '')
        return 'n/a', False
        sys.exit()
		
#############################################################Main function##############################################
# if __name__ == "__main__":
def main(control):
    try:
        '''Get all the arguments from scrapy'''
        DataSourceID = control.dsId
        datasourceName = control.dsName
        marketName = control.mName
        spName = control.scraperParameterName.split('/')
        # print DataSourceID, datasourceName, marketName, spName


        s3path_upload = 'data/raw/' + str(datasourceName) + '/' + str(marketName) + '/1.0/'

        List = []
        rawFile = ''
        sectionName = 'E-' + str(datasourceName) + '-' + str(marketName) + '-'
        print sectionName
        session = control.sections()

        req_sesssion = (x for x in session if sectionName in x)
        for marketSection in req_sesssion:
            print "marketSection:",marketSection
            url =control.get(marketSection, 'URL')

            method = control.get(marketSection, 'E_METHOD').split('|')
            scraperType = control.get(marketSection, 'SCRAPERTYPE').lower()

            rawFile = getcontent(DataSourceID,url, datasourceName, marketName, scraperType,marketSection)
            # print "===>",rawFile
            List.append(rawFile)



        # print "List", List

        if sum(isinstance(i, list) for i in List) != 0:
            fileList = list(itertools.chain.from_iterable(List))
        else:
            fileList = List

        fileList = list(set(fileList))
        # print 'no dulpication:',fileList


        successStatus = 1
        s3File = ''
        if len(fileList) == 1:
            s3File = fileList[0]
        elif len(fileList) > 1:
            htmlFile = [x for x in fileList if '.html' in x]
            if len(htmlFile) == 0:
                # print "sa"
                cookedFile, status = mergeFile(DataSourceID, datasourceName, marketName,control, fileList)
                if cookedFile != 'n/a':
                    s3File = cookedFile
                else:
                    successStatus = 0
                    print 'file Error'
            else:
                print "html file"
                s3File = fileList[0]
        elif len(fileList) < 1:
            successStatus = 0
            print "error"

        if successStatus == 1:
            print s3File

            # Fundalytics_Utility.s3_fileupload(s3File, DataSourceID, s3path_upload, 'Extract', control)

            print "Uploaded Completed"

            Fundalytics_Utility.log(DataSourceID, 'Extract-Module', '', 'Extracted', str(s3path_upload) + str(file))
            control.add_section('status')

            control.add_section('filename')
            control.set("filename", "extractfilename", str(s3File).replace(tempFilePath, ''))

            # for filename in fileList:
                # os.remove(filename)
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