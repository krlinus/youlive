#!/usr/bin/python -O

import sys, email, os
# from email.feedparser import FeedParser as fdp

em = email.message_from_file(sys.stdin) # Read message from Std Input

file_text=''

if em.is_multipart():
  file_text = 'multipart? YES'
  for part in em.walk():
    filename = part.get_filename()
    if filename:
      filedata = part.get_payload(decode=True)
      fid=open(filename,"wb")
      fid.write(filedata)
      fid.close
    else:
      print 'No filename found for attachmt'
else:
  file_text = 'multipart? NO'


file_text += '\n\nGOT MAIL!! \n\nContent: '
file_text += em.as_string()
file=None
try:
  # open file stream
  file_name="m.log"
  file = open(file_name, "w")
  file.write(file_text)
except IOError:
  sys.exit(1)
#finally:
file.close()
sys.exit(0)
