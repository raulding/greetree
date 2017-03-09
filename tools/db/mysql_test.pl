#! /usr/bin/env perl

use DBI;

my $date = shift @ARGV;

my @ver = ("3.0.2.29", "3.0.1.30");
my @isp = (0, 1, 5);
my @prop_bi = ("play_buffering_time", "no_halt_rate", "ms_flux_rate", "client_comm_failrate", "fsp_js_failrate", "conn_tracker_failrate");
my @prop_labin = ("start_num");
my @prop_crash = ("crash_rate", "crash_kernel_ratio");

my $driver = "mysql";
my $database_bi = "kpi";
my $table_bi = "day_open_beta_stat";
my $host_bi = "192.168.1.1";
my $usr = "funclient";
my $pwd = "funclient";
my $dsn_bi = "DBI:$driver:database=$database_bi;host=$host_bi";

my $database_labin = "labin_analyser";
my $table_labin = "version_num_stat";
my $host_labin = "192.168.1.1";
my $dsn_labin = "DBI:$driver:database=$database_labin;host=$host_labin";

# query bi
my $dbh_bi = DBI->connect($dsn_bi, $usr, $pwd) or die $DBI::errstr;

foreach $v (@ver) {
	foreach $i (@isp) {
		my $sqr = $dbh_bi->prepare("SELECT * FROM $table_bi WHERE day=$date AND inet_ntoa(version_id)=\"$v\" AND isp_id=$i");
		$sqr->execute() or die $DBI::errstr;

		my @row = $sqr->fetchrow_array();
		#print "$v, $i, @row\n";
		
		if ($i == 0) {	
			foreach $p (@prop_bi) {
				$value{$v.$p} = ($row[3]/1000)."/".($row[4]/1000) if($p =~ /play_buffering_time/);
				$value{$v.$p} = $row[5]*100 if($p =~ /no_halt_rate/);
				$value{$v.$p} = $row[6]*100 if($p =~ /ms_flux_rate/);
				$value{$v.$p} = ($row[8]*100)."/".($row[9]*100) if($p =~ /client_comm_failrate/);
				$value{$v.$p} = ($row[10]*100)."/".($row[11]*100) if($p =~ /fsp_js_failrate/);
				$value{$v.$p} = $row[12]*100 if($p =~ /conn_tracker_failrate/);
			}
		}

		if ($i == 1) {
			$value{$v."ms_flux_rate"} .= "(".($row[6]*100)."/";
			$value{$v."conn_tracker_failrate"} .= "(".($row[12]*100)."/";
		}

		if ($i == 5) {
                        $value{$v."ms_flux_rate"} .= ($row[6]*100).")";
                        $value{$v."conn_tracker_failrate"} .= ($row[12]*100).")";
                }

		$sqr->finish();
	}
}

$dbh_bi->disconnect();

# query labin
my $dbh_labin = DBI->connect($dsn_labin, $usr, $pwd) or die $DBI::errstr;
foreach $v (@ver) {
	my $sqr = $dbh_labin->prepare("SELECT * FROM $table_labin WHERE client_version=\"$v\" AND data_date=$date");
	$sqr->execute() or die $DBI::errstr;

        my @row = $sqr->fetchrow_array();
	
	foreach $p (@prop_labin) {
		$value{$v.$p} = $row[1]."(".$row[2].")";
	}
	
	$record_num{$v} = $row[1];
	$mac_num{$v} = $row[2];
	
	$sqr->finish();
}

$dbh_labin->disconnect();

# crash ratio
my $crashfile = "crash_result/crash_result_".$date;
open FILE, "<$crashfile";
while(<FILE>) {
        chomp;
        my @element = split /\|/;

	my $need = False;
	my $key;
	foreach $v (@ver) {
		if($element[1] =~ /^$v/) {
			$need = True; 
			$key = $v; 
			last; 	
		}
	}
	
	if(($need == True) && defined($record_num{$key})) {
		#print "$need, $key\n";
        	foreach $p (@prop_crash) {
        		$value{$key.$p} = sprintf("%.3f", $element[2]*100/$record_num{$key})."(".sprintf("%.3f", $element[5]*100/$mac_num{$key}).")" if($p =~ /crash_rate/);
			$value{$key.$p} = $element[3]."(".$element[6].")" if($p =~ /crash_kernel_ratio/);
		}
	}
}
close FILE;

$outfile = "pc_qos_".$date.".csv";
open OUT, ">$outfile";
foreach $p (@prop_bi, @prop_crash, @prop_labin) {
	foreach $v (@ver) {
		if ($v eq $ver[$#ver]) {
			print OUT "$value{$v.$p}\n";
		}
		else {
			print OUT "$value{$v.$p},";
		}
	}
}


