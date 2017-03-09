#! /usr/bin bash

bash ftp_upload.sh $1

#echo "http://192.168.188.230:22222/dispatch/add?id=${2}&path=media1/${1}&filename="
curl -q "http://192.168.188.230:22222/dispatch/add?id=${2}&path=${1}&filename="

while [ ! -f ${1}.ih ]
do
    bash ftp_download.sh ${1}.ih
    sleep 1
done

cat ${1}.ih
rm -rf ${1}.ih
