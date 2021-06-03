# -*- coding: utf-8 -*-

#######################################
#
# pyUSCIS
#
# USCIS case status checker
#
# Author:  Taka Kitazume
# Date:    June 3, 2021
# Version: 0.1
#
#######################################

import requests
import os, sys, config, getopt
import re

SYNTAX_MSG  = 'python pyUSCIS.py -c CASEID [-q QUERYTYPE]'
HOSTNAME    = os.getenv('USCIS_CONFIG_HOSTNAME',config.USCIS_CONFIG['hostname'])
ENDPOINT    = os.getenv('USCIS_CONFIG_ENDPOINT',config.USCIS_CONFIG['endpoint'])

def getStatus(url, caseid, querytype):
    output = None

    payload = {'appReceiptNum': caseid, 'initCaseSearch': querytype}
    r = requests.post(url, data=payload)
    #print(r.text)
    #print(r.status_code)

    # Check HTTP status
    if r.status_code == requests.codes.ok:
        # Check error message
        errcheck = re.search('(<div id="formErrorMessages">)(.*?)</div>', r.text, re.DOTALL)
        errmsg = re.sub('<.*?>',' ',errcheck.group(2).strip())
        if len(errmsg) > 0:
            output = " ".join(errmsg.split())
        else:
            result = re.search('(<h1>)(.*)(</h1>)', r.text, re.DOTALL)
            output = result.group(2)
    else:
        output = 'Error ' + r.status_code

    return output


def main(argv):
    url = 'https://' + HOSTNAME + ENDPOINT
    caseid = None
    querytype = 'CHECK STATUS'

    if len(sys.argv) <= 1:
        print(SYNTAX_MSG)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:")

    except getopt.GetoptError:
        print(SYNTAX_MSG)
        sys.exit(2)

    for opt, arg in opts:
        if (opt == '-c'):
            caseid = arg
        elif (opt == '-q'):
            querytype = arg

    #print('URL={} CASEID={} QUERYTYPE={}'.format(url,caseid,querytype))

    status = getStatus(url, caseid, querytype)

    print('CASEID [{}]: {}'.format(caseid,status))


if __name__ == "__main__":
    main(sys.argv[1:])
