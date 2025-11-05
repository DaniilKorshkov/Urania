import os
import time
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.header    import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

import JSONoperators
import JSONoperators as js
import subprocess
import ssl
import certifi


import requests
import json
import datetime
import pytz





def SendEmail(header, message_text):





    from_mail = js.ReadJSONConfig("email","from_mail")
    from_passwd = js.ReadJSONConfig("email","from_password")
    server_adr = js.ReadJSONConfig("email", "server_adr")
    user_list = js.ReadJSONConfig("email", "user_list")

    for to_mail in user_list:

        try:
            msg = MIMEMultipart()
            msg["From"] = from_mail
            msg['To'] = to_mail
            msg["Subject"] = Header(header, 'utf-8')
            msg["Date"] = formatdate(localtime=True)                  # Дата сообщения
            msg.attach(MIMEText(message_text, 'html', 'utf-8'))  # Добавляем форматированный текст сообщения

            '''
            # Добавляем файл
            filepath = "сертификат.pdf"                               # путь к файлу
            part = MIMEBase('application', "octet-stream")            # Создаем объект для загрузки файла
            part.set_payload(open(filepath,"rb").read())              # Подключаем файл
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename="{os.path.basename(filepath)}"')
            msg.attach(part)                                          # Добавляем файл в письмо
            '''

            '''ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=certifi.where())
            ssl_context.options |= ssl.OP_NO_TLSv1
            ssl_context.options |= ssl.OP_NO_TLSv1_1
    
            ssl_context.load_cert_chain(os.path.join(certsdir, 'certificate.pem'), os.path.join(certsdir, 'id_rsa'))
            ssl_context.load_dh_params(os.path.join(certsdir, 'dhparams.pem'))
    
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE'''





            smtp = smtplib.SMTP(f"smtp.{server_adr}", 587)
                           # Создаем объект для отправки сообщения
            smtp.ehlo()
            smtp.starttls()                                           # Открываем соединение
            smtp.ehlo()
            smtp.login(from_mail, from_passwd)                        # Логинимся в свой ящик
            smtp.sendmail(from_mail, to_mail, msg.as_string())        # Отправляем сообщения
            smtp.quit()                                               # Закрываем соединение

            '''# Сохраняем сообщение в исходящие
            imap = imaplib.IMAP4(f"imap.{server_adr}", 993)                     # Подключаемся в почтовому серверу
            imap.login(from_mail, from_passwd)                        # Логинимся в свой ящик
            imap.select('Sent')                                       # Переходим в папку Исходящие
            imap.append('Sent', None,                                 # Добавляем наше письмо в папку Исходящие
                        imaplib.Time2Internaldate(time.time()),
                        msg.as_bytes())'''
        except:
            pass



def NotifyAsRoot(message, image):





            display = str((subprocess.run(["ls", "/tmp/.X11-unix/"],capture_output=True)).stdout)
            display = display.strip('b')
            display = display.strip("'")
            display = f":{display[1]}"

            user =  str((subprocess.run(["who"],capture_output=True)).stdout)
            user = user.split()
            try:
                display_position = user.index(display)
                username = (user[(display_position-1)])[2:(len(user[(display_position-1)]))]
            except:
                username = (user[0])[2:(len(user[0]))]



            uid = (subprocess.run(["id", "-u", username],capture_output=True)).stdout.decode()
            uid = uid.strip('b')
            uid = uid.strip("'")
            uid = uid.strip("\n")

            try:
                ret = str((subprocess.run(["pwd"], capture_output=True)).stdout)

                ret = ret.strip("b")
                ret = ret.strip("'")
                ret = ret.strip("\\n")
            except:
                ret = "/home/coldlab/Desktop/Urania"



            os.system(f'sudo -u {username} DISPLAY={display} DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus notify-send -u critical -i {ret}/{image} "{message}"')





def NotifyUser(event_code, text, critical=False):
    email_crash = JSONoperators.ReadJSONConfig("email","email_notifications_for_crash")
    email_abnorm = JSONoperators.ReadJSONConfig("email", "email_notifications_for_abnorm")
    live_crash = JSONoperators.ReadJSONConfig("email", "live_notifications_for_crash")
    live_abnorm = JSONoperators.ReadJSONConfig("email", "live_notifications_for_abnorm")

    if critical:
        try:
            if email_crash == "True":
                SendEmail("Sampling system failure", text)
        except:
            pass

        try:
            if live_crash == "True":
                NotifyAsRoot(text, "ErrorIcon.png")
        except:
            pass



    else:
        try:
            if email_abnorm == "True":
                SendEmailDjango(str(event_code), text)
        except:
            pass

        try:
            if live_abnorm == "True":
                NotifyAsRoot(text, "AbnormalityIcon.png")
        except:
            pass



'''if __name__ == "__main__":
    NotifyUser("Test crash message",True)
    NotifyUser("Test abnorm message", False)'''





def SendEmailDjango(event_code = "0002", text = "Here is some data ...."):
    now = datetime.datetime.now(pytz.timezone('America/Denver')).isoformat()
    #now = datetime.datetime.now(pytz.timezone('America/Toronto')).isoformat()

    url = "https://apps1.physics.carleton.ca/alert/notification/email"  

    data = {
        "token": "kqvvLin-ykokvGLpISejkc3rlV7IETxR0JvEYM1PIIYNympl",
        "type": "0002",
        "time_detected": now,
        "data": "Here is some data ..... ",
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")



if __name__ == "__main__":
    SendEmailDjango()