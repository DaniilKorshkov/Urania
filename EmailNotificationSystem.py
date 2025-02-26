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




def SendEmail(header, message_text):





    from_mail = js.ReadJSONConfig("email","from_mail")
    from_passwd = js.ReadJSONConfig("email","from_password")
    server_adr = js.ReadJSONConfig("email", "server_adr")
    user_list = js.ReadJSONConfig("email", "user_list")

    for to_mail in user_list:

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

        smtp = smtplib.SMTP(server_adr, 25)                       # Создаем объект для отправки сообщения
        smtp.starttls()                                           # Открываем соединение
        smtp.ehlo()
        smtp.login(from_mail, from_passwd)                        # Логинимся в свой ящик
        smtp.sendmail(from_mail, to_mail, msg.as_string())        # Отправляем сообщения
        smtp.quit()                                               # Закрываем соединение

        # Сохраняем сообщение в исходящие
        imap = imaplib.IMAP4(server_adr, 143)                     # Подключаемся в почтовому серверу
        imap.login(from_mail, from_passwd)                        # Логинимся в свой ящик
        imap.select('Sent')                                       # Переходим в папку Исходящие
        imap.append('Sent', None,                                 # Добавляем наше письмо в папку Исходящие
                    imaplib.Time2Internaldate(time.time()),
                    msg.as_bytes())



def NotifyAsRoot(message, image):

    DoNotify = JSONoperators.ReadJSONConfig("email","live_notifications")
    if DoNotify == "True":

        display = str((subprocess.run(["ls", "/tmp/.X11-unix/"],capture_output=True)).stdout)
        display = display.strip('b')
        display = display.strip("'")
        display = f":{display[1]}"

        user =  str((subprocess.run(["who"],capture_output=True)).stdout)
        user = user.split()
        display_position = user.index(display)
        username = user[(display_position-1)].strip("b'")



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


NotifyAsRoot("test","AbnormalityIcon.png")