"""Module used for sending big cuke emails"""

import smtplib
import ConfigParser
import threading
import thread

class CukeMail():
    section = 'Mail'
    parser = None
    smtp_server = None
    logged_in = None

    subject = ''
    message = ''

    def __init__(self):
        self.logged_in = threading.Event()
        self.logged_in.clear()
        thread.start_new_thread(self.setup_self, ())

    def setup_self(self):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read('./config/app.conf')

        self.smtp_server = smtplib.SMTP(self.parser.get(self.section, 'smtp_server'))

        if(self.smtp_server.ehlo()[0] != 250):
            return

        if(self.smtp_server.starttls()[0] != 220):
            return

        if(self.smtp_server.login(self.parser.get(self.section, 'address'), self.parser.get(self.section, 'password'))[0] != 235):
            return

        self.logged_in.set()


    ## Set the subject for a message
    def subject(self, subj):
        self.subject = subj

    ## Set the message content for a message
    def message(self, mess):
        self.message = mess

    ## Send the message to an email address
    def send(self, address):
        thread.start_new_thread(self.do_send, (address,))

    def do_send(self, address):
        self.logged_in.wait()
        message = "subject: " + self.subject + "\n"
        message = message + "from: " + self.parser.get(self.section, 'address') + "\n"
        print "Sending to: "
        if type(address) == list:
            message = message + "To: "
            for addr in address:
                print addr
                message = message + addr + "; "
            message = message + "\n\n"
        else:
            message = message + "To: " + address + "\n\n"
        message = message + self.message
        self.smtp_server.sendmail(self.parser.get(self.section, 'address'), address, message)

    ## Setup and send a verification email
    def send_verification(self, unique, email):
        self.logged_in.wait()
        self.subject("Verify your email")
        self.message("Please follow this link to verify your email address:\n" + self.parser.get('General', 'site_host') + "/verify/" + unique)
        self.send(email)
