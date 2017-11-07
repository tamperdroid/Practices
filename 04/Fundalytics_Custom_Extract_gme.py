# import requests,re
# url="http://www.pxe.cz/On-Line/Futures/?language=english"
# ping1=requests.get(url)
# ping_content=re.findall("(<h1>Futures[\w\W]*?</table>)",str(ping1.content),re.I)
# with open("ping2.html","wb") as f:
#     f.write(str(ping_content[0]))
import requests,re,sys,zipfile,imp,os,itertools,xlsxwriter
from titlecase import titlecase
from datetime import datetime
from dateutil.relativedelta import relativedelta

date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
cur_date = str(datetime.now().strftime("%Y-%m-%d"))
separate_file=[]
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', '/home/merit/argusmedia/Fundalytics_Utility.py')

tempFilePath="/home/merit/argusmedia/temp/"

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
                PreviousDay = nowdate + relativedelta(days=int(regex))
                month_value = "{MM\\" + regex + "}"
                post_content = re.sub(month_value, PreviousDay.strftime('%m'), post_content)
                day_value = "{DD\\" + regex + "}"
                post_content = re.sub(str(day_value), str(PreviousDay.strftime('%d')), post_content)
                year_value = "{YYYY\\" + regex + "}"
                post_content = re.sub(year_value, PreviousDay.strftime('%Y'), post_content)
            if re.search(r'\{DD\}',str(post_content)):
                post_content = post_content.replace('{YYYY}', nowdate.strftime("%Y"))
                post_content = post_content.replace('{MM}', nowdate.strftime("%m"))
                post_content = post_content.replace('{DD}', nowdate.strftime("%d"))
        return post_content
    except Exception as e:
            print "Exception::" + str(e)
            print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)

def header_form(formed_url,ses_id):
    header = {
        "Host": "www.mercatoelettrico.org",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": str(formed_url),
        "Connection": "keep-alive",
        # "DNT": "1",
        # "Cookie": "ASP.NET_SessionId=" + str(ses_id) ,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return header
def post_content_needs(formed_url,content):

    regx_vs="<input\s*[^<]*?id=[\"\']__VIEWSTATE[\"\']\s*value=[\"\']([^<]*?)[\"\']\s*\/>"
    vs=re.findall(regx_vs,str(content),re.IGNORECASE)

    regx_vsg="<input\s*[^<]*?id=[\"\']__VIEWSTATEGENERATOR[\"\']\s*value=[\"\']([^<]*?)[\"\']\s*\/>"
    vsg=re.findall(regx_vsg,str(content),re.IGNORECASE)

    regx_ev="<input\s*[^<]*?id=[\"\']__EVENTVALIDATION[\"\']\s*value=[\"\']([^<]*?)[\"\']\s*\/>"
    ev=re.findall(regx_ev,str(content),re.IGNORECASE)

    vs=vs[0]
    vs =re.sub(r'\/', '%2F', str(vs))
    vs =re.sub(r'\=', '%3D', str(vs))
    vs =re.sub(r'\+', '%2B', str(vs))
    vsg=vsg[0]
    vsg =re.sub(r'\/', '%2F', str(vsg))
    vsg =re.sub(r'\=', '%3D', str(vsg))
    vsg =re.sub(r'\+', '%2B', str(vsg))
    ev=ev[0]
    ev =re.sub(r'\/', '%2F', str(ev))
    ev =re.sub(r'\=', '%3D', str(ev))
    ev =re.sub(r'\+', '%2B', str(ev))
    # print ev
    previouspage=re.findall("id=\"__PREVIOUSPAGE\"\s*value=\"(.*?)\"",str(content),re.I)
    return vs,vsg,ev,previouspage[0]
def file_writing(file_data,datasourceName,marketName):
    try:
        rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
        rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"
        workbook = xlsxwriter.Workbook(rawFileName)
        if marketName=="mgp-additional-demand-bid-offers":
            marketName="mgp-add-bid-offers"
        worksheet1 = workbook.add_worksheet(marketName)
        row_inc=0
        flag=0
        for file_indx,file in enumerate(file_data):
            for i,data in enumerate(file):
                    for val_indx,val in enumerate(data):
                        worksheet1.write(i+row_inc+1,val_indx , val[1])
                        if i==0 and flag==0:
                            worksheet1.write(i + row_inc, val_indx, val[0])
                    flag += 1
            row_inc=row_inc+len(file)
        workbook.close()
        return rawFileName
    except Exception as e:
        print "Exception::" + str(e)
        print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
def list_form(data_list):
    file_data=[]
    for datum in data_list:
        data = re.findall("<(.*?)>(.*?)<\/.*?>", str(datum), re.I)
        file_data.append(data)
    separate_file.append(file_data)
    file_data = []
    return separate_file

def getcontent(get_url_to_scrape, DataSourceID, datasourceName, marketName, scraperType,scraperParameterName,POST_CONTENT,control):
    try:
        s=requests.Session()
        POST_CONTENT=postContent_to_parse_date(POST_CONTENT,datasourceName, marketName, control)
        ping1=s.get(get_url_to_scrape)
        ses_id=re.findall(r"ASP.NET_SessionId=(.*?)\s*for",str(ping1.cookies),re.I)
        appendable_url="http://www.mercatoelettrico.org/En/Tools"
        url_to_append_from_site=re.findall(r"action=\"\.(.*?)\"",str(ping1.content),re.I)
        url_to_append_from_site=url_to_append_from_site[0].replace("amp;","")
        formed_url=str(appendable_url)+str(url_to_append_from_site)
        header1=header_form(formed_url,ses_id[0])
        vs,vsg,ev,previouspage=post_content_needs(formed_url,ping1.content)
        post_content1="__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE="+str(vs)+"&__VIEWSTATEGENERATOR="+str(vsg)+"&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=598&__PREVIOUSPAGE="+str(previouspage)+"&__EVENTVALIDATION="+str(ev)+"&ctl00%24tbTitolo=search+this+site&ctl00%24UserName=&ctl00%24Password=&ctl00%24ContentPlaceHolder1%24CBAccetto1=on&ctl00%24ContentPlaceHolder1%24CBAccetto2=on&ctl00%24ContentPlaceHolder1%24Button1=Accept"
        ping2=s.post(formed_url,data=post_content1,headers=header1)
        appendable_url_ping3=re.findall(r"method\=\"post\"\s*action=\"\.(.*?)\"",str(ping2.content),re.I)
        url3="http://www.mercatoelettrico.org/En/download"
        url3_ping3=str(url3)+str(appendable_url_ping3[0])
        print url3_ping3
        header2=header_form(url3_ping3,ses_id[0])
        vs,vsg,ev,previouspage=post_content_needs(url3_ping3,ping2.content)
        post_content2=eval(POST_CONTENT)
        ping3=s.post(url3_ping3,data=post_content2,headers=header2)
        zipFileName=str(marketName) + str(".zip")
        with open(zipFileName,"wb") as f:
            f.write(str(ping3.content))
        try:
            zf = zipfile.ZipFile(zipFileName)
            for name in zf.namelist():
                print name
                file_content=zf.read(name)
                if marketName=="mgp-transmission-limits":
                    data_list=re.findall(r"<LimitiTransito>([\w\W]*?)</LimitiTransito>",str(file_content),re.I)
                    separate_file=list_form(data_list)
                if marketName == "mgp-transits":
                    data_list = re.findall(r"<MgpTransiti>([\w\W]*?)</MgpTransiti>", str(file_content),re.I)
                    separate_file=list_form(data_list)
                if marketName == "mgp-volumes":
                    data_list = re.findall(r"<Quantita>([\w\W]*?)</Quantita>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName == "mgp-liquidity":
                    data_list = re.findall(r"<DatiLiquidita>([\w\W]*?)</DatiLiquidita>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName=="mgp-demand-forecast":
                    data_list = re.findall(r"<marketintervaldetail>([\w\W]*?)</marketintervaldetail>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName=="mgp-demand-actual":
                    data_list = re.findall(r"<Fabbisogno>([\w\W]*?)</Fabbisogno>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName=="mgp-dayahead-prices":
                    data_list = re.findall(r"<Prezzi>([\w\W]*?)</Prezzi>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName=="mgp-conventional-prices" :
                    data_list = re.findall(r"<PrezziConvenzionali>([\w\W]*?)</PrezziConvenzionali>", str(file_content), re.I)
                    separate_file = list_form(data_list)
                if marketName=="mgp-additional-demand-bid-offers":
                    data_list = re.findall(r"<OfferteIntegrativeGrtn>([\w\W]*?)</OfferteIntegrativeGrtn>", str(file_content),re.I)
                    separate_file = list_form(data_list)
            rawFileName = file_writing(separate_file, datasourceName, marketName)
            separate_file = []
            return rawFileName
        finally:
            zf.close()
            os.remove(zipFileName)
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
        Fundalytics_Utility.log(DataSourceID, 'Extract', str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),
                                'Error', '')
        return control

