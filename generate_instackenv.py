#!/usr/bin/python

import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="data file, default: %s" % ('./ipmi_list'), action="store", metavar="FILE", default='./ipmi_list')
parser.add_argument("-d", "--delimiter", help="set the delimiter char, default is ' '", action="store", metavar='DELIM', default=' ')
parser.add_argument("-D", "--driver", help="set the driver type to use char, default is 'pxe_ipmitool'", action="store", metavar='TYPE', default='pxe_ipmitool')

args = parser.parse_args()
filename = args.filename
delimiter = args.delimiter
driver = args.driver

if not os.path.isfile(filename):
    print "ipmi list file not found"
    exit(1)

try:
    with open(filename, 'r') as f:
        lines = f.readlines()
except IOError as e:
    print "Error opening file"

instackenv = {}
instackenv['nodes'] = []

try:
    for line in lines:
        elt = line.strip().split(delimiter)
        tmp = {}
        tmp['mac'] = []
        tmp['mac'].append(elt[0])
        tmp['pm_user'] = elt[2]
        tmp['pm_password'] = elt[3]
        tmp['pm_addr'] = elt[1]
        tmp['pm_type'] = driver
        instackenv['nodes'].append(tmp)
except IndexError as e:
    print "Error creating dict: %s" % (e)
    exit(1)


jsonarray = json.dumps(instackenv)

print jsonarray
