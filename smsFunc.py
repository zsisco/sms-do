import getpass, imaplib
import email
import datetime
import time
import sys

def get_first_text_block(email_message_instance):
  maintype = email_message_instance.get_content_maintype()
  if maintype == 'multipart':
    for part in email_message_instance.get_payload():
      if part.get_content_maintype() == 'text':
        return part.get_payload()
  elif maintype == 'text':
    return email_message_instance.get_payload()

###########################################################################

def validTime(email_message):
  #Email Time adjustment shit
  eDate = email_message['Date']
  eTime = eDate[12:20]
  eHour = int(eTime[0:2])
  if (eHour - 4) < 0:
    eHour = eHour + 20
  else:
    eHour = eHour - 4
  eMin = int(eTime[3:5])
  eSec = int(eTime[6:8])
  print eHour, ":", eMin, ":", eSec

  localTime = time.localtime(None) #Local time
  localHour = localTime[3]
  localMin = localTime[4]
  localSec = localTime[5]
  print localHour, ":", localMin, ":", localSec
  if localHour != eHour:
    #print '\nSorry most recent email was received over an hour ago'
    return False
  else:
    if (localMin - eMin) == 1:
      if (localSec - eSec) <= (-50) and (localSec - eSec) > (-60):
        print "Special Case:", (localSec - eSec)
        return True
      else:
        print "Sorry"
        return False
    elif localMin != eMin:
      #print '\nSorry most recent email was received over 1 minutes ago'
      return False
    elif localMin == eMin:
      if (localSec - eSec) > 10:
        print '\nSorry most recent email was received over 10 seconds ago'
        return False
      else:
        print '\nEmail was received at valid time...continue'
        return True

###########################################################################

def sms_main(name, imapAdd, password, folder, number):
  #Init
  passw = str(password)
  address = str(imapAdd)
  username = str(name)
  inboxFolder = str(folder)
  phoneNumber = str(number)

  #Login
  mail = imaplib.IMAP4_SSL(address)
  mail.login(username, passw)
  mail.list() # Out: list of "folders" aka labels in mail.
  mail.select(inboxFolder) # connect to inbox.

  #Search for emails only on current day
  date = (datetime.date.today() - datetime.timedelta(0)).strftime("%d-%b-%Y")
  result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
  latest_email_uid = data[0].split()[-1]
  result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
  raw_email = data[0][1]
  #Latest email
  email_message = email.message_from_string(raw_email)

  #Make sure email was received within 5 minutes ago
  if not validTime(email_message):
    return "Sorry, most recent email was received over 10 seconds ago."

  #Retrieve the sender information
  sender = str(email.utils.parseaddr(email_message['From']))
  #Make sure it was sent from correct phone number
  if phoneNumber in sender:
    body = get_first_text_block(email_message)
    return body
  else:
    return "Invalid Sender:\nYA BLEW IT\n"

