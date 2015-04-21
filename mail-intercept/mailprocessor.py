#!/usr/bin/python 
# This is a heavily debug-statemented piece, as it handled incoming emails and 
# there are lots of things that could go wrong. I have not taken the time to clean
# this up yet, but at least, this worked fine at the time of its check-in, and would
# work again if the setup is done properly again.
# The setup for a mail interceptor like this is to some extent dependent on the mail solution
# In this case I probably used one of the free email programs, perhaps dovecot or one of the more
# popular softwares. 

import sys, email, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append('/home/sunil/djcode/mysite/')
from paw.models import FileInfo
from paw.models import UserInfo
from time import gmtime
import calendar
# Import smtplib for the actual sending function
import smtplib
import hashlib
import PythonMagick

# Import the email modules we'll need
from email.mime.text import MIMEText
import re

def mailPasswdToNewUser(em,pss,f=None):
  if(f):
    f.write('mailPasswdToNewUser...enter\n')
  msg_text='Use Username "'+em+'" and password "'+pss+'" to access your pictures at http://pennyappware.com:8002/ . Good luck!'
  #me='"Admin, Pennyappware.com" <donotreply@pennyappware.com>'
  me='donotreply@pennyappware.com'

  if(f):
    f.write('msg_text=%s\nme=%s\nem=%s\n' % (msg_text,me,em))
  msg=MIMEText(msg_text)
  msg['Subject'] = 'Your pennyappware.com account password'
  msg['From'] = me
  msg['To'] = em
  
  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  s = smtplib.SMTP('smtp.comcast.net',587)
  s.login('sunilramnarayan','LateTime9')
  if(f):
    f.write('inited smtplib\n')
  s.sendmail(me, [em], msg.as_string())
  if(f):
    f.write('called sendmail\n')
  s.quit()

# from email.feedparser import FeedParser as fdp

try:
  # open file stream
  file_name="logs/m.log"
  #msgfile_name="logs/mmsg.log"
  print 'opening %s\n' % file_name
  file = open(file_name, "w")
  #print 'opening %s\n' % msgfile_name
  #msgfile = open(msgfile_name, "w")
except IOError:
  print 'log file open err'
  sys.exit(4)

em = email.message_from_file(sys.stdin) # Read message from Std Input


#for n,v in em.items():
#  file.write('%s --- %s\n' % (n,v))

if em.is_multipart():
  file_text = 'multipart? YES\n'
  try:
    file.write(file_text)
  except IOError:
    print "mailprocessor: Errored when writing log\n"

  for part in em.walk():
    filename = part.get_filename()
    if filename:
      if ((filename[-4:]).upper() != '.JPG'):
          next
      filename=UserInfo.genPasswd(32) + '.jpg'
      #fpath='/home/sunil/djcode/mysite/paw/media/%s' % filename
      fpath='/data/%s' % filename
      try:
        #        file.write('filename: %s\nfpath = %s\n' % (filename,fpath))
        #recNo        | int(11)       | NO   | PRI | NULL    | auto_increment |
        #| fileName     | varchar(255)  | NO   |     | NULL    |                |
        #| filePath     | varchar(255)  | NO   |     | NULL    |                |
        #| userName     | varchar(255)  | NO   |     | NULL    |                |
        #| emailSubj    | varchar(255)  | NO   |     | NULL    |                |
        #| emailContent | varchar(4095) | YES  |     | NULL    |                |
        #| sendTime     | time          | NO   |     | NULL    |                |
        #| sysTimeRecv  | bigint(20)    | NO   |     | NULL    |                |
        #| senderIpV4   | varchar(16)   | YES  |     | NULL    |                |
        #| status       | varchar(1)    | YES  |     | NULL    |                |
        #+--------------+---------------+------+-----+---------+----------------+

        #file_text += 'writing to file %s\n' % fpath;
        filedata = part.get_payload(decode=True)
        fid=open(fpath,"wb")
        #fid=open(filename,"wb")
        file.write('opened filename: %s\n' % (filename))
        fid.write(filedata)
        fid.close()
        img = PythonMagick.Image(fpath)
      except IOError as e:
        file.write('mailprocessor: Errored when writing :%s %s\n' % (e.errno, e.strerror))
      try:
        file_info = FileInfo()
        file.write('created FileInfo...\n')
        file_info.fileName=filename
        file_info.filePath='/data/'

        file.write('assigned fileName...\n')
        from_fld=em.get_all('From', [])
        file.write('from_fld = %s\n' % from_fld[0])
        em_addr=''
        emaddr_search=re.search('[A-z0-9.]+@[A-z0-9.]+',from_fld[0])
        if(emaddr_search):
          em_addr=emaddr_search.group(0)
        file.write('em_addr = %s...\n' % em_addr)
        (eml,dom)=em_addr.split('@')
        file.write('eml,dom = %s,%s...\n' % (eml,dom))
        file_info.userName=em_addr

        file.write('assigned userName...\n')
        file_info.sendTime=calendar.timegm(gmtime())

        file.write('assigned sendTime...')
        file_info.emailSubj=em.get_all('Subject', [])

        now = calendar.timegm(gmtime())
        file_info.sysTimeRecv=now

        file.write('saving...\n')
        file_info.save()
        file.write('saved...\n')
        uinfo_tbl=UserInfo()
        userpass=uinfo_tbl.putNewUser(em_addr,file)
        if(userpass != None):
          #Send password back to user
          file.write('Put UserInfo.. assigning pss\n')
          mailPasswdToNewUser(file_info.userName,userpass,file)
      #except IntegrityError as inte:
      #  file.write('mailprocessor: IntegrityError\n')
      #except DatabaseError as dbe:
      #  file.write('mailprocessor: DatabaseError\n')
      except IOError as e:
        file.write('mailprocessor: Errored when writing :%s %s\n' % (e.errno, e.strerror))
      file.write('out ...\n')
    else:
      try:
        file.write('No filename found for attachmt\n')
      except IOError:
        print "mailprocessor: Errored when writing log(1)\n"
else:
  try:
    file.write('multipart? NO')
  except IOError:
    print "mailprocessor: Errored when writing log(1)\n"
  #file_text = 'multipart? NO'


try:
  file_text += '\n\nGOT MAIL!! \n\n: '
#  file_text += em.as_string()
#  file.write(file_text)
except IOError:
  print "mailprocessor: Errored when opening log\n"
  sys.exit(3)
#finally:
file.close()
file=None

sys.exit(0)


def conv_time(stime):
  return calendar.timegm(gmtime())
    



