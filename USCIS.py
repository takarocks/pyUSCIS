# -*- coding: utf-8 -*-

#######################################
#
# USCIS case status checker - urllib3
#
# Author:  Taka Kitazume
# Date:    Sep 9, 2021
# Version: 0.2
#
#######################################

import urllib3
import os, config
import re

HOSTNAME    = os.getenv('USCIS_CONFIG_HOSTNAME',config.USCIS_CONFIG['hostname'])
ENDPOINT    = os.getenv('USCIS_CONFIG_ENDPOINT',config.USCIS_CONFIG['endpoint'])
QUERYTYPE   = os.getenv('USCIS_CONFIG_QUERYTYPE',config.USCIS_CONFIG['querytype'])

def getStatus(caseid, querytype=QUERYTYPE):
    output = None
    url = 'https://' + HOSTNAME + ENDPOINT
    payload = {'appReceiptNum': caseid, 'initCaseSearch': querytype}

    http = urllib3.PoolManager()
    r = http.request('POST', url, fields=payload)

    # Check HTTP status
    if int(r.status/100) == 2:
        # Success, get body
        body = r.data.decode('utf-8')
        # Check error message
        errcheck = re.search('(<div id="formErrorMessages">)(.*?)</div>', body, re.DOTALL)
        errmsg = re.sub('<.*?>',' ',errcheck.group(2).strip())
        if len(errmsg) > 0:
            # Looks like the payload was incorrect.
            output = {
                "err": "1",
                "status": " ".join(errmsg.split()),
                "desc": ""
            }
        else:
            # Successful. Use regex to retrieve the main status message and the details.
            # Current html format is <h1>STATUS</h1><p>DESCRIPTION</p> in multiple lines.
            result = re.search('<h1>(.*?)</h1>.*?<p>(.*?)</p>', body, re.DOTALL)
            output = {
                "err": "0",
                "status": result.group(1),
                "desc": result.group(2)
            }
    else:
        # http status error outside of 2xx
        output = {
            "err": "1",
            "status": 'Error ' + r.status,
            "desc": ""
        }

    return output
