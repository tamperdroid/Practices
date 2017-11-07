import zipfile,xlsxwriter,itertools,os,sys,imp,re,ast,requests,xlrd
from datetime import datetime
import imaplib
import email
from titlecase import titlecase
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

Fundalytics_Utility = imp.load_source('Fundalytics_Utility', '/home/merit/argusmedia/Fundalytics_Utility.py')

date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))

tempFilePath="/home/merit/argusmedia/temp/"

if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)

reload(sys)
sys.setdefaultencoding("utf-8")

def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))



def email_download(gmail_imap,imap_port,username,password):
    mail = imaplib.IMAP4_SSL(gmail_imap, imap_port)
    mail.ssl()
    mail.login(username, password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.
    svdir = '/home/merit/argusmedia/'
    result, data = mail.search(None, 'ALL', '(UNSEEN)')
    mail.select("inbox")
    # result, data = mail.uid('search', None, 'ALL',)
    try:
        result, data = mail.uid('search', None, 'ALL', '(UNSEEN)')
        uids = data[0].split()

        print uids
        result, data = mail.uid('fetch', uids[-1], '(RFC822)')
        m = email.message_from_string(data[0][1])
        if m.get_content_maintype() == 'multipart':
            print "inside"
            for part in m.walk():
                if part.get_content_maintype() == 'multipart': continue
                if part.get('Content-Disposition') is None: continue

                # save the attachment in the program directory
                filename = part.get_filename()
                fp = open(str(svdir) + "/" + str(filename), 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print '%s saved!' % filename
        return filename
    except Exception as e:
        print "Exception", e, str(sys.exc_traceback.tb_lineno)
        print "No unread mail"


def split_fun(data_to_be_split):
    data_contains_quates = data_to_be_split.split("=")
    data=data_contains_quates[1].replace("\"","")
    return data


def getcontent_2(DataSourceID, url, datasourceName, marketName, scraperType, scraperParameterName):
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
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        return 'n/a', False
        sys.exit()


def getcontent(gmail_imap,imap_port,username,password,DataSourceID,datasourceName, marketName, scraperType, scraperParameterName):
    TimeInterval_val_list = []
    try:
        zip_fileName=email_download(gmail_imap,imap_port,username,password)
        print zip_fileName
        # zf = zipfile.ZipFile("2016_12_15_Lastflussdaten.zip")
        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"
        zf = zipfile.ZipFile(zip_fileName)
        workbook = xlsxwriter.Workbook(rawFileName)
        worksheet1 = workbook.add_worksheet("email_data")
        worksheet1.write(0, 0, "ID")
        worksheet1.write(0, 1, "TransparencyPublication Version")
        worksheet1.write(0, 2, "TransparencyPublication Release")
        worksheet1.write(0, 3, "Identifcation")
        worksheet1.write(0, 4, "Version")
        worksheet1.write(0, 5, "Type")
        worksheet1.write(0, 6, "CreationDateTime")
        worksheet1.write(0, 7, "ValidityPeriod")
        worksheet1.write(0, 8, "IssuerIdentification")
        worksheet1.write(0, 9, "CodingScheme")
        worksheet1.write(0, 10, "IssuerRole")
        worksheet1.write(0, 11, "RecipientIdentification")
        worksheet1.write(0, 12, "RecipientRole")
        worksheet1.write(0, 13, "Con_identifaction")
        worksheet1.write(0, 14, "Connection codingscheme")
        worksheet1.write(0, 15, "Connection Type")
        worksheet1.write(0, 16, "CapacityCode")
        worksheet1.write(0, 17, "TimeInterval")
        worksheet1.write(0, 18, "Direction")
        worksheet1.write(0, 19, "Quantity")
        worksheet1.write(0, 20, "MeasureUnit")
        value_inc=1
        for name in zf.namelist():
            print name
            Id=re.findall("\_(\d+)\.xml",name,re.I)
            print "Id",Id
            # Id_list.append(Id[0])
            response_content = zf.read(name)
            TransparencyPlc=re.findall("<TransparencyPublication\s*(.*?)\s*>\s*(.*?)\s*</TransparencyPublication>",response_content,re.I)
            TransData=re.split("\s+",TransparencyPlc[0][0])
            #version
            version_list_pbl=split_fun(TransData[0])
            release_list=split_fun(TransData[1])
            # version_list_pblc.append(split_fun(TransData[0]))
            # release_list.append(split_fun(TransData[1]))
            singlevalues=re.findall("<Identification\s*(.*?)\s*/>\s*(.*?)\s*<ConnectionPoint",TransparencyPlc[0][1],re.I)
            #Identification
            identifcation_list=split_fun(singlevalues[0][0])
            Version=re.findall("<Version\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            Version_list=split_fun(Version[0])
            # print Version_list
            Type=re.findall("<Type\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            Type_list=split_fun(Type[0])
            # print Type_list
            CreationDateTime=re.findall("<CreationDateTime\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            CreationDateTime_list=split_fun(CreationDateTime[0])
            ValidityPeriod=re.findall("<ValidityPeriod\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            ValidityPeriod_list=split_fun(ValidityPeriod[0])
            IssuerIdentification = re.findall("<IssuerIdentification\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            IssuerIdentification = re.split("\s+", IssuerIdentification[0])
            IssuerIdentification_list=split_fun(IssuerIdentification[0])
            # print IssuerIdentification_list
            codingScheme_list=split_fun(IssuerIdentification[1])
            # print codingScheme_list
            IssuerRole = re.findall("<IssuerRole\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            IssuerRole_list=split_fun(IssuerRole[0])
            RecipientIdentification = re.findall("<RecipientIdentification\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            RecipientIdentification = re.split("\s+", RecipientIdentification[0])
            RecipientIdentification_list=split_fun(RecipientIdentification[0])
            RecipientRole = re.findall("<RecipientRole\s*(.*?)\s*/>", singlevalues[0][1], re.I)
            RecipientRole_list=split_fun(RecipientRole[0])
            # print RecipientRole_list
            Iterate_values = re.findall("<ConnectionPoint>([\w\W]*?)</ConnectionPoint>", TransparencyPlc[0][1], re.I)
            # print "len(Iterate_values)",len(Iterate_values)
            for con_index,sec_val in enumerate(Iterate_values):
                # print "con_index",con_index
                Con_identifaction=re.findall("<Identification\s*(.*?)\/>",sec_val,re.I)
                Con_identifaction=re.split("\s+",Con_identifaction[0])
                Con_identifaction_v_list=split_fun(Con_identifaction[0])
                Con_codingscheme_list=split_fun(Con_identifaction[1])
                # print Con_codingscheme_list
                Con_Type  = re.findall("<Type\s*(.*?)\/>", sec_val, re.I)
                Con_Type_list=split_fun(Con_Type[0])
                # print Con_Type_list
                category=re.findall("<Category>([\w\W]*?)</Category>",sec_val,re.I)
                for category_val in category:
                    CapacityCode = re.findall("<CapacityCode\s*(.*?)\/>", category_val, re.I)
                    # print "CapacityCode",CapacityCode
                    CapacityCode=split_fun(CapacityCode[0])
                    periods=re.findall("<Period>([\w\W]*?)</Period>",category_val,re.I)
                    # for capacity_loop in range(len(periods)):
                    #     CapacityCode_val_list.append(CapacityCode)
                    # print CapacityCode_val_list
                    # print "Len CapacityCode_list",len(CapacityCode_val_list)
                    for j,period in enumerate(periods):
                        # print "count",j
                        TimeInterval = re.findall("<TimeInterval\s*(.*?)\/>", period, re.I)
                        TimeInterval_val_list.append(split_fun(TimeInterval[0]))
                        Direction= re.findall("<Direction\s*(.*?)\/>", period, re.I)
                        Direction_val_list=split_fun(Direction[0])
                        Quantity = re.findall("<Quantity\s*(.*?)\/>", period, re.I)
                        Quantity_val_list=split_fun(Quantity[0])
                        MeasureUnit= re.findall("<MeasureUnit\s*(.*?)\/>", period, re.I)
                        MeasureUnit_val_list=split_fun(MeasureUnit[0])
                        worksheet1.write(j + value_inc, 0, Id[0])
                        worksheet1.write(j + value_inc, 1, version_list_pbl)
                        worksheet1.write(j + value_inc, 2, release_list)
                        worksheet1.write(j + value_inc, 3, identifcation_list)
                        worksheet1.write(j + value_inc, 4, Version_list)
                        worksheet1.write(j + value_inc, 5, Type_list)
                        worksheet1.write(j + value_inc, 6, CreationDateTime_list)
                        worksheet1.write(j + value_inc, 7, ValidityPeriod_list)
                        worksheet1.write(j + value_inc, 8, IssuerIdentification_list)
                        worksheet1.write(j + value_inc, 9, codingScheme_list)
                        worksheet1.write(j + value_inc, 10, IssuerRole_list)
                        worksheet1.write(j + value_inc, 11, RecipientIdentification_list)
                        worksheet1.write(j + value_inc, 12, RecipientRole_list)
                        worksheet1.write(j + value_inc, 13, Con_identifaction_v_list)
                        worksheet1.write(j + value_inc, 14, Con_codingscheme_list)
                        worksheet1.write(j + value_inc, 15, Con_Type_list)
                        worksheet1.write(j + value_inc, 16, CapacityCode)
                        worksheet1.write(j + value_inc, 17, TimeInterval_val_list[j])
                        worksheet1.write(j + value_inc, 18, Direction_val_list)
                        worksheet1.write(j + value_inc, 19, Quantity_val_list)
                        worksheet1.write(j + value_inc, 20, MeasureUnit_val_list)
                        # print value_inc
                        # print j + value_inc
                    value_inc=value_inc+len(TimeInterval_val_list)
                    TimeInterval_val_list = []
        # with open("val_id.txt","wb") as f:
			# f.write(str(Id_list)+"\n\n"+str(Total_Quantity_val_list))
        # print len(Total_TimeInterval_val_list)
        # site_list.append(Total_TimeInterval_val_list)
        # print "len(site_list)",len(site_list)
        # print "len(Id_list)",len(Id_list)
        # print "len(version_list_pblc)",len(version_list_pblc)
        # print "len(release_list)",len(release_list)
        # print "len(identifcation_list)",len(identifcation_list)
        # print "len(Version_list)",len(Version_list)
        # print "len(Type_list)",len(Type_list)
        # print "len(CreationDateTime_list)",len(CreationDateTime_list)
        # print "len(ValidityPeriod_list)",len(ValidityPeriod_list)
        # print "len(IssuerIdentification_list)",len(IssuerIdentification_list)
        # print "len(codingScheme_list)",len(codingScheme_list)
        # print "len(IssuerRole_list)",len(IssuerRole_list)
        # print "len(RecipientIdentification_list)",len(RecipientIdentification_list)
        # print "len(Total_TimeInterval_val_list)",len(Total_TimeInterval_val_list)
        # print "len(Total_Direction_val_list)",len(Total_Direction_val_list)
        # print "len(Total_Quantity_val_list)",len(Total_Quantity_val_list)
        # print "len(Total_MeasureUnit_val_list)",len(Total_MeasureUnit_val_list)
        # print "len(Total_MeasureUnit_val_list)",len(Total_MeasureUnit_val_list)
        # print "len(Total_CapacityCode_list)",len(Total_CapacityCode_list)
        # print site_list
        # raw_input('press enter')
        # print "*************List collected ****************"
        # file_writing(Id_list, version_list_pblc,release_list,identifcation_list,Version_list,Type_list,CreationDateTime_list,ValidityPeriod_list,IssuerIdentification_list,codingScheme_list,IssuerRole_list,RecipientIdentification_list,RecipientRole_list,Con_identifaction_v_list,Con_codingscheme_list,Con_Type_list,Total_CapacityCode_list,Total_TimeInterval_val_list,Total_Direction_val_list,Total_Quantity_val_list,Total_MeasureUnit_val_list,rawFileName,site_list)
        zf.close()
        os.remove(zip_fileName)
        return rawFileName

    except Exception as e:
        print "Exception::" + str(e)
        print  "Error on extraction for " + str(DataSourceID)
        print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
        Fundalytics_Utility.log(DataSourceID, 'Extract',
                                str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')

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
        '''looping through the scraper parameter name'''
        for scraper_parameters in spName:
            scraperParameterName = 'E-' + str(datasourceName) + '-' + str(marketName) + '-' + str(
                scraper_parameters).strip()
            print scraperParameterName

            '''getting url from scraperparameter'''

            get_url_to_scrape = control.get(scraperParameterName, 'URL')
            # print get_url_to_scrape_date
            #{'gmail_imap': 'imap.gmail.com', 'imap_port': 993, 'username': 'argus.subscribe@meritgroup.co.uk','password': 'Merit987&'}
            if marketName=="transparency-data":
                get_url_to_scrape = ast.literal_eval(get_url_to_scrape)
                gmail_imap=get_url_to_scrape['gmail_imap']
                imap_port=get_url_to_scrape['imap_port']
                username=get_url_to_scrape['username']
                password=get_url_to_scrape['password']
            method = control.get(scraperParameterName, 'E_METHOD').split('|')
            scraperType = control.get(scraperParameterName, 'SCRAPERTYPE').lower()
            if marketName=="the-gas-wheel":
                rawFile = getcontent_2(DataSourceID, get_url_to_scrape, datasourceName, marketName, scraperType, scraperParameterName)
            else:
                rawFile = getcontent(gmail_imap,imap_port,username,password,DataSourceID,datasourceName, marketName, scraperType, scraperParameterName)
            List.append(rawFile)
            print List

        # print "List", List
        '''Removing empty list '''
        List = remove_empty(List)

        '''Joining all List'''
        if sum(isinstance(i, list) for i in List) != 0:
            fileList = list(itertools.chain.from_iterable(List))
        else:
            fileList = List

        '''Removing Duplications in the List'''
        fileList = list(set(fileList))
        successStatus = 1
        print "Final file",fileList
        s3File=fileList[0]
        if successStatus == 1:
            print "s3File:", s3File

            Fundalytics_Utility.s3_fileupload(s3File, DataSourceID, s3path_upload, 'Extract', control)

            print "Uploaded Completed"

            Fundalytics_Utility.log(DataSourceID, 'Extract-Module', '', 'Extracted',
                                    str(s3path_upload) + str(s3File).replace(tempFilePath, ''))
            control.add_section('status')

            control.add_section('filename')
            control.set("filename", "extractfilename", str(s3File).replace(tempFilePath, ''))

            for filename in fileList:
				os.remove(filename)
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
        Fundalytics_Utility.log(DataSourceID, 'Extract',
                                str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        return control
