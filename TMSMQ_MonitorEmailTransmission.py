import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import PASSWORD, SMTP_HOST,PORT,FROM_EMAIL_USER,TO_EMAIL_USER,ALERT_MESSAGE,SUMMARY_MESSAGE
import logging
from datetime import time


  

class EmailHandler():

    def CreateEmail(message_type, time, info ='default'):

        #Instantiate email object
        email = MIMEMultipart()

        #Format messages depending on function input template
        if message_type == ALERT_MESSAGE:
            message = message_type.format(time)
            logging.info(message)
        elif message_type == SUMMARY_MESSAGE:
            message = message_type.format(time, info)
            logging.info(message)

        #Assign email header info
        email['FROM'] = FROM_EMAIL_USER
        email['TO'] = TO_EMAIL_USER
        email['Subject']="TMS transmission to MQ error"

        #Attach message to email
        email.attach(MIMEText(message, 'plain'))

        logging.info("{} E-mail Created".format(message_type))

        return email

    def SendEmail(email):

       #Connect to SMPT SERVER
        try:
            smtp_connection = smtplib.SMTP(host=SMTP_HOST, port=PORT)
            print("Connected to SMTP SERVER")
        except: 
            logging.error("Couldn't connect to the SMTP Server")
            print("Couldn't connect to the SMTP Server")
            exit()

        #Establishing TLS protocol.
        try:
            smtp_connection.starttls()
            print("Established TLS connection")
        except: 
            logging.error("Couldn't establish a TLS protocol exchange with SMTP Server")
            print("Couldn't establish a TLS protocol exchange with SMTP Server")
            exit()
        #Login to smtp server (needed for test with outlook)
        #s.login(FROM_EMAIL_USER,PASSWORD)

        try:
            #send the message on connection 
            smtp_connection.send_message(email)
            logging.info("Email Sent to {}".format(TO_EMAIL_USER))
        except:
            logging.error("Couldn't send the e-mail to {}.".format(TO_EMAIL_USER))

        del email

        #Terminate the SMTP session and close the connection
        smtp_connection.quit()
        logging.debug("SMTP Connection Terminated")