import requests,sys,time,re,xlsxwriter,xlrd,imp,os
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



def merge_file(DataSourceID, datasourceName, marketName, spName, control, fileList):
    rawFile_time = str(titlecase(datasourceName)) + '_' + str(titlecase(marketName)) + '_' + date_time
    rawFileName = tempFilePath + str(str(rawFile_time).replace('-', '_')) + ".xlsx"
    rawFileName = "file.xlsx"
    workbook = xlsxwriter.Workbook(rawFileName)

    for li_indx, xls in enumerate(FileNames):
        insheet = xlrd.open_workbook(xls)
        sheet_count = len(insheet.sheets())
        for c in range(sheet_count):
            # need to add sheet index if sheet count increase
            outsheet = workbook.add_worksheet(str(xls))
            sh = insheet.sheet_by_index(c)
            for row_idx in xrange(sh.nrows):
                for col_idx in xrange(sh.ncols):
                    outsheet.write(row_idx, col_idx, sh.cell_value(row_idx, col_idx))
    workbook.close()

s=requests.Session()
ping1=requests.get("http://www.jao.eu/marketdata/export/overview")
with open("ping1.html","wb") as f:
    f.write(str(ping1.content))

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
#ids of each dropdown is collected
ping2=s.post(post_url,data=post_content_1,headers=header1)
print ping2.cookies.keys()
ping2.cookies.clear()
print "cookies cleared"

with open("ping2.html","wb") as f:
    f.write(str(ping2.content))
dic=eval(str(ping2.content))
meta_ids=dic['responses'][0]['Results'][0]['Result']['Results']
# print meta_ids
id="%22"+str(dic['responses'][1]["Results"][0]['Result']['Results'][0]["Id"])+"%22"
todate="2017-01-10T00:00:00"
fromDate = "2017-01-09T00:00:00"

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
    # print meta_id["Code"]
    # if meta_indx>1:
    #     break
    #form Border ids in to two
    dropdown_ids = dic['responses'][1]["Results"][0]['Result']['Results']
    for dropdown_indx,dropdown_id in enumerate(dropdown_ids):
        # print dropdown_id["Id"]
        # dropdown_ids_to_url=dropdown_id["Id"]
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
                # if dropdown_indx == 29:
        #     dropdown_ids_to_url += str("%22" + dropdown_id["Id"]) + "%22"
        #     break
        # if len(dropdown_ids) > 1:
        #     if dropdown_indx==len(dropdown_ids)-1:
        #         dropdown_ids_to_url += str("%22"+dropdown_id["Id"]) + "%22"
        #     else:
        #         dropdown_ids_to_url+=str("%22"+dropdown_id["Id"])+"%22,"
        # else:
        #     dropdown_ids_to_url=str("%22"+dropdown_id["Id"])+"%22"
        # print "dropdown_indx", dropdown_indx
        # if  ping_count==10:
        #     ping_count = 0
        #     time.sleep(6)
        # ping_count+=1
    # print dropdown_ids_to_url
    # print ping1.status_code
    for border_indx,border_id in  enumerate(urls_list):
        print "border_indx",border_indx
        if border_id == "":
            continue
        baseUrl="http://www.jao.eu/Export/Excel/?actionId="+actionId[0]+"&excelExportId="+str(exportId[0])+"&parameters="
        download_url = "{%22AuctionTypeId%22:%22"+str(meta_id["Id"])+"%22,%22BorderIds%22:[" + str(
            border_id) + "],%22FromDate%22:%22" + str(fromDate) + "%22,%22ToDate%22:%22" + str(
                todate) + "%22,%22AuctionId%22:%22%22}"
        # download_url="{%22AuctionTypeId%22:%22db5b74d2-0523-4dea-9031-1993095f4734%22,%22BorderIds%22:["+str(dropdown_ids_to_url)+"],%22FromDate%22:%22"+str(fromDate)+"%22,%22ToDate%22:%22"+str(todate)+"%22,%22AuctionId%22:%22%22}"
        # print download_url
        # url_download=eval(download_url)
        try:
            formed_url=str(baseUrl)+str(download_url)
            print ping_count,formed_url
            with open("urls.txt","ab") as f:
                f.write(str(ping_count)+str(formed_url)+"\n")
            # print str(formed_url)
            ping3=s.get(formed_url)
            ping_count+=1
            FileName=meta_id["Code"]+str(ping_count)
            with open(FileName+".xlsx","wb") as f:
                f.write(str(ping3.content))
            # write_list.append(str(ping2.content))
            #     f.write(str(data))
            print ping3.status_code
            # with open("status_code.txt","ab") as f:
            #     f.write(str(ping3.status_code)+",")
            # time.sleep(120)
            ping3.cookies.clear()
            print ping3.cookies.keys()
            print "cookies cleared"

        except Exception as e:
            print "Exception::" + str(e)
            print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)
        FileNames.append(FileName)
    print urls_list
    urls_list=[]
    dropdown_ids_to_url_1=""
    dropdown_ids_to_url_2=""
    dropdown_ids_to_url=""

merge_file(FileNames)
