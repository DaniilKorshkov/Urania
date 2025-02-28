import json

import streamlit as st
import JSONoperators as js
import smtplib
from EmailNotificationSystem import NotifyUser


def EmailNotificationSettings():

    current_config = js.ReadJSONConfig("email")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ret = js.ReadJSONConfig("email","live_notifications_for_abnorm")
        st.write(f"On-screen notifications for abnorm: {ret}")

        enable_live_abnorm = st.button("Enable on-screen notifications for abnormal readings")
        disable_live_abnorm = st.button("Disable on-screen notifications for abnormal readings")

        if enable_live_abnorm:
            current_config["live_notifications_for_abnorm"] = "True"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email",dump_config)
        if disable_live_abnorm:
            current_config["live_notifications_for_abnorm"] = "False"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)


    with col2:
        ret = js.ReadJSONConfig("email","live_notifications_for_crash")
        st.write(f"On-screen notifications for crash: {ret}")

        enable_live_crash = st.button("Enable on-screen notifications for crash")
        disable_live_crash = st.button("Disable on-screen notifications for crash")

        if enable_live_crash:
            current_config["live_notifications_for_crash"] = "True"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)
        if disable_live_crash:
            current_config["live_notifications_for_crash"] = "False"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)


    with col3:
        ret = js.ReadJSONConfig("email","email_notifications_for_abnorm")
        st.write(f"Email notifications for abnorm: {ret}")

        enable_email_abnorm = st.button("Enable email notifications for abnormal readings")
        disable_email_abnorm = st.button("Disable email notifications for abnormal readings")

        if enable_email_abnorm:
            current_config["email_notifications_for_abnorm"] = "True"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)
        if disable_email_abnorm:
            current_config["email_notifications_for_abnorm"] = "False"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)


    with col4:
        ret = js.ReadJSONConfig("email","email_notifications_for_crash")
        st.write(f"Email notifications for abnorm: {ret}")

        enable_email_crash = st.button("Enable email notifications for crash")
        disable_email_crash = st.button("Disable email notifications for crash")

        if enable_email_crash:
            current_config["email_notifications_for_crash"] = "True"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)
        if disable_email_crash:
            current_config["email_notifications_for_crash"] = "False"
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)



    for i in range(6):
        st.markdown("")







    current_from_mail = current_config["from_mail"]
    st.write(f"Current email address: {current_from_mail}")
    new_from_mail = st.text_input("Enter email address of the sampling system")
    change_email = st.button("Change email")
    if change_email:
        if new_from_mail != None:
            current_config["from_mail"] = new_from_mail
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)



    new_password = st.text_input("Enter password for the email")
    change_password = st.button("Check password")

    server_adr = js.ReadJSONConfig("email","server_adr")

    if change_password:
        if new_password != None:

            try:
                smtp = smtplib.SMTP(f"smtp.{server_adr}", 587)
                # Создаем объект для отправки сообщения
                smtp.ehlo()
                smtp.starttls()  # Открываем соединение
                smtp.ehlo()
                smtp.login(current_config["from_mail"], new_password)  # Логинимся в свой ящик
                smtp.quit()

                current_config["from_password"] = new_password
                dump_config = json.dumps(current_config)
                js.EditJSONConfig("email", dump_config)


            except:
                st.write("Email/password/server configuration do not match")




    current_mail_server = current_config["server_adr"]
    st.write(f"Current email server: {current_mail_server}")
    new_mail_server = st.text_input("Enter email server address")
    change_server = st.button("Change email server")
    if change_server:
        if new_mail_server != None:
            current_config["server_adr"] = new_mail_server
            dump_config = json.dumps(current_config)
            js.EditJSONConfig("email", dump_config)






    for i in range(6):
        st.markdown("")


    st.write("Recipient list")
    recipient_list = current_config["user_list"]
    for recipient in recipient_list:
        col1, col2 = st.columns(2)
        with col1:
            st.write(recipient)
        with col2:
            delete_recipient = st.button(f"Remove {recipient} from mailing list")
            if delete_recipient:

                    new_config = current_config
                    new_config["user_list"] = current_config["user_list"].remove(recipient)

                    if new_config["user_list"] == None:
                        new_config["user_list"] = []

                    dump_config = json.dumps(new_config)
                    js.EditJSONConfig("email", dump_config)




    new_recipient = st.text_input("Enter new recipient address")
    add_recipient = st.button("Add new recipient")
    if add_recipient:
        if new_recipient != None:
            if not (new_recipient in current_config["user_list"]):
                new_config = current_config
                new_config["user_list"].append(new_recipient)
                dump_config = json.dumps(new_config)
                js.EditJSONConfig("email", dump_config)






    for i in range(12):
        st.markdown("")
    test_abnormal_message = st.button("Test abnormality notification system")
    test_crash_message = st.button("Test crash notification system")

    if test_abnormal_message:
        NotifyUser("Drill abnormality message",False)

    if test_crash_message:
        NotifyUser("Drill crash message",True)














EmailNotificationSettings()