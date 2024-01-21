import datetime
import os
import os.path
import smtplib
import uuid
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from django.template.loader import get_template, render_to_string
from dotenv import load_dotenv
import pdfkit

if not os.getenv("PYTHONANYWHERE_SITE"):
    load_dotenv()
else:
    project_folder = os.path.expanduser('~/adventora')
    print("PROJECT FOLDER: " + project_folder)
    load_dotenv(os.path.join(project_folder, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent


def sendreservationsuccess(email, name, checkin, checkout, people, nights, total, reservation, hotel, room):
    email_address = "no-reply@adventora.net"
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Successful reservation | Успешна резервация'
    msg['From'] = formataddr(('Adventora', email_address))
    msg['To'] = formataddr((name, email))
    msg["Message-ID"] = uuid.uuid4().__str__()
    msg["MIME-Version"] = "1.0"
    msg["Reply-To"] = 'deyannikolov@adventora.net'
    msg["Return-Path"] = 'deyannikolov@adventora.net'
    msg["X-Priority"] = "Normal"
    msg["X-Mailer"] = "Adventora Email System v1.1"
    msg["Auto-Submitted"] = "auto-generated"
    msg["X-Auto-Response-Suppress"] = "All"
    msg["X-Report-Abuse"] = "Please report abuse here: https://adventora.net/contact"
    msg["X-Annoying-Newsletter"] = "We are sorry if you received this email by mistake. Please report abuse here: https://adventora.net/contact"
    msg["X-AntiVirus"] = "Scanned by Adventora Email System"
    msg["X-AntiSpam"] = "Spam is not tolerated by Adventora Email System"
    msg["X-Email-ID"] = uuid.uuid4().__str__()
    msg["X-Email-Category"] = "Welcome Email"
    msg["X-Email-Category-Id"] = "1"

    # format: January 6th, 2024
    date_today = datetime.datetime.now().strftime("%B %d, %Y")

    # get the html template, and use it as email
    template = get_template('email/reservation-success.html')
    html = template.render(
        {'name': name, 'checkin': checkin, 'checkout': checkout, 'people': people, 'nights': nights, 'total': total, 'reservation': reservation, 'hotel': hotel, 'room': room, 'datetoday': date_today}
        )
    html_string = render_to_string('email/reservation-success.html', {'name': name, 'checkin': checkin, 'checkout': checkout, 'people': people, 'nights': nights, 'total': total, 'reservation': reservation, 'hotel': hotel, 'room': room, 'datetoday': date_today})
    msg.add_alternative(html, subtype='html')

    with open(f'{BASE_DIR}/invoices/reservation-{reservation.id}.html', 'w+', encoding='utf-8') as f:
        f.write(str(html_string))
    # save to .html file





    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
