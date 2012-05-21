from Tkinter import *
import ttk
import smtplib
import smsFunc
import smsAction

def configure(*args):
  disableInput()
  emailoutput.set(smsFunc.sms_main(str(username.get()), str(server.get()), str(passw.get()), str(folder.get()), str(number.get())))
  #Update email output window
  try:
    ttk.Label(emailwindow, textvariable=emailoutput).grid(column=1, row=1, stick=W)
  except:
    emailwindow = ttk.Labelframe(mainframe, width=100, height=25, text='Email Output')
    emailwindow.grid(column=3, row=15, sticky=W)
  ttk.Label(emailwindow, textvariable=emailoutput).grid(column=1, row=1, stick=W)
  repeater()
  txt_main()

def disableInput(*args):
  username_entry.configure(state=DISABLED)
  server_entry.configure(state=DISABLED)
  passw_entry.configure(state=DISABLED)
  folder_entry.configure(state=DISABLED)
  number_entry.configure(state=DISABLED)

def repeater():
  emailwindow.after(11000, configure)
  print "GO"

def stop(*args):
  username_entry.configure(state=NORMAL)
  server_entry.configure(state=NORMAL)
  passw_entry.configure(state=NORMAL)
  folder_entry.configure(state=NORMAL)
  number_entry.configure(state=NORMAL)
  emailwindow.destroy()
  print "STOP"

def textFile():
  try:
    fstream = open('userInfo.txt')
    txtUserName = fstream.readline()[:-1]
    txtServer = fstream.readline()[:-1]
    txtFolder = fstream.readline()[:-1]
    txtNumber = fstream.readline()

    username.set(txtUserName)
    server.set(txtServer)
    folder.set(txtFolder)
    number.set(txtNumber)
  except IOError as e:
    print "no userInfo txt file, manual input required."

#############################################################
################### SMTP EMAIL HANDLING #####################
#############################################################
def send_email(sender, receiver, subject, body, password, HOST):
  msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"
    %(sender, receiver, subject, body))
  s = smtplib.SMTP(HOST)
  s.starttls()
  s.login(sender, password)
  s.sendmail(sender, [receiver], msg)
  s.quit()

def txt_main():
  #Grab host, sender, receiver, password info
  HOST = str(server.get())
  TO = str(number.get())
  FROM = str(username.get())
  pass_word = str(passw.get())

  TO += '@vtext.com' #For verizon phones

  question = str(emailoutput.get())
  query = ''
  SUBJECT = ''

  if 'define' in question:
    index = question.find("define ")
    index += 7
    query = question[index:]
    SUBJECT = query
    print query
    BODY = smsAction.search_dictionary(query)
    print BODY
  elif 'weather' in question:
    index = question.find("weather ")
    index += 8
    query = question[index:]
    SUBJECT = query
    print query
    BODY = smsAction.get_weather(query)
    print BODY
  elif 'dhalls' in question:
    BODY = smsAction.get_dhalls()
    print BODY
  elif 'grabngo' in question:
    BODY = smsAction.get_grabngo()
    print BODY
  elif 'markets' in question:
    BODY = smsAction.get_markets()
    print BODY
  elif question == "Sorry, most recent email was received over 10 seconds ago.":
    return
  else:
    BODY = "Query not found!"
    print BODY

  if (len(BODY) + len(SUBJECT) + 3) > 160:
    i = 160 - len(SUBJECT)
    BODY2 = '...'+BODY[i:]
    send_email(FROM, TO, SUBJECT, BODY, pass_word, HOST)
    send_email(FROM, TO, SUBJECT, BODY2, pass_word, HOST)
  else:
    send_email(FROM, TO, SUBJECT, BODY, pass_word, HOST)
#############################################################
#############################################################
#############################################################

root = Tk()
root.title("SMS->Email App")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#Email info StringVars
username = StringVar()
server = StringVar()
passw = StringVar()
folder = StringVar()
number = StringVar()

#StringVar grabbed from smsFunc
emailoutput = StringVar()

#Check userInfo text file
textFile()

#Email info input entry/grids
username_entry = ttk.Entry(mainframe, width=20, textvariable=username)
username_entry.grid(column=2, row=1, sticky=(W, E))
server_entry = ttk.Entry(mainframe, width=20, textvariable=server)
server_entry.grid(column=2, row=3, sticky=(W, E))
passw_entry = ttk.Entry(mainframe, width=20, textvariable=passw, show="*")
passw_entry.grid(column=2, row=5, sticky=(W, E))
folder_entry = ttk.Entry(mainframe, width=20, textvariable=folder)
folder_entry.grid(column=2, row=7, sticky=(W, E))
number_entry = ttk.Entry(mainframe, width=20, textvariable=number)
number_entry.grid(column=2, row=9, sticky=(W, E))

#Email output window
emailwindow = ttk.Labelframe(mainframe, width=100, height=25, text='Email Output')
emailwindow.grid(column=3, row=15, sticky=W)

runButton = ttk.Button(mainframe, text="Run", command=configure).grid(column=3, row=13, sticky=W)
stopButton = ttk.Button(mainframe, text="Stop", command=stop).grid(column=4, row=13, sticky=E)

ttk.Label(mainframe, text="Username").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="IMAP Address").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="Password").grid(column=1, row=5, sticky=E)
ttk.Label(mainframe, text="Inbox Folder (e.g. 'inbox')").grid(column=1, row=7, sticky=E)
ttk.Label(mainframe, text="Phone Number").grid(column=1, row=9, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
#for child in emailwindow.winfo_children(): child.grid_configure(padx=5, pady=5)

if open('userInfo.txt'):
  passw_entry.focus()
else:
  username_entry.focus()

root.bind('<Return>', configure)

root.mainloop()
