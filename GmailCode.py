import smtplib
from email.message import EmailMessage
from random import randint


def send_code_to(email):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('rus.darkmail@gmail.com', 'Q5G9jY+Kn')
    l_C = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    l_s = 'zyxwvutsrqponmlkjihgfedcba'
    n = '0123456789'
    code = l_C[randint(0, len(l_C) - 1)] + l_s[randint(0, len(l_s) - 1)] + n[randint(0, 9)]
    code = code + l_C[randint(0, len(l_C) - 1)] + l_s[randint(0, len(l_s) - 1)] + n[randint(0, 9)]
    code = code + l_C[randint(0, len(l_C) - 1)] + l_s[randint(0, len(l_s) - 1)] + n[randint(0, 9)]
    msg = EmailMessage()
    msg.set_content(code)
    msg['Subject'] = 'Code'
    msg['From'] = 'DarkMail'
    text = 'Hi. Here is your registration code. Please use it on DarkMail:'
    smtpObj.sendmail("rus.darkmail@gmail.com", email, text + ' ' + code)
    smtpObj.quit()
    return code


def send_report(text):
    count = 0
    with open('reports_sended.txt', 'r') as file:
        data = file.readline()
        count = int(data)
    with open('reports_sended.txt', 'w') as file:
        file.write(str(count))
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('rus.darkmail@gmail.com', 'Q5G9jY+Kn')
    smtpObj.sendmail("rus.darkmail@gmail.com", 'bot-error@mail.ru', text)
    smtpObj.quit()
