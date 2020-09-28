import time

import schedule
from dashboard_exporter import exporter

from config import config
from gmail import get_service, create_message_with_attachment, send_email


def job():
    print("Exporting New Relic dashboard...")
    dashboard = exporter(
        guid=config["dashboard"]["guid"],
        file_type=config["dashboard"]["file_type"],
        width=int(config["dashboard"]["width"]),
        height=int(config["dashboard"]["height"]),
    )

    print("Authenticating with Google...")
    service = get_service()

    for email in config["email"]["to"]:
        print("Creating message...")
        message = create_message_with_attachment(
            sender=config["email"]["sender"],
            to=email,
            subject=config["email"]["subject"],
            message_text=config["email"]["text"],
            file=dashboard,
        )

        print("Sending email...")
        send_email(message=message, user_id="me", session=service)

    print("Done!")


if __name__ == "__main__":
    # Run the initial job to authenticate with Google.
    job()

    # By default the job will run ever Friday.
    # Refer to the Schedule project documentation to configure the scheduler: https://pypi.org/project/schedule/
    schedule.every().friday.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
