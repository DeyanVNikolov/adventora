from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import uuid
from email.utils import formataddr
import os.path
from pathlib import Path
import os
import smtplib
import imghdr
from email.message import EmailMessage

from django.utils.translation import gettext as _

from dotenv import load_dotenv

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

    message_1 = _("Your reservation is successful.")
    message_2 = _("Your invoice is below.")
    message_3 = _("The invoice is also available in your dashboard.")
    message_4 = _("The invoice acts as ticket.")
    message_5 = _("Please show the invoice to the hotel staff upon arrival.")
    message_6 = _("Thank you for using Adventora.")

    # Add a plain text alternative
    msg.set_content(f'''
            {message_1}
            {message_2}
            {message_3}
            {message_4} {message_5}

            {message_6}
            
            # # # # #
            
            RESERVATION #{reservation.id}
            HOTEL - {hotel.name}
            ROOM #{room.number}
            CHECK-IN - {checkin.strftime("%d %B %Y")}
            CHECK-OUT - {checkout.strftime("%d %B %Y")}
            PEOPLE - {people}
            NIGHTS - {nights}
            
            TOTAL # {total} BGN
            
            # # # # #
        ''', subtype='plain', charset='utf-8'
                    )

    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
