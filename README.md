# <u>Email Classifier</u>

## Welcome! this is the app that i made for classify your emails

## I´m gonna teach to you how this work so you can modify and use to yourself

### configure your email

- create an application password:
  first of all you need to say the program what is your email, for this you need to have an application password created inside of your gmail.

- create a file: you will need to put your email and the app password in variables inside a file with name you want, in my case was `.env`, create it on the root of the proyect. I name the variables `smtp_username` and `smtp_password`

- import the module on main.py so you can use the variables on the future, here is how i did it:

```
from dotenv import load_dotenv

load_dotenv()

...

username = os.getenv('smtp_username')
password = os.getenv('smtp_password')
```

### Classify your emails

On main.py you will need to write the filters you need, this is what i need:

```

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

...

elif content_type == 'text/plain' or content_type == 'text/html':
try:
body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
except UnicodeDecodeError:
body = part.get_payload(decode=True).decode('latin1', errors='ignore')

    # Here write your filters for your emails
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

...

if 'unsubscribe' in body:
folder = 'Promos'
```

Dont forget to create an environment to install all the dependencies with conda or `python -m venv <the name of your env>`

Use `python main.py` in the proyect root to run the code, and if you want to create an executable you only have to type `pyinstaller --onefile --console --name email_classifier --icon=icon.ico main.py` on the console. You will find the `.exe` on <b>dist/email_classifier.exe</b> if you ran the <b>pyinstaller</b> command previously.
