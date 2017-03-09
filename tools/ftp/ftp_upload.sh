#! /usr/bin/env bash

ftp -n<<!
open 192.168.188.230
user test 123456
binary
cd /media1
prompt
put $1
close
bye
!
