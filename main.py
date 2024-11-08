import imaplib
from dotenv import load_dotenv
import os
import email
from email.header import decode_header

load_dotenv()

#imap sv
imap_server = 'imap.gmail.com'

#login credentials
username = os.getenv('smtp_username')
password = os.getenv('smtp_password')

mail = imaplib.IMAP4_SSL(imap_server, 993)
mail.login(username, password)

mail.select('"INBOX"')

status, messages = mail.search(None, 'ALL')

email_ids = messages[0].split()

for index, email_id in enumerate(email_ids):

    folder = None

    #get the content of the mail
    res, msg = mail.fetch(email_id, '(RFC822)')

    print(f'{index + 1} de {len(email_ids)}')

    for response_part in msg:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])

            sender = message.get("From")
            subject, encoding = decode_header(message.get("Subject"))[0]

            date = message.get("Date")

            if isinstance(subject, bytes):
                try:
                    subject = subject.decode(encoding if encoding and encoding.lower() != 'unknown-8bit' else 'utf-8')
                except UnicodeDecodeError:
                    subject = subject.decode('latin1')
            
            if 'password' in subject.lower():
                folder = 'Password'
            if 'reunion' in subject.lower():
                folder = 'Reuniones'
            elif 'factura' in subject.lower():
                folder = 'Factura'
            elif 'reclamo' in subject.lower():
                folder = 'Reclamos'
            elif 'LinkedIn' or 'linkedin' or 'work' or 'trabajo' in subject.lower():
                folder = 'Trabajo'
            
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))

                    if 'atachment' in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join('adjuntos', filename)
                            
                            with open(filepath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            print(f'adjunto guardado {filename}')
                            
                            if 'factura' in filename.lower():
                                print('subiendo archivo a drive')

                    elif content_type == 'text/plain' or content_type == 'text/html':
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except UnicodeDecodeError:
                            body = part.get_payload(decode=True).decode('latin1', errors='ignore')

                        if 'password' in body:
                            folder = 'Password'
                        elif 'unsubscribe' in body:
                            folder = 'Promos'
                        elif 'reunion' in body:
                            folder = 'Reuniones'
                        elif 'factura' in body:
                            folder = 'Factura'
                        elif 'reclamo' in body:
                            folder = 'Reclamos'
                        elif 'LinkedIn' or 'linkedin' or 'work' or 'trabajo' in body:
                            folder = 'Trabajo'
            
            else: 
                content_type = message.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    try:
                        body = message.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except (AttributeError, UnicodeDecodeError) as error:
                        print(f'error: {error}')
                    
                    if 'unsubscribe' in body:
                        folder = 'Promos'
    if folder:
        print('-' * 28)
        print('archivo requerido encontrado')
        print('-' * 28)
        mail.create(folder)
        mail.copy(email_id, folder)
        mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()

mail.close()