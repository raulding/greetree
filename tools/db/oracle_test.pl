#!/usr/bin/env perl

use DBI;

$ip = "192.168.1.1";
$port = 8787;
$service_name = "BIDW.com";
$user = "dingliang";
$pwd = "dingliang123";

$db = DBI->connect("dbi:Oracle://$ip:$port/$service_name", $user, $pwd) or die "Cannot connect db: $DBI::errstr\n";
print "I have connected to the Oracle database!\n";

$db->disconnect or warn "DB disconnect failed: $DBI::errstr\n";
print "Disconnected from Oracle databae!\n";


