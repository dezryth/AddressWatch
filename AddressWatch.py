import urllib
import json
import datetime
import time

# Print runtime
print datetime.datetime.now()

# Read DCR Addresses from addresses.txt file
with open("addresses.txt") as f:
    addresses = f.readlines()
addresses = [x.strip() for x in addresses]

# Make API call to check addresses for use
for address in addresses:
    result  = urllib.urlopen("http://explorer.dcrdata.org/api/address/" + address).read()
    try:
        jsonStr = json.loads(result)
        values = jsonStr["address_transactions"]
        total = 0
        for x in values:
            total += x["value"]
        if (total > 0):
            print address + ": Activity Detected!"
        else:
            print address + ": No Activity Detected"
        #print address + ": " + str(total)
    except:
        pass
        print address + ": Address unused (or malformed)"