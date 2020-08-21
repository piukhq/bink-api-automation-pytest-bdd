import os
import datetime
import subprocess
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

env = os.getenv("ENV", "dev")

env_config = {
    "dev": {
        "confluence": "1456865503",
        "command": ["pytest", "--md", "report.md", "-m", "dev", "--channel", "barclays"],
        "cron": "0 2 * * *",
    },
    "staging": {
        "confluence": "1456701609",
        "command": ["pytest", "--md", "report.md", "-m", "staging", "--env", "staging", "--channel", "barclays"],
        "cron": "0 2 * * *",
    },
    "preprod": {
        "confluence": "1456832788",
        "command": ["pytest", "--md", "report.md", "-m", "preprod", "--env", "preprod", "--channel", "barclays"],
        "cron": "*/10 * * * *",
    },
    "prod": {
        "confluence": "1456636188",
        "command": ["pytest", "--md", "report.md", "-m", "prod", "--env", "prod", "--channel", "barclays"],
        "cron": "*/10 * * * *",
    },
}


def run_basic_test():
    print('--------------')
    print(f"Executing Test for {env}")
    print('--------------')
    process = subprocess.run(
        env_config[env]["command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    print(process.stdout.decode())

    if os.path.exists("report.md"):
        print('--------------')
        print('Executing upload')
        print('--------------')
        with open("report.md", "r") as report_fp, open("report2.md", "w") as report2_fp:
            title = "API Test " + datetime.datetime.now().strftime("%d %b %Y")
            report2_fp.write(f'---\npage_title: "{title}"\n---\n')
            while (data := report_fp.read(4096)) != "":
                report2_fp.write(data)

        process = subprocess.run(
            (
                "/usr/local/bin/markdown2confluence",
                "--base-url",
                "https://hellobink.atlassian.net",
                "--default-space",
                "QA",
                "--default-ancestor",
                env_config[env]["confluence"],
                "--user",
                os.environ["CONFLUENCE_USER"],
                "--password",
                os.environ["CONFLUENCE_APITOKEN"],
                "report2.md",
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(process.stdout.decode())


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_basic_test, trigger=CronTrigger.from_crontab(env_config[env]["cron"]))
    scheduler.start()


if __name__ == "__main__":
    main()
