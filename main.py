import imaplib
from dotenv import load_dotenv
import os

load_dotenv()

#imap sv
imap_server = 'imap.gmail.com'

#login credentials
username = os.getenv('smtp_username')
password = os.getenv('smtp_password')

print(f"Username: {username}")
print(f"Password: {password}")

mail = imaplib.IMAP4_SSL(imap_server, 993)
mail.login(username, password)

#load emails
for i in mail.list()[1]:
    l = i.decode().split(' "/" ')
    print(f'{l[0]} = {l[1]}')

#select de main view
mail.select('"INBOX"')

#look for all UNSEEN emails
status, messages = mail.search(None, 'UNSEEN')

print(messages)
print(status)