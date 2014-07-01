# Create your views here.
from django.db.models import F
from django.utils import simplejson
from django.db import models
from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import redirect
import simplejson as sjs
from paw.models import FileInfo
from paw.models import UserInfo
import os

def validatedResp(req):
    uid=req.POST['login']
    passHash=req.POST['hashpass']
    user_info=UserInfo().matchUserPass(uid,passHash)
    t=loader.get_template('l2.html')
    if (user_info is None):
        t=loader.get_template('l1.html')
        c=RequestContext(req,{'errMsg':'Login failed. Try again'})
        return HttpResponse(t.render(c))
    tkn=UserInfo.genPasswd()
    user_info.in_session=tkn
    user_info.save()
    file_info=FileInfo.getByUser(uid)
    file_lst=[]
    if(file_info):
        file_lst = ['/static/'+fi.fileName for fi in file_info]
    c=RequestContext(req,{'uid':uid,'file_list':",".join(file_lst),'tkn':tkn})
    return HttpResponse(t.render(c))

def logout(req):
    tkn=None
    if ('tkn' in req.GET):
        tkn=req.GET['tkn']
        uid=req.GET['uid']
        user_info=UserInfo.getUserSession(uid,tkn)
        if(user_info):
            user_info.in_session=''
            user_info.save()
    return redirect('/')


def login(req):
    reqVars={}
    for k in req.POST:
        reqVars[k]=req.POST[k] 
    if 'login' in reqVars:
        #Process as login validation
        return validatedResp(req)
    c=RequestContext(req)
    t=loader.get_template('l1.html')
    return HttpResponse(t.render(c))
    

def index(req):
    jsonObj=None
    retObj={}
    fi=FileInfo.getLastN(15);
    print 'fi = %s\n' % fi
    for f in fi:
        retObj[f.recNo]='/static/'+f.fileName
    retStr=simplejson.dumps(retObj)
    print ('retStr %s\n' % retStr)
    c=Context({'imgs':retStr,'lgn_scr':'l1.html'})
    t=loader.get_template('b1.html')
    #return HttpResponse(retStr, mimetype='application/json')
    return HttpResponse(t.render(c))

def hello(req):
    jsonObj=None
    retObj={}
    fi=FileInfo.getLastN(15);
    print 'fi = %s\n' % fi
    for f in fi:
        retObj[f.recNo]='/static/'+f.fileName
    retStr=simplejson.dumps(retObj)
    print ('retStr %s\n' % retStr)
    c=Context({'imgs':retStr,'lgn_scr':'l1.html'})
    t=loader.get_template('b3.html')
    #return HttpResponse(retStr, mimetype='application/json')
    return HttpResponse(t.render(c))

def putfilenames(req):
    print('hit putfilenames\n')
    print ('type of req = %s' % type (req))
    ##  print 'req=%s'%req
    retObj={}
    fi=None
    id=req.GET['id']
    n_imgs=req.GET['nimgs']
    print 'n_imgs=%s'%n_imgs
    if (id and int(id)>0):
        print('req True id = %s\n'%id)
        if n_imgs > 0:
            fi=FileInfo.getNextN(id,n_imgs)
        else:
            fi=FileInfo.getNextN(id)
    else:
        print('req False\n')
        fi=FileInfo.objects.order_by('recNo').reverse()
    print 'back ... \n'
    print 'fi = %s\n' % fi
    for f in fi:
        retObj[f.recNo]='/static/'+f.fileName
    retStr=simplejson.dumps(retObj)
    print ('retStr %s\n' % retStr)
    return HttpResponse(retStr, mimetype='application/json')

def etc(req):
#    t=loader.get_template(req)
    return HttpResponse(req.__dict__)
#    return HttpResponse(t.render())

