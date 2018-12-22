'''
myPing
==============================================================================
Author:   RW Martin
Version:  1.1.0
Date:     22.12.2018
For documentation please visit https://github.com/rwmartin/myPing
==============================================================================
'''

import os
import re
import subprocess
import time
from typing import Any, Union

packetCount = '1'
reportLine=[]
index=0

timestr = time.strftime("%Y%m%d%H%M%S")
fileName: str = 'myPing-'+timestr+'.txt'

def testhosts(reportLine):
    myList = []
    # hosts.txt contains vultr sites
    hosts = os.path.join('hosts.txt')
    hostsFile = open(hosts, "r")
    lines = hostsFile.readlines()

    print("Sending " + packetCount + " packets each to " + str(lines.__len__()) + " hosts...")

    for host in lines:
        host = host.strip()
        # refer to Mac OSX ping usage for additional parameters
        args = ["ping", host, "-c"+packetCount, "-W1"]
        ping = subprocess.Popen(
            args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out = ping.communicate()
        report = re.findall("(\d+.\d+)",str(out[0]))

        #get host IP address
        ipAddr = re.findall("\d+.\d+.\d+.\d+", str(out[0]))[0]

        # assign relevant list items
        packet = report[2]
        if float(packet) == 100:
            avg = '9999.0'
        else:
            avg = report[4]

        info = host +" ("+ipAddr+") pkt loss = "+packet+"%, round-trip average = "+avg
        print (info)

        # create tuple and append it to the list
        myList.append((float(avg),host,ipAddr))

    myList=sorted(myList,key=lambda host: host[0])
    return (myList)

results = testhosts(reportLine)
status: str = (str ("\nHost with the quickest return trip is "+results[0][1] + " (" + str(float(results[0][0]))+" ms)"))
print (status)

for line in results:
    if line[0] == 9999:
        line[0]= "FAILED"
    info: Union[str, Any] = line[1] + " (" + line[2] + '), round-trip average = ' + str(line[0]) + '\n'
    results[index] = info
    index+=1

file = open(fileName,'w')
file.writelines(results)
file.writelines(status)
file.close()