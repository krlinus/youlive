import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append('/home/sunil/djcode/mysite/')
sys.path.append('/home/sunil/djcode/mysite/paw/jq')
from django.db.models import F
from django.db import models

import datetime
import string
from random import choice
import uuid
import hashlib
import calendar
from time import gmtime

# Create your models here.
class FileInfo(models.Model):
    recNo = models.AutoField(max_length=12,primary_key=True)
    fileName = models.CharField(max_length=255)
    filePath  = models.CharField(max_length=255,null=True)
    userName = models.CharField(max_length=255)
    emailSubj = models.CharField(max_length=255,null=True)
    emailContent= models.CharField(max_length=4095,null=True)
    sendTime = models.BigIntegerField(max_length=20,null=True)
    sysTimeRecv = models.BigIntegerField(max_length=20,null=True)
    senderIpV4 = models.CharField(max_length=16,null=True)
    status=models.CharField(max_length=1,null=True)
    @staticmethod
    def getByUser(uid):
        print("getByUser called with uid=%s\n" % uid)
        srchRes=FileInfo.objects.filter(userName__iexact=uid)
        if (srchRes.exists()):
            return srchRes
        return None

    @staticmethod
    def getLastN(n=5):
        print("getLastN called\n")
        return FileInfo.objects.order_by('recNo').reverse()[:n]

    @staticmethod
    def getNextN(start_from,n=5):
        print("getNextN called.... \n")
        fi= FileInfo.objects.filter(recNo__gt=start_from)
        retval=[itm for itm in fi]
        nfi=len(retval)
        print 'fi-len=%s, n=%s' % (nfi,n)
        r=0
        if int(nfi) < int(n):
            print 'nfi<n'
            r= int(n) - int(nfi)
            print 'r=%s'%r
            fi2=FileInfo.objects.order_by('recNo')[:r]
            supvals=[itm for itm in fi2]
            print 'getNextN getting %s more from top'%r
            retval.extend(supvals)
        elif int(nfi) > int(n):
            retval=retval[:-(int(n))]
        return retval

class UserInfo(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    email_domain = models.CharField(max_length=64,null=True)
    in_session = models.CharField(max_length=32,null=True)
    last_hit = models.BigIntegerField(max_length=20,null=True)
    pass_hash = models.CharField(max_length=1024,null=True)
    salt = models.CharField(max_length=1024,null=True)
    force_pw_change= models.BooleanField()
    def __str__(self):
        return '\nemail=%s\vemail_domain=%s\nin_session=%s\nlast_hit=%s\n'\
          'pass_hash=%s\nsalt=%s\nforce_pw_change=%s\n' % \
          (self.email,self.email_domain,self.in_session,self.last_hit,self.pass_hash,self.salt,self.force_pw_change)
    @staticmethod
    def genPasswd(nchars=8,file=None):
        if(file):
            file.write('GenPasswd....\n')
        chars = string.letters + string.digits
        newpasswd=''
        for i in range(nchars):
            newpasswd = newpasswd + choice(chars)
        return newpasswd


    def __preparePassSaltAndHash(self,em_addr,f=None):
        randpass=UserInfo.genPasswd()
        salted_randpass = randpass+em_addr
        hashed_saltrand=hashlib.sha512(salted_randpass).hexdigest()
        if(f):
            f.write('\nproduced hasted %s \n' % hashed_saltrand)
        new_salt=uuid.uuid4().hex
        hashed_saltrand += new_salt
        hashed_password = hashlib.sha512(hashed_saltrand).hexdigest()        
        return (randpass,hashed_password,new_salt)
        
    def __matchUser(self,uid,f=None):
        print("matchUser called\n")
        if(f):
            f.write('matchUser called uid=%s..\n' % uid)
        return UserInfo.objects.filter(email__iexact=uid)

    def getUserSession(uid,tkn):
        urecQset=UserInfo.objects.filter(email__iexact=uid).filter(in_session__exact=tkn)
        if(urecQset.exists()):
            return urecQset[0]
        return None

    def matchUserPass(self,usid,phash):
        print("matchUserPass called\n")
        urecQset= UserInfo.objects.filter(email__iexact=usid)
        
        if (not urecQset.exists()):
            return None

        db_pass_salt=urecQset[0].salt
        #for k in urecQset:
            #print k.salt
            #db_pass_salt=k
        print "db pass salt = %s\n" % db_pass_salt
        salted_phash = str(phash) + db_pass_salt
        hashed_phash= hashlib.sha512(salted_phash).hexdigest()
        print "pass hash = %s\n" % hashed_phash
        print "DB pass hash = %s\n" % urecQset[0].pass_hash
        urecQset= UserInfo.objects.filter(pass_hash__exact=hashed_phash)
        if(urecQset.exists()): return urecQset[0]
        return None

    def putNewUser(self, eml,f=None):
        print("putNewUser called\n\nrecd eml=%s" %eml)
        if(f != None):
            f.write('putNewUser called\nrecd eml=%s' % eml)
        user_infoQset = self.__matchUser(eml,f)
        user_info=None
        if (user_infoQset.exists()):
            user_info=user_infoQset[0] 
        if(user_info):
            if(f):
                f.write('user_info = %s\n' % user_info)
            return None
        user_info = UserInfo()
        user_info.email = eml
        print('eml=%s\n'%eml)
        user_info.email_domain = eml.split('@')[1]
        (passwd,passhash,salt) = self.__preparePassSaltAndHash(eml,f)
        user_info.pass_hash=passhash
        user_info.salt=salt
        user_info.last_hit=calendar.timegm(gmtime())
        user_info.force_pw_change=True
        user_info.save()
        return passwd


#SmallIntegerField
#EmailField
#DateField
#datetime
#FloatField
#validators
#TimeField
#parse_time
#smart_unicode
#TextField
#IPAddressField
#subclassing
#smart_str
#parse_datetime
#capfirst
#__package__
#forms
#NullBooleanField
#clean_ipv6_address
#CharField
#BooleanField
#__doc__
#math
#DecimalField
#files
#PositiveSmallIntegerField
#BigIntegerField
#IntegerField
#warnings
#__builtins__
#__file__
#PositiveIntegerField
#GenericIPAddressField
#DateTimeField
#FilePathField
#DictWrapper
#related
#timezone
#__name__
#AutoField
#copy
#_
#Field
#settings
#BLANK_CHOICE_NONE
#decimal
#URLField
#connection
#CommaSeparatedIntegerField
#parse_date
#exceptions
#FieldDoesNotExist
#curry
#proxy
