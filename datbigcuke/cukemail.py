import smtplib
import ConfigParser

class CukeMail():
    section = 'Mail'
    parser = None
    smtp_server = None
    logged_in = False

    subject = ''
    message = ''

    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read('./config/app.conf')

        self.smtp_server = smtplib.SMTP(self.parser.get(self.section, 'smtp_server'))
    
        if(self.smtp_server.ehlo()[0] != 250):
            return

        if(self.smtp_server.starttls()[0] != 220):
            return

        if(self.smtp_server.login('bigdatacuke@gmail.com', 'cKgYm0R4')[0] != 235):
            return

        self.logged_in = True

    def subject(self, subj):
        self.subject = subj

    def message(self, mess):
        self.message = mess

    def send(self, address):
        if self.logged_in:
            message = "subject: " + self.subject + "\n"
            message = message + "from: " + self.parser.get(self.section, 'address') + "\n"
            message = message + "To: " + address + "\n\n"
            message = message + self.message
            self.smtp_server.sendmail(self.parser.get(self.section, 'address'), address, message)

    def send_verification(self, unique, email):
        self.subject("Verify your email")
        self.message("Please follow this link to verify your email address:\n" + self.parser.get('General', 'site_host') + "/verify/" + unique)
        self.send(email)
