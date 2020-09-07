#!/usr/bin/python
# - RevIP
#   | Date: 10/03/2018
#   | Author: insane-dotin
#   | Description: simple reverse IP lookup tool that combines multiple API to achieve effective result.

import requests
import sys
requests.packages.urllib3.disable_warnings()
from socket import gethostbyname
def xverify(domain, comparator, verifyb):
    if not verifyb: 
        return True
    else:
        try: 
            ip = gethostbyname(domain)
        except:
            return False
        else:
            if ip == comparator:
                return True
            else:
                return False

def main():
    results = []
    if len(sys.argv) != 3:
        print("""\
   ___           _______ 
  / _ \\___ _  __/  _/ _ \\  | RevIP: Reverse IP Lookup Tool
 / , _/ -_) |/ // // ___/  | [ v1.0 beta ]
/_/|_|\\__/|___/___/_/      | https://github.com/insane-dotin
usage: {} <ip/domain> <mode:1(verbose/unverified);2(raw/unverified);3(verbose/verified);(raw/verified)>
example: {} example.com 1
       
mode help:
    1 verbose/unverified    : verbose output, not verifying ip address of results
    2 raw/unverified        : raw output, not verifying ip address of results
    3 verbose/verified      : verbose output, verify ip address of results
    4 raw/verified          : raw output, verify ip address of results
    """.format(sys.argv[0], sys.argv[0]))
        sys.exit()
    ip = gethostbyname(sys.argv[1])
    mode = int(sys.argv[2])
    verbose = True
    verify = False
    if mode == 2 or mode == 4:
        verbose = False
    if mode == 3 or mode == 4:
        verify = True
    api_1 = requests.get("http://reverseip.logontube.com/?url={}&output=json".format(ip)).json()
    if 'response' in api_1:
        for dom in api_1['response']['domains']:
            if dom in results:
                continue
            else:
                results.append(dom)
    api_2 = requests.post("https://domains.yougetsignal.com/domains.php", data={'remoteAddress': ip}, verify=False, allow_redirects=False, headers={'X-Requested-With': 'XMLHttpRequest'}).json()
    if api_2['status'] == 'Success':
        if api_2['domainCount'] != "0":
            for dom in api_2['domainArray']:
                dom = dom[0]
                if dom in results:
                    continue
                else:
                    if xverify(dom, ip, verify):
                        results.append(dom)
    api_3 = requests.get("http://api.hackertarget.com/reverseiplookup/?q={}".format(ip)).text.split("\n")
    if len(api_3) > 0:
        for dom in api_3:
            dom = dom.rstrip()
            if dom in results or dom == "":
                continue
            else:
                results.append(dom)
    results.sort()
    if verbose:
        com = ""
        if not verify:
            com = "un"
        print("[ got {} {}verified domains ]".format(len(results), com))
    num = 1
    for dom in results: 
        com = ""
        if verbose:
            com = "{}. ".format(num)
        print(com + dom)
        num += 1
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(": SIGINT detected! Exiting . . .")
        sys.exit()
    except Exception as e:
        print("Exception: {}".format(str(e)))
        pass
