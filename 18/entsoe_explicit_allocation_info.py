import requests,re,time
url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"
url=requests.get(url)
con1=re.findall("A\.10\.\s*Areas</h3>([\w\W]*?)_code_samples",str(url.content),re.I)
con2=re.findall(r"<tr>.*?class\=\"tableblock\">(.*?)</p>",str(con1),re.I)
ping_count = 0
if marketname=="Explicit_Allocation_Information_Capacity":


for con_man_agree in ["A01","A02","A03","A04","A05","A06","A07","A13"]:
    # for auc in ["A01","A02"]:
        for eic1 in con2[1:]:
            for eic in con2[1:]:
                formed_url="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A25&businessType=A43&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201601012300&periodEnd=201601022300"
                print formed_url
                formed_url1="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A25&businessType=B05&contract_MarketAgreement.Type="+str(con_man_agree)+"&in_Domain="+str(eic)+"&out_Domain="+str(eic1)+"&periodStart=201601012300&periodEnd=201601022300"
                ping1=requests.get(formed_url,verify=False)
                time.sleep(3)
                ping2 = requests.get(formed_url1, verify=False)
                time.sleep(3)
                print ping1.status_code
                ping_count+=1
                with open("eic_codes_explicity_a_i.txt","ab") as f:
                    f.write(str(ping_count)+"\t"+str(con_man_agree)+"\t"+str(eic)+"\t"+str(eic1)+"\t"+str(ping1.status_code)+"\t"+str(ping2.status_code)+"\n")
print "done"

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

