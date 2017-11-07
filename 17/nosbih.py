import requests,re
cookies_url="http://www.nosbih.ba"

url="http://www.nosbih.ba/webservice/getDBData.asmx/getGrafPotrosnje"
s=requests.Session()
ping1=s.get(cookies_url)
print str(ping1.cookies)
sess_id=re.findall("ASP.NET_SessionId=(.*?)\s*for",str(ping1.cookies),re.I)

header1={
# "Host": "www.nosbih.ba",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
# "X-Requested-With": "XMLHttpRequest",
"Referer": "http://www.nosbih.ba/en/partneri/graph-consumption/23",
"Content-Type":"application/json; charset=utf-8",
"Cookie":"AspxAutoDetectCookieSupport=1;ASP.NET_SessionId="+str(sess_id[0])
# "Cookie": "AspxAutoDetectCookieSupport=1; ASP.NET_SessionId=vinlq0ajpi30cre3ngoprhln"
}
print header1
post_content="{datum:'16.01.2017'}"
ping2=s.post(url,data=post_content,headers=header1)
print ping2.status_code
print ping2.content



