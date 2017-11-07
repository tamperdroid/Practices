import incapsula,requests

session = requests.Session()

proxy="http://172.20.240.251:3130"

header={
"Host":"www.generalpants.com.au",
"Referer": "https://www.generalpants.com.au/womens",
"Accept": "application/json, text/plain, */*"
}

ses=session.get('https://www.generalpants.com.au/category/womens',proxies={'http': proxy},headers=header,verify=False)
print ses.content
print ses.status_code

# response = incapsula.crack(session,ses)
# print response
