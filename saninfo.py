#!/usr/bin/env python -t
# ************************************************************************
# * This tool shows 
# * This informations a extracted from 'prtconf -Dv' so you can use this
# * tool also 'offline' e.g. use explorer output 
# * 
# * Written By: Carsten Grzemba (cgrzemba@opencsw.org)
# * 
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at pkg/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at pkg/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
# ************************************************************************

from sys import exit, argv
from subprocess import Popen, PIPE
from re import findall, match, sub, compile
import argparse
import os
from socket import gethostname
import pdb

filename = ''
printShort = False
explo_prtconf = 'sysconfig/prtconf-vD.out'

hbalst = []

pcipaths = {'ORCL,SPARC-S7-2L': [
        'gibtsnicht',
'/pci@300/pci@1/pci@0/pci@11',
'/pci@302/pci@1/pci@0/pci@12',
'/pci@302/pci@1/pci@0/pci@13',
'/pci@300/pci@2/pci@0/pci@14',
'/pci@300/pci@2/pci@0/pci@15',
'/pci@302/pci@2/pci@0/pci@16',
'/pci@302/pci@2/pci@0/pci@17' ],
'ORCL,SPARC-S7-2': [
        'gibtsnicht',
    '/pci@300/pci@1/pci@0/pci@11',
    '/pci@300/pci@1/pci@0/pci@12',
    '/pci@300/pci@1/pci@0/pci@13',
    '/pci@300/pci@1/pci@0/pci@14',
],
'ORCL,SPARC-T4-2': [
    'pci@400/pci@2/pci@0/pci@8',
    'pci@500/pci@2/pci@0/pci@a',
    'pci@400/pci@2/pci@0/pci@4',
    'pci@500/pci@2/pci@0/pci@6',
    'pci@400/pci@2/pci@0/pci@0',
    'pci@500/pci@2/pci@0/pci@0',
    'pci@400/pci@1/pci@0/pci@8',
    'pci@500/pci@1/pci@0/pci@6',
    'pci@400/pci@1/pci@0/pci@c',
    'pci@500/pci@1/pci@0/pci@0',
    
],
'SUNW,SPARC-Enterprise': [ # M4000
    '/pci@0,600000/pci@0/pci@8/pci@0,1',
    '/pci@0,600000/pci@0/pci@9',
    '/pci@1,700000',
    '/pci@2,600000',
    '/pci@3,700000',
],
'ORCL,SPARC64-X': [ # M10-1
    '/pci@8000/pci@4/pci@0/pci@8',
    '/pci@8100/pci@4/pci@0/pci@1/',
    '/pci@8100/pci@4/pci@0/pci@9/',
]}

def usage():
    print """usage is:
list inforamtions for MPXIO devices
where options are:

    -f|--file <prtdiag -Dv Output file>
            file with the output of prtdiag -Dv
	--explorer <path>

    -s|--short list, list only devlink and WWN's
"""

class HBA(object):
    headprinted = False
    lst = []
    def __init__(self):
        self.inst = 0
        self.wwnlst = []  
        self.devlink = '' # '/dev/cfg/c'
        self.serial = ''
        self.vendor = ''
        self.prod = ''
        self.fw = ''
        self.pci_slot = ''
         
    def __init__(self,inst):
        self.inst = inst
        self.wwnlst = []  
        self.devlink = '' # '/dev/cfg/c'
        self.devpath = '' # '/dev/cfg/c'
        self.serial = ''
        self.vendor = ''
        self.model = ''
        self.prod = ''
        self.fw = ''
        self.pci_slot = ''
        self.devlink = '/dev/cfg/c'
        self.blksize = 512
        self.nWWN = ''
        self.pWWN = ''
        self.connecttype = ''

    def addDevId(self, id):
        self.devid = id
    def getDevId(self):
        return self.devid
    def addSerno(self, no):
        self.serial = no
    def addVendor(self, name):
        self.vendor = name
    def addProd(self, name):
        self.prod = name
    def addLink(self, name):
        self.devlink = name
    def addPath(self, name):
        self.devpath = name
    def addBLKsize(self, size):
        self.blksize = size
    def addnWWN(self, wwn):
        self.nWWN = wwn
    def addpWWN(self, wwn):
        self.pWWN = wwn
    def addType(self, conntype):
        self.connecttype = conntype
        
            

    def printVal(self):
         if not HBA.headprinted and not printShort:
             print "%3s %3s %-16s %-48s %-16s %-16s %-12s %-8s %-8s %-8s %-8s" % ('id','PCI','devlink','devpath','port WWN','nodeWWM','Type','SN','Vendor','PROD','model')
             HBA.headprinted = True
         elif not HBA.headprinted and not printShort:
             print "devlink, LUN list"
         print "%3d" % self.inst,
         for pci in pcipaths[servertype]:
             if pci in self.devpath: 
                 print pcipaths[servertype].index(pci),
                 break
         try:
             print "%-16s" % self.devlink,
         except AttributeError:
             print "%-16s" % 'none',
         try:
             print '' if printShort else "%-50s" % self.devpath,
         except AttributeError:
             print "%-50s" % 'none',
         try:
             print "%-16s" % self.pWWN,
         except AttributeError:
             print "%-16s" % 'none',
         try:
             print "%-16s" % self.nWWN,
         except AttributeError:
             print "%-16s" % 'none',
         try:
             print '' if printShort else "%-6s" % self.connecttype,
         except AttributeError:
             print "%-6s" % 'none',
         try:
             print '' if printShort else "%-12s" % self.serial,
         except AttributeError:
             print "%-12s" % 'none',
         try:
             print '' if printShort else "%-8s" % self.vendor,
         except AttributeError:
             print "%-8s" % 'nonev',
         try:
             print '' if printShort else "%-8s" % self.prod,
         except AttributeError:
             print "%-8s" % 'nonep',
         try:
             print '' if printShort else "%-8s" % self.model,
         except AttributeError:
             print "%-8s" % 'nonem',
         print


def getDevNode(iter_lines,inst):
    hba = HBA(inst)
    allfound = False
    for line in iter_lines:
        if line.split('=')[0].strip() == "value":
            continue
        # print line
        # pdb.set_trace()
        if 'name=' in line:
            if line.split('=')[1].split()[0] == "'model'":
                hba.addProd(iter_lines.next().split('=')[1].strip().strip("'"))
                continue
            elif line.split('=')[1].split()[0] == "'max-xfer-size'":
                hba.addBLKsize(iter_lines.next().split('=')[1])
                continue
        elif 'Device Minor Nodes:' in line :
            for line in iter_lines:
                if line.split('=')[0].strip() == 'dev_path':
                    hba.addPath(line.split('=')[1].strip())
                    break
        elif 'fp, instance #' in line :
            for line in iter_lines:
                if line.split('=')[0].strip() == "value":
                    continue
                # if inst == 4: pdb.set_trace()
                if 'name=' in line:
                    if line.split('=')[1].split()[0] == "'initiator-node'":
                        hba.addnWWN(iter_lines.next().split('=')[1].strip().strip("'"))
                        continue
                    elif line.split('=')[1].split()[0] == "'initiator-port'":
                        hba.addpWWN(iter_lines.next().split('=')[1].strip().strip("'"))
                        continue
                    elif line.split('=')[1].split()[0] == "'initiator-interconnect-type'":
                        hba.addType(iter_lines.next().split('=')[1].strip().strip("'"))
                        continue
                elif 'Device Minor Nodes:' in line :
                    for line in iter_lines:
                        if line.split('=')[0].strip() == "dev_path" and 'nodetype=ddi_ctl:attachment_point:fc' in iter_lines.next():
                            hba.addLink(iter_lines.next().split('=')[1].strip())
                            allfound = True
                            break
                # pdb.set_trace()
                if allfound or match("(    ){1,5}\S+ (instance #\d+ )?\(driver name: \S+\)",line): 
                    hbalst.append(hba)
                    # print "return line: "+line
                    return line
                # else:
                #    print "line: "+line
                    
    print "unexpected return line: "+line
    return line


#          pdb.set_trace()

def openExplo(explorer):
    if os.path.isdir(explorer):
        fprtconf = open(os.path.join(explorer,explo_prtconf))
    elif os.path.isfile(explorer):
        import tarfile
        
        basetf = match("(.+).tar.*", os.path.basename(explorer)).groups()[0]
        tar = tarfile.open(explorer)
        fprtconf = tar.extractfile(os.path.join(basetf, explo_prtconf))
    else:
        print "file/directory %s not found" % explorer
        exit(1)
    return fprtconf

### MAIN PROGRAM ###
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--short", help="PCI Slot, print only device link and WWN", action="store_true")
    parser.add_argument("-f","--file", dest="filename", help="provide a 'prtconf -vD' file")
    parser.add_argument("-g","--explorer", dest="explorer", help="provide data in packed or unpacked explorer ")
    args = parser.parse_args()

    if args.explorer:
        if args.filename:
            print "WARNING: ignore %s because use explorer output" % args.filename
        fl = openExplo(args.explorer)
    else:
        if args.filename:
            fl = open(args.filename)
        else:
            fl = Popen(['/usr/sbin/prtconf','-Dv'],stdout=PIPE).stdout
        
    lines = fl.readlines()
    iter_lines = iter(lines)
    prevline, line = None, iter_lines.next()
    
    # pdb.set_trace()
    for line in iter_lines:
        if "(driver name: rootnex)" in line:
            servertype = line.split(' ')[0]
            print servertype
        lastline = line
        while 'SUNW,qlc, instance' in lastline or 'SUNW,emlxs, instance' in lastline:
            # print "begin line: "+lastline
            lastline = getDevNode(iter_lines,int(findall('#[0-9]*', lastline)[0].replace("#","")))

    # pdb.set_trace()
    for l in hbalst:
            l.printVal()
