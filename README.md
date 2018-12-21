# saninfo
Solaris tool for show FC-SAN infos

```bash
$ saninfo.py
ORCL,SPARC-S7-2L
 id PCI devlink        devpath                                            port WWN         nodeWWM          Type         SN       PROD     model   
  0 1 /dev/cfg/c3      /pci@300/pci@1/pci@0/pci@11/SUNW,emlxs@0:devctl    10000011bf7c1ef6 20000011bf7c1ef6 FABRIC                       7101684          
  1 1 /dev/cfg/c4      /pci@300/pci@1/pci@0/pci@11/SUNW,emlxs@0,1:devctl  10000011bf7c1ef7 20000011bf7c1ef7 FABRIC                       7101684          
  4 5 /dev/cfg/c16     /pci@300/pci@2/pci@0/pci@15/SUNW,qlc@0:devctl      2100f5a764f864e0 2000f5a764f864e0 FABRIC                                        
  5 5 /dev/cfg/c17     /pci@300/pci@2/pci@0/pci@15/SUNW,qlc@0,1:devctl    2100f5a764f864e1 2000f5a764f864e1 FABRIC                                        
  6 2 /dev/cfg/c18     /pci@302/pci@1/pci@0/pci@12/SUNW,qlc@0:devctl      2100f5a764f86c60 2000f5a764f86c60 FABRIC                                        
  7 2 /dev/cfg/c19     /pci@302/pci@1/pci@0/pci@12/SUNW,qlc@0,1:devctl    2100f5a764f86c61 2000f5a764f86c61 FABRIC                                        
  2 6 /dev/cfg/c9      /pci@302/pci@2/pci@0/pci@16/SUNW,emlxs@0:devctl    10000011bf7c2047 20000011bf7c2047 FABRIC                       7101684          
  3 6 /dev/cfg/c11     /pci@302/pci@2/pci@0/pci@16/SUNW,emlxs@0,1:devctl  10000011bf7c2048 20000011bf7c2048 FABRIC                       7101684          
```


```bash
usage: saninfo.py [-h] [-s] [-f FILENAME] [-g EXPLORER]

optional arguments:
  -h, --help            show this help message and exit
  -s, --short           PCI Slot, print only device link and WWN
  -f FILENAME, --file FILENAME
                        provide a 'prtconf -vD' file
  -g EXPLORER, --explorer EXPLORER
                        provide data in packed or unpacked explorer
```
