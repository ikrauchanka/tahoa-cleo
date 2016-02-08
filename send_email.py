#!/usr/bin/python
import smtplib

def prompt(prompt):
    return raw_input(prompt).strip()

fromaddr = 'myserver@server.com'
toaddrs  = 'tomygmail@gmail.com'
msg = """From: dude@somewhere.com

Hello, this is dog.
"""

print "Message length is " + repr(len(msg))

#Change according to your settings
smtp_server = 'email-smtp.us-east-1.amazonaws.com'
smtp_username = 'ELKFJWENFKJWKWBEFJHWB'
smtp_password = 'VsefleFkekwfj\wefwefqwfdsegrgwg'
smtp_port = '587'
smtp_do_tls = True

server = smtplib.SMTP(
    host = smtp_server,
    port = smtp_port,
    timeout = 10
)
server.set_debuglevel(10)
server.starttls()
server.ehlo()
server.login(smtp_username, smtp_password)
server.sendmail(fromaddr, toaddrs, msg)
print server.quit()
