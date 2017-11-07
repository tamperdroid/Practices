import requests,re,time,sys,os,xlsxwriter
marketname=sys.argv[1]
tempFilePath = "D:/01_2017/19/entsoetemp/"
if not os.path.exists(tempFilePath):
    os.makedirs(tempFilePath)

url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"
url=requests.get(url)
con1=re.findall("A\.10\.\s*Areas</h3>([\w\W]*?)_code_samples",str(url.content),re.I)
con2=re.findall(r"<tr>.*?class\=\"tableblock\">(.*?)</p>",str(con1),re.I)

ping_count= 0
success_count = 0

print marketname
def ping_Save(formed_url,marketname):
    global ping_count
    global success_count

    ping1 = requests.get(formed_url, verify=False)
    if ping1.status_code == 200:
        success_count += 1
        with open(tempFilePath + "url_list_" + str(marketname) + ".txt", "ab") as f:
            f.write(str(success_count) + "\t" + str(formed_url) + "\n")
    ping_count += 1
    with open(tempFilePath + "eic_codes_" + str(marketname) + ".txt", "ab") as f:
        f.write(str(ping_count) + "\t" + str(eic) + "\t" + str(ping1.status_code) + "\n")



if marketname=="Actual Total Load":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A65&processType=A16&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)
elif marketname == "Day-Ahead Total Load Forecast":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A65&processType=A01&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Week-Ahead Total Load Forecast":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A65&processType=A31&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)
elif marketname == "Month-Ahead Total Load Forecast":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A65&processType=A32&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url,marketname)
elif marketname == "Year-Ahead Total Load Forecast":
    marketname=marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A65&processType=A33&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Year-Ahead Forecast Margin":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A70&processType=A33&outBiddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)
#
elif marketname=="Redispatching":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A63&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Countertrading":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A91&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Costs of Congestion Management":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A92&in_Domain="+str(eic)+"&out_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Installed Generation Capacity Aggregated":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A68&processType=A33&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Installed Generation Capacity per Unit":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A71&processType=A33&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Day-ahead Aggregated Generation":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A71&processType=A01&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)
elif marketname == "Day-ahead Generation Forecasts for Wind and Solar":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A69&processType=A01&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Actual Generation Output per Generation Unit":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A73&processType=A16&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201601012300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Aggregated Generation per Type":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A75&processType=A16&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Aggregated Filling Rate of Water Reservoirs and Hydro Storage Plants":
    marketname = marketname.replace(" ", "")
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A72&processType=A16&in_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

# transperancy
# for eic1 in con2[1:]:
#     for eic in con2[1:]:
#         formed_url="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A90&in_Domain="+str(eic1)+"&out_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
#         print formed_url
#         ping1=requests.get(formed_url,verify=False)
#         print ping1.status_code
#         ping_count+=1
#         with open("eic_codes_test1.txt","ab") as f:
#             f.write(str(ping_count)+"\t"+str(eic)+"\t"+str(eic1)+"\t"+str(ping1.status_code)+"\n")
# print "done"

