import smtplib 
from email.message import EmailMessage 

email_subject = "ALERTA: 293 AGENTES CON CAIDAS MAYOR AL 20 EN JUNIN SUR AL 7 DE OCTUBRE" 
sender_email_address = "ianclaro19@gmail.com"
receiver_email_address = "irumiche@globokas.com" 
email_smtp = "smtp.gmail.com" 
email_password = "CONTRA"


message = EmailMessage() 
message['Subject'] = email_subject 
message['From'] = sender_email_address 
message['To'] = receiver_email_address 

message.set_content("DATA", subtype='html')

server = smtplib.SMTP(email_smtp, '587')  
server.ehlo() 
server.starttls() 
server.login(sender_email_address, email_password) 
server.send_message(message) 
server.quit()