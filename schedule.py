import os
import string
import random
import requests
import subprocess
from datetime import datetime
from azure.storage.blob import BlobClient, ContentSettings
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

env = os.getenv("ENV", "dev")
mode = os.getenv("MODE", "daily")
blob_storage_dsn = os.getenv("BLOB_STORAGE_DSN")

teams_webhook_qa = "https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/5d25733db5994811b6ee4049ef74713e/48aca6b1-4d56-4a15-bc92-8aa9d97300df"  # noqa
teams_webhook_alerts_qa = "https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/0856493823a1484b9adfa37c942d2da4/48aca6b1-4d56-4a15-bc92-8aa9d97300df"  # noqa
teams_webhook_alerts_production = "https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/7ae4116d366e4e5a92a65d9135a0664d/48aca6b1-4d56-4a15-bc92-8aa9d97300df"  # noqa

config = {
    "dev": {
        "command": [
            "pytest",
            "--html",
            "report.html",
            "--self-contained-html",
            "-s",
            "-m",
            "dev",
            "--channel",
            "barclays",
        ],
        "daily": {"cron": "5 22 * * *"},
    },
    "staging": {
        "command": [
            "pytest",
            "--html",
            "report.html",
            "--self-contained-html",
            "-s",
            "-m",
            "staging",
            "--env",
            "staging",
            "--channel",
            "barclays",
        ],
        "daily": {"cron": "5 22 * * *"},
    },
    "preprod": {
        "command": [
            "pytest",
            "--html",
            "report.html",
            "--self-contained-html",
            "-m",
            "preprod",
            "--env",
            "preprod",
            "--channel",
            "barclays",
        ],
        "daily": {"cron": "5 22 * * *"},
        "continuous": {"cron": "0 * * * *"},
    },
    "prod": {
        "command": [
            "pytest",
            "--html",
            "report.html",
            "--self-contained-html",
            "-m",
            "prod",
            "--env",
            "prod",
            "--channel",
            "barclays",
        ],
        "daily": {"cron": "5 22 * * *"},
        "continuous": {"cron": "0 * * * *"},
    },
}


def run_test():
    try:
        process = subprocess.run(config[env]["command"], timeout=540, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired:
        print('Timeout occured, skipping run')
        return
    print(process.stdout.decode())
    if process.returncode == 0:
        status = "Success"
    else:
        status = "Failure"
    url = upload("report.html")
    if env == "prod":
        if status == "Success":
            post(teams_webhook_alerts_qa, status, url)
        if status == "Failure":
            post(teams_webhook_alerts_production, status, url)
            post(teams_webhook_alerts_qa, status, url)
    else:
        post(teams_webhook_qa, status, url)


def upload(filename):
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    blob = BlobClient.from_connection_string(
        conn_str=blob_storage_dsn,
        container_name="qareports",
        blob_name=f"{datetime.now().strftime('%Y%m%d-%H%M')}-{suffix}.html",
    )
    with open(filename, "rb") as f:
        blob.upload_blob(f, content_settings=ContentSettings(content_type="text/html"))
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
        "summary": f"{mode.title()} Test Results",
        "Sections": [
            {
                "activityTitle": f"{mode.title()} Test Results",
                "facts": [
                    {"name": "Environment", "value": env},
                    {"name": "Mode", "value": mode},
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
    scheduler.add_job(run_test, trigger=CronTrigger.from_crontab(config[env][mode]["cron"]))
    scheduler.start()


if __name__ == "__main__":
    main()
