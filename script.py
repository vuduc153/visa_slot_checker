from twocaptcha import TwoCaptcha
import requests
import base64
import os
from io import BytesIO
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender_email, sender_password, subject, message, recipients):

    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # Login to the SMTP server
        server.login(sender_email, sender_password)
        # Send the email
        server.sendmail(sender_email, recipients, msg.as_string())
        # Close the connection to the SMTP server
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Failed to send email:", str(e))


def get_available_date(start_date_str, end_date_str, excluded_dates):

    # Convert start and end dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    avail_date = []

    # Iterate over dates between start and end dates
    current_date = start_date
    while current_date <= end_date:
        # Check if the current date is not in the excluded dates list
        if current_date.strftime('%Y-%m-%d') not in excluded_dates:
            avail_date.append(current_date)
        # Move to the next date
        current_date += timedelta(days=1)
    
    # If no valid date found, return None
    return avail_date


def get_interval(app_id):

    interval_endpoint = "https://api.consulat.gouv.fr/api/team/621540d353069dec25bd0045/reservations/get-interval?serviceId=624317926863643fe83c8548"

    # Add headers for request authentication
    headers = {'x-gouv-web': 'fr.gouv.consulat', 'x-gouv-app-id': app_id, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(interval_endpoint, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        print("Interval request failed.")


def get_excluded_days(app_id):

    excluded_day_endpoint = "https://api.consulat.gouv.fr/api/team/621540d353069dec25bd0045/reservations/exclude-days"

    # Add headers for request authentication
    headers = {'x-gouv-web': 'fr.gouv.consulat', 'x-gouv-app-id': app_id, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    body = {
        "session": {
            "624317926863643fe83c8548": True
        }
    }
    response = requests.post(excluded_day_endpoint, headers=headers, json=body)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        print("Excluded days request failed.")


def get_app_id():

    starting_page_url = "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas"
    
    # Add headers for request authentication
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(starting_page_url, headers=headers)

    # Get the app id from the documen
    pattern = r'"x-gouv-app-id":"([^"]+)"'
    match = re.search(pattern, response.text)

    if match:
        return f'fr.gouv$+{match.group(1)}-meae-ttc'


def get_captcha():

    starting_page_url = "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas"
    # Add headers for request authentication
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(starting_page_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the element with id "captcha-image"
        captcha = soup.find(id="captcha-image")
        
        if captcha:
            svg_b64 = captcha.get("src").split(",", maxsplit=1)[1]
            # Convert to bytes type
            return svg_b64.encode("ascii")
        else:
            print("Captcha image not found.")
    else:
        print("Failed to retrieve the webpage.")

    return ""
    


def convert_svg_to_jpg_base64(svg_base64):

    # Decode the Base64 SVG image to binary
    svg_data = base64.b64decode(svg_base64)

    # Convert SVG to PIL Image
    drawing = svg2rlg(BytesIO(svg_data))
    img_buffer = BytesIO()
    renderPM.drawToFile(drawing, img_buffer, fmt="JPG")
    img_buffer.seek(0)

    # Convert PIL Image to Base64 JPG
    with Image.open(img_buffer) as img:
        jpg_buffer = BytesIO()
        img.save(jpg_buffer, format="JPEG")
        jpg_buffer.seek(0)
        jpg_base64 = base64.b64encode(jpg_buffer.getvalue()).decode()

    return jpg_base64


if __name__ == '__main__':

    while True:

        log_file = 'logfile.txt'

        app_id = get_app_id()
        interval = get_interval(app_id)
        excluded = get_excluded_days(app_id)
        start_date, end_date = interval["start"], interval["end"]

        # Get email credentials from env variables
        sender_email = os.environ['SENDER_EMAIL']
        sender_password = os.environ['SENDER_PASSWORD']
        subject = '[NOTIFICATION] Visa'
        recipients = os.environ['MAILING_LIST'].split(";")

        avail_date = get_available_date(start_date, end_date, excluded)
        avail_str = f"Available date: {avail_date}"

        if avail_date:
            print(avail_date)
            # Notification logic
            send_email(sender_email, sender_password, subject, avail_str, recipients)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a') as file:
            file.write(current_time + '\n')
            file.write(avail_str + '\n')

        time.sleep(180)