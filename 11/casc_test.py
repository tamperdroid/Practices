import requests,sys,time,re
#
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
todate="2017-01-09T00:00:00"
fromDate = "2017-01-08T00:00:00"

write_list=[]
a = []
for i in range(50):
    a.append(i)
print a
ping_count = 0
for meta_indx,meta_id in enumerate(meta_ids):
    # print meta_id["Id"]
    # if meta_indx>1:
    #     break
    dropdown_ids = dic['responses'][1]["Results"][0]['Result']['Results']
    dropdown_ids_to_url = ""
    for dropdown_indx,dropdown_id in enumerate(dropdown_ids):
        # print dropdown_id["Id"]
        # dropdown_ids_to_url=dropdown_id["Id"]
        # if dropdown_indx in a[2:20]:
        #     continue

        # if dropdown_indx ==41:
        #     dropdown_ids_to_url += str("%22" + dropdown_id["Id"]) + "%22"
        #     break

        if len(dropdown_ids) > 1:
            if dropdown_indx==len(dropdown_ids)-1:
                dropdown_ids_to_url += str("%22"+dropdown_id["Id"]) + "%22"
            else:
                dropdown_ids_to_url+=str("%22"+dropdown_id["Id"])+"%22,"
        else:
            dropdown_ids_to_url=str("%22"+dropdown_id["Id"])+"%22"
        # print "dropdown_indx", dropdown_indx
        # if  ping_count==10:
        #     ping_count = 0
        #     time.sleep(6)
        # ping_count+=1
    # print dropdown_ids_to_url
    # print ping1.status_code

    baseUrl="http://www.jao.eu/Export/Excel/?actionId="+actionId[0]+"&excelExportId="+str(exportId[0])+"&parameters="
    download_url = "{%22AuctionTypeId%22:%22"+str(meta_id["Id"])+"%22,%22BorderIds%22:[" + str(
            dropdown_ids_to_url) + "],%22FromDate%22:%22" + str(fromDate) + "%22,%22ToDate%22:%22" + str(
            todate) + "%22,%22AuctionId%22:%22%22}"
    # download_url="{%22AuctionTypeId%22:%22db5b74d2-0523-4dea-9031-1993095f4734%22,%22BorderIds%22:["+str(dropdown_ids_to_url)+"],%22FromDate%22:%22"+str(fromDate)+"%22,%22ToDate%22:%22"+str(todate)+"%22,%22AuctionId%22:%22%22}"
    # print download_url
    # url_download=eval(download_url)
    try:
        download_ids=str(baseUrl)+str(download_url)
        print "download_ids",download_ids
        # print str(download_ids)
        ping3=s.get(download_ids)
        with open("ping"+str(meta_indx)+".xlsx","wb") as f:
            f.write(str(ping3.content))
        # write_list.append(str(ping2.content))
        #     f.write(str(data))
        print ping3.status_code
        with open("status_code.txt","ab") as f:
            f.write(str(ping3.status_code)+",")
        time.sleep(120)
        ping3.cookies.clear()
        print ping3.cookies.keys()
        print "cookies cleared"

    except Exception as e:
        print "Exception::" + str(e)
        print   "Error on extraction for " + str(sys.exc_traceback.tb_lineno)

