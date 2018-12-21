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

packetCount = '1'

def testHosts():
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

        # assign relevant list items
        packet = report[2]
        avg = report[4]
        print (host +" packet loss = "+packet+"%, round-trip average = "+avg)

        # create tuple and append it to the list
        myList.append((float(avg),host))

    myList=sorted(myList,key=lambda host: host[0])
    return (myList[0])

results = testHosts()
print (str ("\nHost with the quickest return trip is "+results[1]) + " (" + str(results[0])+" ms)")
