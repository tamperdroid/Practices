import requests,sys,time,re,xlsxwriter,xlrd,imp,os,itertools
from titlecase import titlecase
from datetime import datetime
from dateutil.relativedelta import relativedelta


date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))
separate_file=[]
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/12/Fundalytics_Utility.py')

tempFilePath="D:/01_2017/12/temp/"

if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)

def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))

def postContent_to_parse_date(post_content,datasourceName, marketName, control):
    # def url_to_parse_date(url, datasourceName, marketName, control):
    try:
        try:
            if control.get("backfill_data-" + str(marketName), str(datasourceName) + "IsBackFill") == 'YES':
                backFillStart = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillFrom")
                backFillEnd = control.get("backfill_data-" + marketName, str(datasourceName) + "BackFillTo")
                nowdate = datetime.strptime(str(backFillStart), '%Y-%m-%d  %H:%M:%S')
            else:
                raise Exception
        except Exception as e:
            nowdate = datetime.now()
        # nowdate = datetime.now()
        if re.search(r'\{DD(\W)(\d+)\}', str(post_content)):
            dateRegex = re.findall(r'\{DD(\W\d+)\}', post_content, re.I)
            for regex in dateRegex:
                PreviousMonth = nowdate + relativedelta(days=int(regex))
                month_value = "{MM\\" + regex + "}"
                post_content = re.sub(month_value, PreviousMonth.strftime('%m'), post_content)
                day_value = "{DD\\" + regex + "}"
                post_content = re.sub(str(day_value), str(PreviousMonth.strftime('%d')), post_content)
                year_value = "{YYYY\\" + regex + "}"
                post_content = re.sub(year_value, PreviousMonth.strftime('%Y'), post_content)
            if re.search(r'\{DD\}',str(post_content)):
                post_content = post_content.replace('{YYYY}', nowdate.strftime("%Y"))
                post_content = post_content.replace('{MM}', nowdate.strftime("%m"))
                post_content = post_content.replace('{DD}', nowdate.month)
        return post_content
    except Exception as e:
            print "Exception::" + str(e)
            print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)


def merge_file(DataSourceID, datasourceName, marketName ,control, fileList):
    try:
        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"
        # rawFileName = "file.xlsx"
        workbook = xlsxwriter.Workbook(rawFileName)

        for li_indx, xls in enumerate(fileList):
            print xls
            insheet = xlrd.open_workbook(str(xls)+".xlsx")
            sheet_count = len(insheet.sheets())
            for c in range(sheet_count):
                # need to add sheet index if sheet count increase
                outsheet = workbook.add_worksheet(str(xls))
                sh = insheet.sheet_by_index(c)
                for row_idx in xrange(sh.nrows):
                    for col_idx in xrange(sh.ncols):
                        outsheet.write(row_idx, col_idx, sh.cell_value(row_idx, col_idx))
        workbook.close()
        return rawFileName
    except Exception as e:
            print "Excecption",str(e)
            print "Excecption line No",sys.exc_traceback.tb_lineno

def getcontent(get_url_to_scrape, DataSourceID, datasourceName, marketName, scraperType,scraperParameterName,POST_CONTENT,control):
    try:
        s=requests.Session()
        POST_CONTENT = postContent_to_parse_date(POST_CONTENT, datasourceName, marketName, control)
        ping1=requests.get(get_url_to_scrape)
        # with open("ping1.html","wb") as f:
        #     f.write(str(ping1.content))

        actionId=re.findall("CurrentActionId\"\:\"(.*?)\"",str(ping1.content),re.I)
        #export from 4 ids
        exportId=re.findall("ExportExcel.*?command\"\:\"(.*?)\"\,\"commandViewModelKeys",str(ping1.content),re.I)

        post_url="http://www.jao.eu/LicquidAction/ProcessEventActions"
        header1={

            "Host": "www.jao.eu",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Referer":"http://www.jao.eu/marketdata/export/overview",
            "X-Requested-With": "XMLHttpRequest",
            "Connection":"keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        post_content_1="""{"actionId":"84d46002-4705-47a1-89fb-a56200e5403e","globalParameters":{},"localParameters":{"AuctionTypeId":null,"BorderIds":null,"FromDate":"1900-01-01","ToDate":"2100-12-31","AuctionId":""},"requests":[{"eventActionType":"ExecuteQuery","actionId":"84d46002-4705-47a1-89fb-a56200e5403e","rootMorphId":"84d46002-4705-47a1-89fb-a56200e5403e","queryObjectName":"AuctionsTypes","queries":[{"listeners":["1"],"params":{}}],"eventActionId":6},{"eventActionType":"ExecuteQuery","actionId":"84d46002-4705-47a1-89fb-a56200e5403e","rootMorphId":"84d46002-4705-47a1-89fb-a56200e5403e","queryObjectName":"Borders","queries":[{"listeners":["2"],"params":{}}],"eventActionId":7}]}"""

        ping2=s.post(post_url,data=post_content_1,headers=header1)
        # print ping2.cookies.keys()
        ping2.cookies.clear()

        dic=eval(str(ping2.content))
        meta_ids=dic['responses'][0]['Results'][0]['Result']['Results']
        # print meta_ids
        id="%22"+str(dic['responses'][1]["Results"][0]['Result']['Results'][0]["Id"])+"%22"

        urls_list=[]
        a = []
        for i in range(59):
            a.append(i)

        ping_count = 0
        dropdown_ids_to_url_1 = ""
        dropdown_ids_to_url_2 = ""
        dropdown_ids_to_url= ""
        FileNames=[]
        for meta_indx,meta_id in enumerate(meta_ids):
            dropdown_ids = dic['responses'][1]["Results"][0]['Result']['Results']
            for dropdown_indx,dropdown_id in enumerate(dropdown_ids):
                if dropdown_indx in a[:30]:
                    # print dropdown_indx
                    if dropdown_indx == 29:
                        dropdown_ids_to_url_1 += str("%22" + dropdown_id["Id"]) + "%22"
                    else:
                        dropdown_ids_to_url_1 += str("%22" + dropdown_id["Id"]) + "%22,"
                elif dropdown_indx in a[29:]:
                    if dropdown_indx == len(dropdown_ids)-1:
                        dropdown_ids_to_url_2 += str("%22" + dropdown_id["Id"]) + "%22"
                    else:
                        dropdown_ids_to_url_2 += str("%22" + dropdown_id["Id"]) + "%22,"
                else:
                    # print dropdown_indx
                    dropdown_ids_to_url=str("%22"+dropdown_id["Id"])+"%22"
            urls_list.append(dropdown_ids_to_url_1)
            urls_list.append(dropdown_ids_to_url_2)
            urls_list.append(dropdown_ids_to_url)

            for border_indx,border_id in  enumerate(urls_list):
                # print "border_indx",border_indx
                if border_id == "":
                    continue
                baseUrl="http://www.jao.eu/Export/Excel/?actionId="+actionId[0]+"&excelExportId="+str(exportId[0])+"&parameters="
                download_url=eval(POST_CONTENT)
                try:
                    formed_url=str(baseUrl)+str(download_url)
                    # print ping_count,formed_url
                    with open("urls.txt","ab") as f:
                        f.write(str(ping_count)+str(formed_url)+"\n")
                    ping3=s.get(formed_url)
                    ping_count+=1
                    FileName=meta_id["Code"]+str(ping_count)
                    with open(FileName+".xlsx","wb") as f:
                        f.write(str(ping3.content))
                    # print ping3.status_code
                    ping3.cookies.clear()
                except Exception as e:
                    print "Exception::" + str(e)
                    print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
                FileNames.append(FileName)
            # print urls_list
            urls_list=[]
            dropdown_ids_to_url_1=""
            dropdown_ids_to_url_2=""
            dropdown_ids_to_url=""

        rawFileName=merge_file(DataSourceID, datasourceName, marketName, control,FileNames)
        for File in FileNames:
            os.remove(str(File)+".xlsx")
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
            POST_CONTENT = control.get(scraperParameterName, "POST_CONTENT2")

            # print get_url_to_scrape_date
            method = control.get(scraperParameterName, 'E_METHOD').split('|')

            scraperType = control.get(scraperParameterName, 'SCRAPERTYPE').lower()

            rawFile = getcontent(get_url_to_scrape, DataSourceID, datasourceName, marketName, scraperType,
                                 scraperParameterName,POST_CONTENT,control)
            print rawFile
            List.append(rawFile)
            print List

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
        s3File = ''

        '''If FileList is 1 returning that file to s3'''
        if len(fileList) == 1:
            xlsFile = ''
            if '.xls' in str(fileList[0]) or '.xlsx' in str(fileList[0]):
                xlsFile = fileList[0]
            if len(xlsFile) > 0:
                cookedFile, status = rawFile, True
                if cookedFile != 'n/a':
                    s3File = cookedFile
                else:
                    successStatus = 0
                    print 'fileList Error for lenth ==1'
            else:
                s3File = fileList[0]
                print fileList[0]
        elif len(fileList) > 1:
            '''File merging takes place '''
            cookedFile, status = rawFile, True
            if cookedFile != 'n/a':
                s3File = cookedFile
            else:
                successStatus = 0
                print 'fileList Error for length >1'
        elif len(fileList) < 1:
            successStatus = 0
            print "fileList error for length ,1"

        if successStatus == 1:
            print "s3File:", s3File
            # Fundalytics_Utility.s3_fileupload(s3File, DataSourceID, s3path_upload, 'Extract', control)
            print "Uploaded Completed"
            Fundalytics_Utility.log(DataSourceID, 'Extract-Module', '', 'Extracted',
                                    str(s3path_upload) + str(s3File).replace(tempFilePath, ''))
            control.add_section('status')

            control.add_section('filename')
            control.set("filename", "extractfilename", str(s3File).replace(tempFilePath, ''))

            # for filename in fileList:
                # os.remove(filename)
            # control.set("status", "extractStatus", "1")
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