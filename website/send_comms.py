from email.message import EmailMessage
import smtplib
import requests
import random


def send_mail(receiver, subject, content):
    email = EmailMessage()
    email['from'] = 'Smart Notes'
    email['to'] = receiver
    email['subject'] = subject
    email.set_content(content)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('abc@gmail.com', 'abc123')
        smtp.send_message(email)
        print('mail sent')


def send_sms(txt, num):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers={}".format(txt, str(num))
    headers = {
    'authorization': "abcdwdsd",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    print('sms sent')
    return requests.request("POST", url, data=payload, headers=headers).text




