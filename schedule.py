import os
import string
import random
import requests
import subprocess
from datetime import datetime
from azure.storage.blob import BlobClient, ContentSettings
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

from settings import logger

name = os.getenv("FRIENDLY_NAME")
blob_storage_dsn = os.getenv("BLOB_STORAGE_DSN")
teams_webhook = os.getenv("TEAMS_WEBHOOK")
schedule = os.getenv("SCHEDULE")
command = os.getenv("COMMAND")
alert_on_success = os.getenv("ALERT_ON_SUCCESS", True)
alert_on_failure = os.getenv("ALERT_ON_FAILURE", True)


def run_test():
    try:
        logger.debug(f"Starting automated test suite using command: {command}")
        process = subprocess.run(command.split(" "), timeout=7200, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired:
        logger.exception("Error in subprocess, skipping run")
        print("Timeout occurred, skipping run")
        return
    logger.debug(process.stdout.decode())
    print(process.stdout.decode())
    alert = False
    if process.returncode == 0:
        status = "Success"
        if alert_on_success:
            alert = True
    else:
        status = "Failure"
        if alert_on_failure:
            alert = True
    logger.debug("Uploading report.html to blob storage...")
    url = upload("report.html")

    if alert:
        post(teams_webhook, status, url)


def upload(filename):
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    blob = BlobClient.from_connection_string(
        conn_str=blob_storage_dsn,
        container_name="qareports",
        blob_name=f"pytest_report/{datetime.now().strftime('%Y%m%d-%H%M')}-{suffix}.html",
    )
    with open(filename, "rb") as f:
        blob.upload_blob(f, content_settings=ContentSettings(content_type="text/html"))
    logger.debug(f"Successfully uploaded report to blob storage: {blob.url}")
    return blob.url


def post(webhook, status, url):
    if status == "Success":
        themeColor = "00FF00"
    else:
        themeColor = "FF0000"
    template = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": themeColor,
        "summary": f"{name} Test Results",
        "Sections": [
            {
                "activityTitle": f"{name} Test Results",
                "facts": [
                    {"name": "Status", "value": status},
                    {"name": "URL", "value": f"[{url}]({url})"},
                ],
                "markdown": True,
            }
        ],
    }
    return requests.post(webhook, json=template)


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_test, trigger=CronTrigger.from_crontab(schedule))
    logger.debug(f"Scheduled automated test run using cron expression: {schedule}")
    scheduler.start()


if __name__ == "__main__":
    main()
