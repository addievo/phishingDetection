# Functions We Need
# Domain, IP, @, URL Length, URL Depth, Redirect (//_), https,
# url shortening, prefix/suffix (using - or @ in domain name),
# DNS records (if avail), Website Traffic (if avail, ranking),
# Domain Age, Domain Expiry, iFrame, (If domain uses iFrame in url webpage)
# Mouse Over, Right click, Web Forwards
from datetime import datetime
import ipaddress
import urllib
import urllib.request
import whois
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import requests


# We dropped domain in training data

# IP

def havingIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


# @ sign
def haveAtSign(url):
    if '@' in url:
        at = 1
    else:
        at = 0
    return at


# URL length if longer than 54 characters mark as phishing

def urlLength(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1
    return length


# Return URL depth

def urlDepth(url):
    s = url.split('/')
    depth = 0
    for i in range(len(s)):
        if len(s[i]) != 0:
            depth = depth + 1
    return depth


# Checking number of redirections, if greater than 6 mark as phishing
def redirection(url):
    pos = url.rfind('//')
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0


# Check if https is in the url
def httpsInUrl(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 1
    else:
        return 0


# Check if url is shortened

def urlShort(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                          r"tr\.im|link\.zip\.net"
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


# Check if prefix or suffix is used in domain name

def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0


# website traffic

# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
        rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": url.domain})

        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
        if global_rank > 0 and global_rank < 100000:
            return 1
        return -1
    except:
        return -1


# domain age


def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain / 30) < 6):
            age = 1
        else:
            age = 0
    return age


# domain expiry

def domainExpiry(domain_name):
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end / 30) < 6):
            end = 0
        else:
            end = 1
    return end


# iFrame

def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 1
        else:
            return 0


# Mouse Over

def mouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


# Right Click (disabled)

def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 1
        else:
            return 0


# Check how many times a website has been redirected

def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        elif len(response.history) <= 4:
            return 1
        else:
            return 0


# Computing URL features

def featureExtraction(url):
    features = []

    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(urlLength(url))
    features.append(urlDepth(url))
    features.append(redirection(url))
    features.append(httpsInUrl(url))
    features.append(urlShort(url))
    features.append(prefixSuffix(url))

    # Domain based features (Checking DNS Record)

    dns = 1
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except Exception as e:
        print(f"Couldn't get whois for {url}, error: {e}")
        dns = 0

    features.append(dns)
    #features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainExpiry(domain_name))

    # HTML & Javascript based features

    try:
        response = requests.get(url)
    except:
        response = ""

    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))

    return features

