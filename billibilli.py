import requests
import time

from stem import Signal
from stem.control import Controller
def renew_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        print("Success!")
        controller.signal(Signal.NEWNYM)
        print("New Tor connection processed")



cookie = 'bsource=search_google; _uuid=947D28E2-A126-BC65-0D1F-08F3D117263134039infoc; buvid3=38A5EA74-271D-40BF-B6EE-891EB23BA42D18559infoc; bfe_id=f197415d50c3ae88d0c168156836d178; LIVE_BUVID=AUTO8316113442625005; sid=5byhcy19; PVID=2'


header = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

def get_current_ip():
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'

    try:
        r = session.get('http://httpbin.org/ip')
    except Exception as e:
        print(str(e))
    else:
        return r.text

channel_id = "94601633"
# Request to get the total
url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn=1&ps=500&order=desc'.format(channel_id)
req = requests.get(url,headers=header)
total = req.json()["data"]["total"] 
print(len(req.json()["data"]["list"]))

counter = 0
# request to get the full list
page_number = int(total/50)+1
for i in  range(5): # not logged in user || otherwise use range(page_number):
    url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn={}&ps=50&order=desc'.format(channel_id,i+1)
    req = requests.get(url,headers=header,proxies={"sock5":"127.0.0.1:9050"})
    if req.status_code == 200:
        try:
            if req.json()["code"] == 22007:
                # change ip 
                renew_ip()
                # reissue request
                url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn={}&ps=50&order=desc'.format(channel_id,i+1)
                req = requests.get(url,headers=header,proxies={"https":"127.0.0.1:9050"})
            fans = req.json()["data"]["list"]
            counter += len(fans)
            time.sleep(3)
            for fan in fans:
                print("====================== BEGIN ================")
                print("the fan name is : {}".format(fan["uname"]))
                print("the fan id is : {}".format(fan["mid"]))
                print("the fan avatar is : {}".format(fan["face"]))
                print("the fan subscription date is (timestamp): {}".format(fan["mtime"]))
                print("====================== END ================")
        except Exception as e:
            print(e)
            print(req.text)
        print(get_current_ip())
        print("Page #{}".format(i+1))
print(counter)