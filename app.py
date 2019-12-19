import csv, smtplib, ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer:

    def __init__(self,sender_email,password):
        print("You need to allow users to turn on access by less secure apps by this link https://myaccount.google.com/lesssecureapps")
        self.sender_email = sender_email
        self.password = password

    def send_mail(self,subject,body,cc,contacts_file,attachment_file):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["Subject"] = subject
        message['cc'] = cc
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        #get contacts list
        filename = attachment_file
        with open(filename, "rb") as attachment:
            # The content type "application/octet-stream" means that a MIME attachment is a binary file
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode to base64
            encoders.encode_base64(part)
            # Add header
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            # Add attachment to your message and convert it to string
            message.attach(part)
            text = message.as_string()
            
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                #read contact list and send mail
                with open(filename) as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    for Name,Course_Title,Batch,ID,Email,Marks in reader:
                        #print(Email)
                        server.sendmail(self.sender_email, Email,
                            text,)
                
            server.close()
            print('Email successfully sent')
        except Exception as error:
            print ('Something Wrong.Error:',error)

def main():
    sender_email = input("Enter Your Gmail Address ")
    password = input("Enter Your Password ")
    subject = "Python Marksheet"
    body = "মার্কস দেখে খুশি হওয়ার কিছু নাই, এটা ডেমো :-)"
    cc = "ryeasin03@gmail.com"
    contacts_file = "Marks_sheet.csv"
    attachment_file = "Marks_sheet.csv"
    mail = Mailer(sender_email,password)
    mail.send_mail(subject,body,cc,contacts_file,attachment_file)

if __name__ == "__main__":
    main()

    

