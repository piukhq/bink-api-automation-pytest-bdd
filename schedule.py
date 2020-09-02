import os
import requests
import subprocess
from datetime import datetime
from azure.storage.blob import BlobClient, ContentSettings
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

env = os.getenv("ENV", "dev")
blob_storage_dsn = os.getenv("BLOB_STORAGE_DSN")
teams_webhook_url = os.getenv(
    "TEAMS_WEBHOOK_URL",
    "https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/5d25733db5994811b6ee4049ef74713e/48aca6b1-4d56-4a15-bc92-8aa9d97300df",# noqa
)

env_config = {
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
            "barclays"
        ],
        "cron": "0 2 * * *",
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
        "cron": "0 2 * * *",
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
        "cron": "*/10 * * * *",
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
        "cron": "*/10 * * * *",
    },
}


def run_test():
    process = subprocess.run(env_config[env]["command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(process.stdout.decode())
    if process.returncode == 0:
        status = "Success"
    else:
        status = "Failure"
    url = upload("report.html")
    post(status, url)


def upload(filename):
    blob = BlobClient.from_connection_string(
        conn_str=blob_storage_dsn,
        container_name="qareports",
        blob_name=f"{datetime.now().strftime('%Y%m%d-%H%M')}.html",
    )
    with open(filename, "rb") as f:
        blob.upload_blob(f, content_settings=ContentSettings(content_type="text/html"))
    return blob.url


def post(status, url):
    if status == "Success":
        themeColor = "00FF00"
    else:
        themeColor = "FF0000"
    template = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": themeColor,
        "summary": "Nightly Test Results",
        "Sections": [
            {
                "activityTitle": "Nightly Test Results",
                "facts": [
                    {"name": "Environment", "value": env},
                    {"name": "Status", "value": status},
                    {"name": "URL", "value": f"[{url}]({url})"},
                ],
                "markdown": True,
            }
        ],
    }
    return requests.post(teams_webhook_url, json=template)


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_test, trigger=CronTrigger.from_crontab(env_config[env]["cron"]))
    scheduler.start()


if __name__ == "__main__":
    main()
