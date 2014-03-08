#!/usr/bin/perl
#The slution is in https://www.zabbix.com/forum/showthread.php?t=26756
#admin@itnihao.com modified it at 2013-01-30

$first = 1;

$dm_device = $ARGV[0];
$dm_info = $ARGV[1];

if (!$dm_device) {
$exec = "grep '\\b[a-z][a-z][a-z]\\b'  /proc/diskstats";
} else {
$exec = "grep \"\\b$dm_device\\b\" /proc/diskstats"
}

if (!$dm_info) {
print "{\n";
print "\t\"data\":[\n\n";

for (`$exec` ) {
( $major_number,
$minor_number,
$dm_name,
$reads_completed,
$reads_merged,
$reads_sectors,
$reads_time,
$writes_completed,
$writes_merged,
$writes_sectors,
$writes_time,
$io_queue,
$io_time,
$weighted_io_time
) = m/ +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)/;

print "\t\n" if not $first;
$first = 0;

print "\t\t{";
print " \"{#DISKNAME}\":\"$dm_name\"";
print "\t},";
}
print "\n\t]\n";
print "}\n";
} else {

for (`$exec` ) {
( $major_number,
$minor_number,
$dm_name,
$reads_completed,
$reads_merged,
$reads_sectors,
$reads_time,
$writes_completed,
$writes_merged,
$writes_sectors,
$writes_time,
$io_queue,
$io_time,
$weighted_io_time
) = m/ +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)/;

}
if ($dm_info eq "MAJOR") {print $major_number;}
elsif ($dm_info eq "MINOR") {print $minor_number;}
elsif ($dm_info eq "DISKNAME") {print $dm_name;}
elsif ($dm_info eq "READS_COMPLETED") {print $reads_completed;}
elsif ($dm_info eq "READS_MERGED") {print $reads_merged;}
elsif ($dm_info eq "READS_SECTORS") {print $reads_sectors;}
elsif ($dm_info eq "READS_TIME") {print $reads_time;}
elsif ($dm_info eq "WRITES_COMPLETED") {print $writes_completed;}
elsif ($dm_info eq "WRITES_MERGED") {print $writes_merged;}
elsif ($dm_info eq "WRITES_SECTORS") {print $writes_sectors;}
elsif ($dm_info eq "WRITES_TIME") {print $writes_time;}
elsif ($dm_info eq "IO_QUEUE") {print $io_queue;}
elsif ($dm_info eq "IO_TIME") {print $io_time;}
elsif ($dm_info eq "WIO_TIME") {print $weighted_io_time;}
else {print "ERROR: Chose one of the following info:\n MAJOR MINOR DISKNAME READS_COMPLETED READS_MERGED READS_SECTORS READS_TIME WRITES_COMPLETED WRITES_MERGED WRITES_SECTORS WRITES_TIME IO_QUEUE IO_TIME WIO_TIME\n";}
}

################################################
