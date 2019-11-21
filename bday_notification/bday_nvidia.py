#!/home/utils/Python-3.6.1/bin/python3.6

import datetime
import email
import json
import os
import random
import smtplib

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from jinja2 import Environment, FileSystemLoader


def Rand_Image():
    image_list = os.listdir("/home/scratch.yogeshg_mis/project/dev/bday_notification/static/")
    rand_image = random.choice(image_list)
    image = os.path.join(str("/home/scratch.yogeshg_mis/project/dev/bday_notification/static/"), str(rand_image))
    return image
#Rand_Image()

def Template_Loader():
    template_loader = FileSystemLoader(searchpath = "/home/scratch.yogeshg_mis/project/dev/bday_notification/")
    template_env = Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    return template
#Template_Loader()

def Send_Mail(emp_name, emp_email, message):
    image = Rand_Image()
    template = Template_Loader()
    msg = MIMEMultipart('alternative')
    msg['From'] = 'IT India'
    msg['To'] = emp_email
    msg['Cc'] = 'manjustaff@exchange.nvidia.com'
    msg['Subject'] = "Happy Birthday...!!!"
    msg.add_header('Content-Type', 'text/html')
    fp = open(image, 'rb')
    msg_image = MIMEImage(fp.read(), name = image)
    msg_image.add_header('Content-ID', '<image1>')
    msg_image.add_header("Content-Disposition", "in-line", filename=image)
    msg_image.add_header('X-Attachment-Id', str('image1'))
    msg.attach(msg_image)
    recipient = [msg['To'] , msg['Cc']]
    msg.attach(MIMEText(template.render(name = emp_name, message = message, cid = str('image1')), "html"))
    try:
        smtp_obj = smtplib.SMTP('smtp.nvidia.com')
        smtp_obj.sendmail('yogeshg@nvidia.com', recipient, msg.as_string())
    except smtplib.SMTPException:
        print ("something went wrong")
#Send_Mail()

def Read_File():
    emp_data = '/home/scratch.yogeshg_mis/project/dev/bday_notification/emp_dob.json'
    message_data = '/home/scratch.yogeshg_mis/project/dev/bday_notification/message.json'
    with open (emp_data) as file:
        emp_dict = json.loads(file.read())
    with open (message_data) as file:
        message_dict = json.loads(file.read())
    return emp_dict, message_dict
#Read_File()

def DOB_Emp(emp_data, message_data):
    current_date = datetime.datetime.now().strftime("%d-%B")
    for emp in emp_data:
        for msg_data in message_data:
            msg = random.choice(msg_data['message'])
            if current_date == str(emp['dob']):
                emp_name = emp['emp_name']
                emp_email = emp['email_id']
                Send_Mail (str(emp_name), str(emp_email), str(msg))
#DOB_Emp()

def main():
    emp_data, message_data = Read_File()
    DOB_Emp(emp_data, message_data)

if __name__ == '__main__':
    main()
