import requests,re
url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"
url=requests.get(url)
con1=re.findall("A\.10\.\s*Areas</h3>([\w\W]*?)_code_samples",str(url.content),re.I)
con2=re.findall(r"<tr>.*?class\=\"tableblock\">(.*?)</p>",str(con1),re.I)
ping_count = 0
for i,eic1 in enumerate(con2[1:20]):
    print "--------------------------------------",i
    for eic in con2[1:20]:
        formed_url="https://transparency.entsoe.eu/api?securityToken=5cd9c738-3b32-4b95-86e9-f9c8b2cd3bb6&documentType=A90&in_Domain="+str(eic1)+"&out_Domain="+str(eic)+"&periodStart=201512312300&periodEnd=201612312300"
        # print formed_url
        ping1=requests.get(formed_url,verify=False)
        print ping1.status_code
        ping_count+=1
        # with open("eic_codes_test1.txt","ab") as f:
        #     f.write(str(ping_count)+"\t"+str(eic)+"\t"+str(eic1)+"\t"+str(ping1.status_code)+"\n")
        print eic
        print ping_count
print "done"