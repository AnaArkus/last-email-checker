# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:58:20 2023

@author: ana_j
"""

import time
from itertools import chain
import email
import imaplib
import base64
import os
import re
import yaml  


with open("credentials.yml") as f:
    content = f.read()
    
my_credentials = yaml.load(content,Loader=yaml.FullLoader)
user, password = my_credentials["user"], my_credentials["password"]

imap_url = 'imap.gmail.com'

imap_port = 993

uid_max = 0

filters = {}

my_mail = imaplib.IMAP4_SSL(imap_url)
my_mail.login(user,password)
my_mail.select('Inbox')

def search_string(uid_max,filters):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), filters.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))

result, data = my_mail.uid('SEARCH',None, search_string(uid_max,filters))
print(f'Fetch response for message {result}')
print(f'Raw email data:\n{data[0][1]}')

my_mail_uid_list = [int(s) for s in data[0].split()]
if my_mail_uid_list:
    uid_max = max(my_mail_uid_list)
    print(uid_max)
my_mail.logout()

# new_emails = [] 

while 1:
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select('Inbox')
    result, data = my_mail.uid('SEARCH',None, search_string(uid_max,filters))
    my_mail_uid_list = [int(s) for s in data[0].split()]

    for uid in my_mail_uid_list:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:                        
                result, data = my_mail.uid('fetch', str(uid), '(RFC822)')
               
                # new_emails.append(data)
                for response_part in data:
                    if isinstance(response_part, tuple):                    
                        print(email.message_from_bytes(response_part[1]))
                uid_max = uid         



