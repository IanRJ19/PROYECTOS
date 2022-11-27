import smtplib, ssl
from decouple import config
class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "ianclaro19@gmail.com"
        self.password = config("EMAIL_IANTABLET_CONTRA")

    def send(self, emails, subjects, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for ubject in subjects:
            result = service.sendmail(self.sender_mail, emails, f"Subject: {ubject}\n{content}")

        service.quit()


if __name__ == '__main__':
    #mails = input("Enter emails: ").split()
    mails = "irumiche@globokas.com"
    subject = input("Enter subjects: ").split()
    content = "test"

    mail = Mail()
    mail.send(mails, subject, content)
