# Functions We Need
# Domain, IP, @, URL Length, URL Depth, Redirect (//_), https,
# url shortening, prefix/suffix (using - or @ in domain name),
# DNS records (if avail), Website Traffic (if avail, ranking),
# Domain Age, Domain Expiry, iFrame, (If domain uses iFrame in url webpage)
# Mouse Over, Right click, Web Forwards
import ipaddress
from urllib.parse import urlparse


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

#