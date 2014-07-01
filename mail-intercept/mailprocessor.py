#!/usr/bin/python 

import sys, email, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append('/home/sunil/djcode/mysite/')
from paw.models import FileInfo
from time import gmtime
import calendar

# from email.feedparser import FeedParser as fdp

try:
  # open file stream
  file_name="logs/m.log"
  file = open(file_name, "w")
except IOError:
  print 'log file open err'
  sys.exit(4)

file_text=''
em = email.message_from_file(sys.stdin) # Read message from Std Input
for n,v in em.items():
  file.write('%s --- %s\n' % (n,v))

if em.is_multipart():
  file_text = 'multipart? YES\n'
  try:
    file.write(file_text)
  except IOError:
    print "mailprocessor: Errored when writing log\n"

  for part in em.walk():
    filename = part.get_filename()
    if filename:
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
      except IOError as e:
        file.write('mailprocessor: Errored when writing :%s %s\n' % (e.errno, e.strerror))
      try:
        file_info = FileInfo()
        file.write('created FileInfo...')
        file_info.fileName=filename
        file_info.filePath='/data/'

        file.write('assigned fileName...')
        file_info.userName=em.get_all('From', [])

        file.write('assigned userName...')
        file_info.sendTime=calendar.timegm(gmtime())

        file.write('assigned sendTime...')
        file_info.emailSubj=em.get_all('Subject', [])

        now = calendar.timegm(gmtime())
        file_info.sysTimeRecv=now

        file.write('saving...\n')
        file_info.save()
        file.write('saved...')
      except IntegrityError as inte:
        file.write('mailprocessor: IntegrityError\n')
      except DatabaseError as dbe:
        file.write('mailprocessor: DatabaseError\n')
      except IOError as e:
        file.write('mailprocessor: Errored when writing :%s %s\n' % (e.errno, e.strerror))
      file.write('out ...\n')
    else:
      try:
        file.write('No filename found for attachmt\n');
      except IOError:
        print "mailprocessor: Errored when writing log(1)\n"
else:
  try:
    file.write('multipart? NO')
  except IOError:
    print "mailprocessor: Errored when writing log(1)\n"
  #file_text = 'multipart? NO'


try:
  file_text += '\n\nGOT MAIL!! \n\nContent: '
  file_text += em.as_string()
  file.write(file_text)
except IOError:
  print "mailprocessor: Errored when opening log\n"
  sys.exit(3)
#finally:
file.close()
file=None

sys.exit(0)


def conv_time(stime):
  return calendar.timegm(gmtime())
    



