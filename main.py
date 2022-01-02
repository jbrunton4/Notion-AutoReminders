# import HTTP request modules for querying notion
import requests, json

# import SMTP related libraries for email notifications
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import datetime, time


# define a function to log important information
def log(message: str) -> None:
    with open("log.log", "a") as fh:
        log_str = f"{datetime.datetime.now()} | {message}"
        print(log_str)
        fh.write(f"{log_str}\n")


# Get important data from the config file
with open("config.json", "r") as fh:
    config_data = json.load(fh)

    DATABASE_ID = config_data["database_id"]
    TOKEN = config_data["notion_token"]
    DATE_PROPERTY_NAME = config_data["date_property_name"]
    EMAIL_SENDER = config_data["email_addr"]
    EMAIL_PASSWORD = config_data["email_password"]
    YOUR_EMAIL = config_data["your_email"]
    INTERVALS = config_data["reminder_intervals"]
log("Retrieved data from config.json")

# create the headers from the token
HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Notion-Version": "2021-05-13"
}
log("Configured headers")


def send_email(recipient: str, subject: str, content: str, mode: str = "plain") -> None:
    """
    Send an email using SMTP
    :param recipient: The e-mail address of the recipient
    :param subject: The subject line of the email
    :param content: The body of the email
    :param mode: "plain" for plain text, "html" for HTML formatted text
    :return: None
    """

    # declare some default information
    port = 465

    # format message as a MIME multipart
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = recipient
    plain_text = MIMEText(content, mode)
    message.attach(plain_text)
    object_to_send = message.as_string()

    # create the SSL context
    context = ssl.create_default_context()

    # with the context as the server, log in and send
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, object_to_send)
        log("Sent email reminder")

HTML_REMINDER = """
<html>
  <head>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

      * {
        font-family: 'Roboto', sans-serif;
      }

      .middle {
        background: #BEBEBE;
        width: 50%;
        max-width: 500px;
        height: 50%;
        border-radius: 12px;
        padding: 20px;

        /* DIV centering */
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
      }

      .middle #notion-logo {
        width: 30%;

        /* IMG centering */
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 40%;
      }

      .middle h1, .middle h6 {
        text-align: center;
      }

      .middle h1 #link-btn {
        background-color: #e16259;
        border: none;
        border-radius: 4px;
        color: #fff;
        font-size: 20px;
        padding: 1%;
        text-decoration: none;
      }
      .middle h1 #link-btn:hover {
        background-color: #cf534a;
      }
    </style>
  </head>
  <body>
    <div class="middle">
      <img id="notion-logo" src="https://cdn.icon-icons.com/icons2/2429/PNG/512/notion_logo_icon_147257.png" />

      <h1><b>Your Notion Reminder</b></h1>

      <br />
      You set up a reminder to study <a href="pageUrlGoesHere">pageNameGoesHere</a>
      today. Open notion and study now!

      <br />
      <h1><a id="link-btn" href="pageUrlGoesHere">Study Now!</button></h1>

      <h6>This service is not affiliated with Notion.

    </div>
  </body>
</html>

"""


def read_database(database_id: str, headers: dict) -> requests.Response:
    """
    Read a notion database by requesting it from the notion API.
    :param database_id: The UUID of the database to fetch
    :param headers: The headers for the HTTP request
    :return: The response
    """
    # declare the database URL to read from
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

    # send the POST request
    log("Making a POST request for the database")
    res = requests.request("POST", read_url, headers=headers)

    # display the primary keys of the data
    data = res.json()
    for entry in data["results"]:
        name = (entry["properties"]["Name"]["title"][0]["text"]["content"])
        date = (entry["properties"][DATE_PROPERTY_NAME]["date"]["start"])

        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])

        date_object = datetime.date(year, month, day)

        deltas = []
        for i in INTERVALS:
            deltas.append(datetime.timedelta(i))

        for delta in deltas:
            reminder_date = date_object + delta
            if datetime.date.today() == reminder_date:
                log("Reminder due today")
                if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 0:  # if it's 9 AM on reminder
                    log("Reminder due now")
                    page_url = f"https://www.notion.so/{entry['id'].replace('-', '')}"
                    outgoing_html = HTML_REMINDER.replace("pageNameGoesHere", name)\
                        .replace("pageUrlGoesHere", page_url)
                    send_email(
                        YOUR_EMAIL,
                        f"It's time to study {name}",
                        outgoing_html,
                        "html"
                    )

    # return the response object including the data
    log("POST request complete")
    return res


def main():
    log("Running main")

    while True:
        read_database(DATABASE_ID, HEADERS)
        time.sleep(60)


if __name__ == "__main__":
    main()
