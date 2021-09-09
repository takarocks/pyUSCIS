# -*- coding: utf-8 -*-

#######################################
#
# USCIS case status checker - console app
#
# Author:  Taka Kitazume
# Date:    Sep 9, 2021
# Version: 0.2
#
#######################################

import USCIS
import sys, getopt

SYNTAX_MSG  = 'python app.py -c CASEID [-q QUERYTYPE]'

def main(argv):
    caseid = None
    querytype = None

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

    if querytype:
        output = USCIS.getStatus(caseid, querytype)
    else:
        output = USCIS.getStatus(caseid)

    print('CASEID [{}]: {} \n{}'.format(caseid,output['status'],output['desc']))


if __name__ == "__main__":
    main(sys.argv[1:])
