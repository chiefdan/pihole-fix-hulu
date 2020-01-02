import dns.resolver
import requests

# DNS Variables
dnshostnametocheck = 'www.google.com' # A domain to use for testing DNS
dnsserver = '8.8.8.8' # This should be your pi-hole address

# Edgerouter Variables
myusername = ''
mypassword = ''
erhost = ''
loginurl = f'https://{erhost}/'
configurl = f'https://{erhost}/api/edge/batch.json'
logindata = {'username': myusername,'password': mypassword}
configheaders = {'X-Requested-With': 'XMLHttpRequest'}

# Edgerouter Commands
enablenat = '{"DELETE":{"service":{"nat":{"rule":{"100":{"disable":null}}}}}}'
disablenat = '{"SET":{"service":{"nat":{"rule":{"100":{"disable":null}}}}}}'

# Requests Session
s = requests.Session()

def getdnsstatus(host, dnsresolver): # Check if DNS is working and return a boolean
    try:
        res = dns.resolver.Resolver()
        res.nameservers = [dnsresolver]
        res.query(host, lifetime=3)
        return True
    except dns.resolver.NXDOMAIN:
        return True
    except:
        return False

def login(): # Login to EdgeRouter
    output = s.post(loginurl, data=logindata, verify=False)
    return output

def sendcommands(data): # Push config json to EdgeRouter
    output = s.post(configurl, headers=configheaders, data=data, verify=False)
    return output

def main():
    dnsstatus = getdnsstatus(dnshostnametocheck, dnsserver)
    if dnsstatus == True:
        login()
        sendcommands(enablenat)
        
    if dnsstatus == False:
        login()
        sendcommands(disablenat)
        
if __name__ == "__main__":
    main()