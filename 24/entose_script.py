import requests,re,time,sys,os
marketname=sys.argv[1]
tempFilePath = "C:/entsoe_test/entsoetemp/"
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

#Load domain
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

#Transmission domain
elif marketname == "Forecasted Capacity":
    marketname = marketname.replace(" ", "")
    for con_man_agree in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        # for auc in ["A01", "A02"]:
            for eic1 in con2[1:]:
                for eic in con2[1:]:
                    formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A61&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201612312300"
                    print formed_url
                    ping_Save(formed_url, marketname)

elif marketname == "Offered Capacity":
    marketname = marketname.replace(" ", "")
    for con_man_agree in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        for auc in ["A01", "A02"]:
            for eic1 in con2[1:]:
                for eic in con2[1:]:
                    formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A31&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&auction.Type="+str(auc)+"&periodStart=201601012300&periodEnd=201601022300"
                    print formed_url
                    ping_Save(formed_url, marketname)
elif marketname == "Flow-based Parameters":
    marketname = marketname.replace(" ", "")
    for con_man_agree in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        for processType in ["A01","A02"]: #complete processtype["A01","A02","A16","A31","A32","A33"]:
                for eic in con2[1:]:
                    formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=B11&processType="+str(processType)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201601012300"
                    print formed_url
                    ping_Save(formed_url, marketname)
elif marketname == "Explicit Allocation Information (Capacity)":
    marketname = marketname.replace(" ", "")
    for con_man_agree in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        for businesstype in ["A43","B05"]:
            for eic1 in con2[1:]:
                for eic in con2[1:]:
                    formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A25&businessType="+str(businesstype)+"&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201601012300&periodEnd=201601022300"
                    print formed_url
                    ping_Save(formed_url, marketname)

elif marketname == "Explicit Allocation Information (Revenue only)":
    marketname = marketname.replace(" ", "")
    for con_man_agree in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        # for businesstype in ["A43", "B05"]:
            for eic1 in con2[1:]:
                for eic in con2[1:]:
                    formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A25&businessType=B07&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201601012300&periodEnd=201601022300"
                    print formed_url
                    ping_Save(formed_url, marketname)

elif marketname == "Scheduled Day Ahead Commercial Exchanges":
    marketname = marketname.replace(" ", "")
    for eic1 in con2[1:]:
        for eic in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A09&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Physical Flows":
    marketname = marketname.replace(" ", "")
    for eic1 in con2[1:]:
        for eic in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A09&in_Domain=" + str(
                eic) + "&out_Domain=" + str(eic1) + "&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

#Congestion domain
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

#Generation domain
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

#Balancing domain
elif marketname == "Amount of Balancing Reserves Under Contract":
    marketname = marketname.replace(" ", "")
    for typ_mrkt_agrmnt in ["A01","A02","A03","A04","A05","A06","A07","A13"]:
        for eic in con2[1:]:
        # for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A81&type_MarketAgreement.Type="+str(typ_mrkt_agrmnt)+"&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201601012300"
            print formed_url
            ping_Save(formed_url, marketname)
elif marketname == "Prices of Procured Balancing Reserves":
    marketname = marketname.replace(" ", "")
    for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
        for eic in con2[1:]:
            # for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A89&type_MarketAgreement.Type="+str(typ_mrkt_agrmnt)+"&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201601012300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Accepted Aggregated Offers":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A82&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)


elif marketname == "Activated Balancing Energy":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A83&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Prices of Activated Balancing Energy":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A84&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Imbalance Prices":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A85&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Total Imbalance Volumes":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A86&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Financial Expenses and Income for Balancing":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A87&controlArea_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Cross-border Balancing":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        for eic1 in con2[1:]:
            # for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A88&acquiring_Domain="+str(eic)+"&connecting_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201601010100"
            print formed_url
            ping_Save(formed_url, marketname)

#Outages
elif marketname == "Unavailability of Consumption Units":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A76&biddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Unavailability of Transmission Infrastructure":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic1 in con2[1:]:
        for eic in con2[1:]:
            # for eic1 in con2[1:]:
            formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A78&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201512312300&periodEnd=201612312300"
            print formed_url
            ping_Save(formed_url, marketname)

elif marketname == "Unavailability of Offshore Grid Infrastructure":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A79&biddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Unavailability of Generation Units":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A80&biddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)

elif marketname == "Unavailability of Production Units":
    marketname = marketname.replace(" ", "")
    # for typ_mrkt_agrmnt in ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A13"]:
    for eic in con2[1:]:
        # for eic1 in con2[1:]:
        formed_url = "https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A773&biddingZone_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        print formed_url
        ping_Save(formed_url, marketname)
