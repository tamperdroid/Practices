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

Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/03/Fundalytics_Utility.py')

tempFilePath="D:/01_2017/03/temp/"

if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)

def remove_empty(l):
    '''
        Remove empty list
    '''
    return filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l))

def postContent_to_parse_date(post_content):
    try:
        nowdate = datetime.now()
            # backFillEnd = ''
            # date_time = str(datetime.now().strftime("%Y%m%d_%H%M"))
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
    # print "View State:",vs

    regx_vsg="<input\s*[^<]*?id=[\"\']__VIEWSTATEGENERATOR[\"\']\s*value=[\"\']([^<]*?)[\"\']\s*\/>"
    vsg=re.findall(regx_vsg,str(content),re.IGNORECASE)
    # print "View State generator:",vsg

    regx_ev="<input\s*[^<]*?id=[\"\']__EVENTVALIDATION[\"\']\s*value=[\"\']([^<]*?)[\"\']\s*\/>"
    ev=re.findall(regx_ev,str(content),re.IGNORECASE)
    # print "Event validation:",ev

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
def file_writing(file_data,datasourceName,marketName,headers):
    rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
    rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"
    workbook = xlsxwriter.Workbook(rawFileName)
    if marketName=="mgp-additional-demand-bid-offers":
        marketName="mgp-add-bid-offers"
    worksheet1 = workbook.add_worksheet(marketName)
    row_inc=0
    for head_indx,header in enumerate(headers):
        worksheet1.write(0, head_indx,header)
    for file_indx,file in enumerate(file_data):
        for i,data in enumerate(file):
                for val_indx,val in enumerate(data):
                    worksheet1.write(val_indx+row_inc+1, i, val)
        # print "Before",row_inc
        row_inc=row_inc+len(data)
        # print "after",row_inc
        # raw_input("row_inc")
        print len(data)
    workbook.close()
    return rawFileName

def getcontent(get_url_to_scrape, DataSourceID, datasourceName, marketName, scraperType,scraperParameterName,POST_CONTENT):
    try:
        s=requests.Session()
        separate_file=[]
        file_data=[]
        headers=[]
        POST_CONTENT=postContent_to_parse_date(POST_CONTENT)
        ping1=s.get(get_url_to_scrape)
        # with open("ping1.html","wb") as f:
        #         f.write(str(ping1.content))
        ses_id=re.findall(r"ASP.NET_SessionId=(.*?)\s*for",str(ping1.cookies),re.I)
        appendable_url="http://www.mercatoelettrico.org/En/Tools"
        url_to_append_from_site=re.findall(r"action=\"\.(.*?)\"",str(ping1.content),re.I)
        url_to_append_from_site=url_to_append_from_site[0].replace("amp;","")
        formed_url=str(appendable_url)+str(url_to_append_from_site)
        header1=header_form(formed_url,ses_id[0])
        vs,vsg,ev,previouspage=post_content_needs(formed_url,ping1.content)
        post_content1="__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE="+str(vs)+"&__VIEWSTATEGENERATOR="+str(vsg)+"&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=598&__PREVIOUSPAGE="+str(previouspage)+"&__EVENTVALIDATION="+str(ev)+"&ctl00%24tbTitolo=search+this+site&ctl00%24UserName=&ctl00%24Password=&ctl00%24ContentPlaceHolder1%24CBAccetto1=on&ctl00%24ContentPlaceHolder1%24CBAccetto2=on&ctl00%24ContentPlaceHolder1%24Button1=Accept"

        ping2=s.post(formed_url,data=post_content1,headers=header1)
        # with open("ping2.html","wb") as f:
        #     f.write(str(ping2.content))
        appendable_url_ping3=re.findall(r"method\=\"post\"\s*action=\"\.(.*?)\"",str(ping2.content),re.I)
        url3="http://www.mercatoelettrico.org/En/download"
        url3_ping3=str(url3)+str(appendable_url_ping3[0])
        print url3_ping3
        header2=header_form(url3_ping3,ses_id[0])
        vs,vsg,ev,previouspage=post_content_needs(url3_ping3,ping2.content)
        # post_content2="__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE="+str(vs)+"&__VIEWSTATEGENERATOR="+str(vsg)+"&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=113&__PREVIOUSPAGE="+str(previouspage)+"&__EVENTVALIDATION="+str(ev)+"&ctl00%24tbTitolo=search+this+site&ctl00%24UserName=&ctl00%24Password=&ctl00%24ContentPlaceHolder1%24tbDataStart=29%2F12%2F2016&ctl00%24ContentPlaceHolder1%24tbDataStop=30%2F12%2F2016&ctl00%24ContentPlaceHolder1%24btnScarica=download+compressed+xml+file"
        post_content2=eval(POST_CONTENT)
        ping3=s.post(url3_ping3,data=post_content2,headers=header2)
        # print ping3.content
        zipFileName=str(marketName) + str(".zip")
        with open(str(marketName)+str(".zip"),"wb") as f:
            f.write(str(ping3.content))
        try:
            zf = zipfile.ZipFile(zipFileName)
            for name in zf.namelist():
                print name
                file_content=zf.read(name)
                # print file_content

                if marketName=="mgp-transmission-limits":
                    # LimitTransito_list=re.findall(r"<LimitiTransito>([\w\W]*?)</LimitiTransito>",str(file_content),re.I)
                    # print LimitTransito_list
                    # print "LimitTransito_list",len(LimitTransito_list)
                    # for LimitTransito in LimitTransito_list:
                        # print LimitTransito
                    E1=re.findall("<(.*?)>(.*?)<\/.*?>",str(file_content),re.I)
                    # E2=re.findall("<Da>(.*?)</Da>",str(file_content),re.I)
                    # E3 = re.findall("<A>(.*?)</A>", str(file_content), re.I)
                    # Date=re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    # Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    # value1 = re.findall("<Limite>(.*?)</Limite>", str(file_content), re.I)
                    # value2 = re.findall("<Coefficiente>(.*?)</Coefficiente>", str(file_content), re.I)
                    # # print value2
                    # file_data.append(name)
                    # headers=["Mercato","Da","A","Data","Ora","Limite","Coefficiente"]
                    file_data.append(E1)
                    # file_data.append(E2)
                    # file_data.append(E3)
                    # file_data.append(Date)
                    # file_data.append(Hour)
                    # # print value1
                    # file_data.append(value1)
                    # file_data.append(value2)
                    # print "len file_data",len(file_data)
                    # raw_input("file")
                    separate_file.append(file_data)
                    file_data=[]
                    # print len(separate_file)
                    # with open("separate.txt","wb") as f:
                    #     f.write(str(separate_file))
                if marketName == "mgp-transits":
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    E2 = re.findall("<Da>(.*?)</Da>", str(file_content), re.I)
                    E3 = re.findall("<A>(.*?)</A>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1=re.findall("<TransitoMWh>(.*?)</TransitoMWh>",str(file_content),re.I)
                    headers = ["Mercato","Da","A","Data","Ora","TransitoMWh"]
                    file_data.append(E1)
                    file_data.append(E2)
                    file_data.append(E3)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value1)
                    separate_file.append(file_data)
                if marketName == "mgp-volumes":
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1 = re.findall("<NAT_ACQUISTI>(.*?)</NAT_ACQUISTI>", str(file_content), re.I)
                    value2 = re.findall("<CNOR_ACQUISTI>(.*?)</CNOR_ACQUISTI>", str(file_content), re.I)
                    value3 = re.findall("<CSUD_ACQUISTI>(.*?)</CSUD_ACQUISTI>", str(file_content), re.I)
                    value4 = re.findall("<NORD_ACQUISTI>(.*?)</NORD_ACQUISTI>", str(file_content), re.I)
                    value5 = re.findall("<SARD_ACQUISTI>(.*?)</SARD_ACQUISTI>", str(file_content), re.I)
                    value6 = re.findall("<SICI_ACQUISTI>(.*?)</SICI_ACQUISTI>", str(file_content), re.I)
                    value7 = re.findall("<SUD_ACQUISTI>(.*?)</SUD_ACQUISTI>", str(file_content), re.I)
                    value8 = re.findall("<AUST_ACQUISTI>(.*?)</AUST_ACQUISTI>", str(file_content), re.I)
                    value9 = re.findall("<BRNN_ACQUISTI>(.*?)</BRNN_ACQUISTI>", str(file_content), re.I)
                    value10 = re.findall("<COAC_ACQUISTI>(.*?)</COAC_ACQUISTI>", str(file_content), re.I)
                    value11 = re.findall("<CORS_ACQUISTI>(.*?)</CORS_ACQUISTI>", str(file_content), re.I)
                    value12 = re.findall("<FOGN_ACQUISTI>(.*?)</FOGN_ACQUISTI>", str(file_content), re.I)
                    value13 = re.findall("<FRAN_ACQUISTI>(.*?)</FRAN_ACQUISTI>", str(file_content), re.I)
                    value14 = re.findall("<GREC_ACQUISTI>(.*?)</GREC_ACQUISTI>", str(file_content), re.I)
                    value15 = re.findall("<MFTV_ACQUISTI>(.*?)</MFTV_ACQUISTI>", str(file_content), re.I)
                    value16 = re.findall("<PRGP_ACQUISTI>(.*?)</PRGP_ACQUISTI>", str(file_content), re.I)
                    value17 = re.findall("<ROSN_ACQUISTI>(.*?)</ROSN_ACQUISTI>", str(file_content), re.I)
                    value18 = re.findall("<SLOV_ACQUISTI>(.*?)</SLOV_ACQUISTI>", str(file_content), re.I)
                    value19 = re.findall("<SVIZ_ACQUISTI>(.*?)</SVIZ_ACQUISTI>", str(file_content), re.I)
                    value20 = re.findall("<BSP_ACQUISTI>(.*?)</BSP_ACQUISTI>", str(file_content), re.I)
                    value21 = re.findall("<MALT_ACQUISTI>(.*?)</MALT_ACQUISTI>", str(file_content), re.I)
                    value22 = re.findall("<XAUS_ACQUISTI>(.*?)</XAUS_ACQUISTI>", str(file_content), re.I)
                    value23 = re.findall("<XFRA_ACQUISTI>(.*?)</XFRA_ACQUISTI>", str(file_content), re.I)
                    value24 = re.findall("<TOTALE_VENDITE>(.*?)</TOTALE_VENDITE>", str(file_content), re.I)
                    value25 = re.findall("<NAT_VENDITE>(.*?)</NAT_VENDITE>", str(file_content), re.I)
                    value26 = re.findall("<CNOR_VENDITE>(.*?)</CNOR_VENDITE>", str(file_content), re.I)
                    value27 = re.findall("<CSUD_VENDITE>(.*?)</CSUD_VENDITE>", str(file_content), re.I)
                    value28 = re.findall("<NORD_VENDITE>(.*?)</NORD_VENDITE>", str(file_content), re.I)
                    value29 = re.findall("<SARD_VENDITE>(.*?)</SARD_VENDITE>", str(file_content), re.I)
                    value30 = re.findall("<SICI_VENDITE>(.*?)</SICI_VENDITE>", str(file_content), re.I)
                    value31 = re.findall("<SUD_VENDITE>(.*?)</SUD_VENDITE>", str(file_content), re.I)
                    value32 = re.findall("<AUST_VENDITE>(.*?)</AUST_VENDITE>", str(file_content), re.I)
                    value33 = re.findall("<BRNN_VENDITE>(.*?)</BRNN_VENDITE>", str(file_content), re.I)
                    value34 = re.findall("<COAC_VENDITE>(.*?)</COAC_VENDITE>", str(file_content), re.I)
                    value35 = re.findall("<CORS_VENDITE>(.*?)</CORS_VENDITE>", str(file_content), re.I)
                    value36 = re.findall("<FOGN_VENDITE>(.*?)</FOGN_VENDITE>", str(file_content), re.I)
                    value37 = re.findall("<FRAN_VENDITE>(.*?)</FRAN_VENDITE>", str(file_content), re.I)
                    value38 = re.findall("<GREC_VENDITE>(.*?)</GREC_VENDITE>", str(file_content), re.I)
                    value39 = re.findall("<MFTV_VENDITE>(.*?)</MFTV_VENDITE>", str(file_content), re.I)
                    value40 = re.findall("<PRGP_VENDITE>(.*?)</PRGP_VENDITE>", str(file_content), re.I)
                    value41 = re.findall("<ROSN_VENDITE>(.*?)</ROSN_VENDITE>", str(file_content), re.I)
                    value42 = re.findall("<SLOV_VENDITE>(.*?)</SLOV_VENDITE>", str(file_content), re.I)
                    value43 = re.findall("<SVIZ_VENDITE>(.*?)</SVIZ_VENDITE>", str(file_content), re.I)
                    value44 = re.findall("<BSP_VENDITE>(.*?)</BSP_VENDITE>", str(file_content), re.I)
                    value45 = re.findall("<MALT_VENDITE>(.*?)</MALT_VENDITE>", str(file_content), re.I)
                    value46 = re.findall("<XAUS_VENDITE>(.*?)</XAUS_VENDITE>", str(file_content), re.I)
                    value47 = re.findall("<XFRA_VENDITE>(.*?)</XFRA_VENDITE>", str(file_content), re.I)
                    value48 = re.findall("<TOTITABSP_VENDITE>(.*?)</TOTITABSP_VENDITE>", str(file_content), re.I)
                    value49 = re.findall("<TOTITABSP_ACQUISTI>(.*?)</TOTITABSP_ACQUISTI>", str(file_content), re.I)

                    file_data.append(E1)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value1)
                    file_data.append(value2)
                    file_data.append(value3)
                    file_data.append(value4)
                    file_data.append(value5)
                    file_data.append(value6)
                    file_data.append(value7)
                    file_data.append(value8)
                    file_data.append(value9)
                    file_data.append(value10)
                    file_data.append(value11)
                    file_data.append(value12)
                    file_data.append(value13)
                    file_data.append(value14)
                    file_data.append(value15)
                    file_data.append(value16)
                    file_data.append(value17)
                    file_data.append(value18)
                    file_data.append(value19)
                    file_data.append(value20)
                    file_data.append(value21)
                    file_data.append(value22)
                    file_data.append(value23)
                    file_data.append(value24)
                    file_data.append(value25)
                    file_data.append(value26)
                    file_data.append(value27)
                    file_data.append(value28)
                    file_data.append(value29)
                    file_data.append(value30)
                    file_data.append(value31)
                    file_data.append(value32)
                    file_data.append(value33)
                    file_data.append(value34)
                    file_data.append(value35)
                    file_data.append(value36)
                    file_data.append(value37)
                    file_data.append(value38)
                    file_data.append(value39)
                    file_data.append(value40)
                    file_data.append(value41)
                    file_data.append(value42)
                    file_data.append(value43)
                    file_data.append(value44)
                    file_data.append(value45)
                    file_data.append(value46)
                    file_data.append(value47)
                    file_data.append(value48)
                    file_data.append(value49)

                    separate_file.append(file_data)
                    file_data = []
                if marketName == "mgp-liquidity":
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    # E2 = re.findall("<Da>(.*?)</Da>", str(file_content), re.I)
                    # E3 = re.findall("<A>(.*?)</A>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1 = re.findall("<Liquidita>(.*?)</Liquidita>", str(file_content), re.I)
                    file_data.append(E1)
                    # file_data.append(E2)
                    # file_data.append(E3)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value1)
                    separate_file.append(file_data)
                    file_data=[]
                if marketName=="mgp-demand-forecast" or marketName=="mgp-demand-actual":
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1 = re.findall("<Totale>(.*?)</Totale>", str(file_content), re.I)
                    if value1==[]:
                        value1 = re.findall("<Italia>(.*?)</Italia>", str(file_content), re.I)
                    value2 = re.findall("<CNOR>(.*?)</CNOR>", str(file_content), re.I)
                    value3 = re.findall("<CSUD>(.*?)</CSUD>", str(file_content), re.I)
                    value4 = re.findall("<NORD>(.*?)</NORD>", str(file_content), re.I)
                    value5 = re.findall("<SARD>(.*?)</SARD>", str(file_content), re.I)
                    value6 = re.findall("<SICI>(.*?)</SICI>", str(file_content), re.I)
                    value7 = re.findall("<SUD>(.*?)</SUD>", str(file_content), re.I)
                    file_data.append(E1)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value1)
                    file_data.append(value2)
                    file_data.append(value3)
                    file_data.append(value4)
                    file_data.append(value5)
                    file_data.append(value6)
                    file_data.append(value7)
                    separate_file.append(file_data)
                    file_data = []
                if marketName=="mgp-dayahead-prices" or marketName=="mgp-conventional-prices" :
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1 = re.findall("<PUN>(.*?)</PUN>", str(file_content), re.I)
                    value2 = re.findall("<NAT>(.*?)</NAT>", str(file_content), re.I)
                    value3 = re.findall("<CNOR>(.*?)</CNOR>", str(file_content), re.I)
                    value4 = re.findall("<CSUD>(.*?)</CSUD>", str(file_content), re.I)
                    value5 = re.findall("<NORD>(.*?)</NORD>", str(file_content), re.I)
                    value6 = re.findall("<SARD>(.*?)</SARD>", str(file_content), re.I)
                    value7 = re.findall("<SICI>(.*?)</SICI>", str(file_content), re.I)
                    value8 = re.findall("<SUD>(.*?)</SUD>", str(file_content), re.I)
                    value9 = re.findall("<AUST>(.*?)</AUST>", str(file_content), re.I)
                    value10 = re.findall("<BRNN>(.*?)</BRNN>", str(file_content), re.I)
                    value11 = re.findall("<COAC>(.*?)</COAC>", str(file_content), re.I)
                    value12 = re.findall("<CORS>(.*?)</CORS>", str(file_content), re.I)
                    value13 = re.findall("<FOGN>(.*?)</FOGN>", str(file_content), re.I)
                    value14 = re.findall("<FRAN>(.*?)</FRAN>", str(file_content), re.I)
                    value15 = re.findall("<GREC>(.*?)</GREC>", str(file_content), re.I)
                    value16 = re.findall("<MFTV>(.*?)</MFTV>", str(file_content), re.I)
                    value17 = re.findall("<PRGP>(.*?)</PRGP>", str(file_content), re.I)
                    value18 = re.findall("<ROSN>(.*?)</ROSN>", str(file_content), re.I)
                    value19 = re.findall("<SLOV>(.*?)</SLOV>", str(file_content), re.I)
                    value20 = re.findall("<SVIZ>(.*?)</SVIZ>", str(file_content), re.I)
                    value21 = re.findall("<BSP>(.*?)</BSP>", str(file_content), re.I)
                    value22 = re.findall("<MALT>(.*?)</MALT>", str(file_content), re.I)
                    value23 = re.findall("<XAUS>(.*?)</XAUS>", str(file_content), re.I)
                    value24 = re.findall("<XFRA>(.*?)</XFRA>", str(file_content), re.I)
                    file_data.append(E1)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value3)
                    file_data.append(value4)
                    file_data.append(value5)
                    file_data.append(value6)
                    file_data.append(value7)
                    file_data.append(value8)
                    file_data.append(value9)
                    file_data.append(value10)
                    file_data.append(value11)
                    file_data.append(value12)
                    file_data.append(value13)
                    file_data.append(value14)
                    file_data.append(value15)
                    file_data.append(value16)
                    file_data.append(value17)
                    file_data.append(value18)
                    file_data.append(value19)
                    file_data.append(value20)
                    if value1!=[]:
                        file_data.append(value21)
                        file_data.append(value1)
                        file_data.append(value2)
                        file_data.append(value23)
                        file_data.append(value24)
                    file_data.append(value22)
                    separate_file.append(file_data)
                    file_data = []
                if marketName=="mgp-additional-demand-bid-offers":
                    E1 = re.findall("<Mercato>(.*?)</Mercato>", str(file_content), re.I)
                    Date = re.findall("<Data>(.*?)</Data>", str(file_content), re.I)
                    Hour = re.findall("<Ora>(.*?)</Ora>", str(file_content), re.I)
                    value1 = re.findall("<CNOR_BID>(.*?)</CNOR_BID>", str(file_content), re.I)
                    value2 = re.findall("<CSUD_BID>(.*?)</CSUD_BID>", str(file_content), re.I)
                    value3 = re.findall("<NORD_BID>(.*?)</NORD_BID>", str(file_content), re.I)
                    value4 = re.findall("<SARD_BID>(.*?)</SARD_BID>", str(file_content), re.I)
                    value5 = re.findall("<SICI_BID>(.*?)</SICI_BID>", str(file_content), re.I)
                    value6 = re.findall("<SUD_BID>(.*?)</SUD_BID>", str(file_content), re.I)
                    value7 = re.findall("<CNOR_OFF>(.*?)</CNOR_OFF>", str(file_content), re.I)
                    value8 = re.findall("<CSUD_OFF>(.*?)</CSUD_OFF>", str(file_content), re.I)
                    value9 = re.findall("<NORD_OFF>(.*?)</NORD_OFF>", str(file_content), re.I)
                    value10 = re.findall("<SARD_OFF>(.*?)</SARD_OFF>", str(file_content), re.I)
                    value11 = re.findall("<SICI_OFF>(.*?)</SICI_OFF>", str(file_content), re.I)
                    value12 = re.findall("<SUD_OFF>(.*?)</SUD_OFF>", str(file_content), re.I)
                    file_data.append(E1)
                    file_data.append(Date)
                    file_data.append(Hour)
                    file_data.append(value1)
                    file_data.append(value2)
                    file_data.append(value3)
                    file_data.append(value4)
                    file_data.append(value5)
                    file_data.append(value6)
                    file_data.append(value7)
                    file_data.append(value8)
                    file_data.append(value9)
                    file_data.append(value10)
                    file_data.append(value11)
                    file_data.append(value12)
                    separate_file.append(file_data)
                    file_data = []
            rawFileName = file_writing(separate_file, datasourceName, marketName,headers)
            separate_file = []
            headers=[]
            return rawFileName
        finally:
            print 'closing'
            zf.close()
            # os.remove(zipFileName)
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
                                 scraperParameterName,POST_CONTENT)
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
            #     os.remove(filename)
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

