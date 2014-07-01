#!/usr/bin/python -O

import sys, email, os
# from email.feedparser import FeedParser as fdp

em = email.message_from_file(sys.stdin) # Read message from Std Input

file_text = 'GOT MAIL!! \n\nContent: %s' % em.as_string()
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
