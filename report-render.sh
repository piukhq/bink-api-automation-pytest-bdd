#!/bin/bash

bolb_name=$(date +%s | awk '{ print strftime("%Y%m%d-%H%M", $1);  }')-$(echo $RANDOM | md5sum | head -c 6).html
url="https://binkuksouthstaging.blob.core.windows.net/test/${bolb_name}"
webhook="https://hellobink.webhook.office.com/webhookb2/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/05a1d268dc4c44ee84b8765d9b6fa6fd/e69fd5a7-8b6c-4ac5-8df0-c88c77df0a12"

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
curl -H 'Content-Type: application/json' -d '{"@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "'"$themeColor"'", "summary": "Staging - Merchant API V1.2 Test Results", "Sections": [{"activityTitle": "Staging - Merchant API V1.2 Test Results", "facts": [{"name": "Status", "value": "'"$status"'"}, {"name": "URL", "value": "'"$url"'"}]}]}' $webhook