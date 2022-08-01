#!/bin/bash

bolb_name=$(date +%s | awk '{ print strftime("%Y%m%d-%H%M", $1);  }')-$(echo $RANDOM | md5sum | head -c 6).html
url="https://binkuksouthstaging.blob.core.windows.net/test/${bolb_name}"

# look for report.html generated during pytest run
while [ ! -f /tmp/report.html ]; do
    sleep 2
done
sleep 2

# copy report to azureblob
az storage blob upload --account-name $(echo $BLOB_STORAGE_DSN | awk -F ';' '{print $2}' | sed 's/AccountName=//g') --container-name test --name $bolb_name --file /tmp/report.html --account-key $(echo $BLOB_STORAGE_DSN | awk -F ';' '{print $3}' | sed 's/AccountKey=//g') --auth-mode key

# determine what message to POST to teams using the error.log
if [ -s /tmp/error.txt ]; then
    echo "file not empty -> error -> red"
    themeColor="FF0000"
    status="FAILURE"
else
    echo "file is empty -> no errors -> green"
    themeColor="00FF00"
    status="SUCCESS"
fi

# POST to teams the output of pytest run
curl -H 'Content-Type: application/json' -d '{"@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "'"$themeColor"'", "summary": "Staging - Merchant API V1.2 Test Results", "Sections": [{"activityTitle": "Staging - Merchant API V1.2 Test Results", "facts": [{"name": "Status", "value": "'"$status"'"}, {"name": "URL", "value": "'"$url"'"}]}]}' $TEAMS_WEBHOOK


curl  -XPOST localhost:4191/shutdown