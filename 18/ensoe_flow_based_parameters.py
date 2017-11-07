import requests,re
url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"
url=requests.get(url)
con1=re.findall("A\.10\.\s*Areas</h3>([\w\W]*?)_code_samples",str(url.content),re.I)
con2=re.findall(r"<tr>.*?class\=\"tableblock\">(.*?)</p>",str(con1),re.I)
ping_count = 0
# if marketname=

for process_type in ["A01","A02","A16","A31","A32","A33"]:
    # for auc in ["A01","A02"]:
        for eic1 in con2[1:]:
            for eic in con2[1:]:
                formed_url="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=B11&processType="+str(process_type)+"&in_Domain="+str(eic1)+"&out_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201601012300"
                print formed_url
                ping1=requests.get(formed_url,verify=False)
                print ping1.status_code
                ping_count+=1
                with open("eic_codes_Flow_based_Parameters.txt","ab") as f:
                    f.write(str(ping_count)+"\t"+str(process_type)+"\t"+str(eic)+"\t"+str(eic1)+"\t"+str(ping1.status_code)+"\n")
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

