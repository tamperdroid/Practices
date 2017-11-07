import  re,requests

ping1=requests.get("https://alsi.gie.eu/#/historical/1")
with open("ping1.html","wb") as f:
    f.write(str(ping1.content))

print ping1.status_code