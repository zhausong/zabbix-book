#!/bin/sh
#################################################################
#                 Zabbix trapper monitor
#####
# Version: 0.1 - 20011/08/09
# Author: Jean Baptiste Favre < jean-baptiste.favre@iscool-e.com>
#####
# Version: 0.2 - 20012/05/04
# Author: Charles-Christian Croix < karles@karlesnine.com >
#####
# Changelog:
# - v0.1: replace (ugly) vfs.fs.size & custom.vfs.dev.* metrics
#         from customs checks to zabbix trapper implementation
# - v0.2: add inode support
#         change ItemName to custom.ItemName
#         change /dev/sd* devise support to /dev/xvd* (ubuntu LTS 12.04) 
#################################################################
# vfs.fs.size metrics
df -Pk | awk ' /^\/dev\// { 
    print "- custom.vfs.fs.size[" $6 ",total] " $2
    print "- custom.vfs.fs.size[" $6 ",used] " $3
    print "- custom.vfs.fs.size[" $6 ",free] " $4
    print "- custom.vfs.fs.size[" $6 ",pfree] " 100 - $5
    print "- custom.vfs.fs.size[" $6 ",pused] " 0 + $5
}'
# vfs.fs.inode metrics
df -Pki | awk ' /^\/dev\// { 
    print "- custom.vfs.fs.inode[" $6 ",total] " $2
    print "- custom.vfs.fs.inode[" $6 ",used] " $3
    print "- custom.vfs.fs.inode[" $6 ",free] " $4
    print "- custom.vfs.fs.inode[" $6 ",pfree] " 100 - $5
    print "- custom.vfs.fs.inode[" $6 ",pused] " 0 + $5
}'
# custom.vfs.dev.
grep xvd /proc/diskstats | awk '{
    if ( $3=="xvda1" )
        disk = "xvda"
    else
        disk = $3
    print "- custom.vfs.dev.io.active["disk"] "$12
    print "- custom.vfs.dev.io.ms["disk"] "$13
    print "- custom.vfs.dev.read.ms["disk"] "$7
    print "- custom.vfs.dev.read.ops["disk"] "$4
    print "- custom.vfs.dev.read.sectors["disk"] "$6
    print "- custom.vfs.dev.write.ms["disk"] "$11
    print "- custom.vfs.dev.write.ops["disk"] "$8
    print "- custom.vfs.dev.write.sectors["disk"] "$10
}'
