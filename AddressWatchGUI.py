#!/usr/bin/python
import datetime
import json
import time
import urllib
import Tkinter
import re
    
def load(a):
    addresses = ''
    with open('addresses.txt') as fp:
        for line in fp:
            if not re.match(r'^\s*$', line):
                addresses += line
    a.insert(Tkinter.INSERT, addresses)

def check(r, a):
    # Save input in address text widget
    strs = str(a.get('1.0',Tkinter.END)).split()
    with open('addresses.txt', 'w') as fp:
        for line in strs:
            if not re.match(r'^\s*$', line):
                fp.write(line + '\n')

    # Delete any text already in the results text widget
    r.delete('1.0', Tkinter.END)
    results = ''
    # Read DCR Addresses from addresses.txt file
    with open('addresses.txt') as f:
        addresses = f.readlines()
    addresses = [x.strip() for x in addresses]

    # Make API call to check addresses for use
    for address in addresses:
        result  = urllib.urlopen('https://explorer.dcrdata.org/api/address/' + address).read()
        try:
            jsonStr = json.loads(result)
            values = jsonStr['address_transactions']
            total = 0
            for x in values:
                total += x['value']
            if (total > 0):
                results += address + ': Activity Detected!\n'
            else:
                results += address + ': No Activity Detected\n'
            
        except:
            pass
            results += address + ': Address unused (or malformed)\n'
    r.insert(Tkinter.INSERT, results)

def main():
    root = Tkinter.Tk()

    c = Tkinter.Canvas(root, width=600)
    c.pack()

    l1 = Tkinter.Label(c, text="Enter addresses you'd like to track:")
    l1.pack()

    a = Tkinter.Text(c, height=10)
    a.pack()

    ca = Tkinter.Button(c, text='Check Activity', command=lambda:check(r, a))
    ca.pack()

    l2 = Tkinter.Label(c, text='Results:')
    l2.pack()

    r = Tkinter.Text(c, height=10)
    r.pack()

    x = Tkinter.Button(c, text='Close', command=root.destroy)
    x.pack()

    load(a)

    root.mainloop()

if __name__ == '__main__':
    main()
