#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Desc: Telegram bot. Python 2.7
#Author: Dimitry Lukin, dimitry.lukin@gmail.com
#Version: 2019041900

from telegram.ext import Updater, MessageHandler, Filters
import re

import pycurl
import StringIO
from pymorphy import get_morph
morph = get_morph('/var/lib/pymorphy')



SIGNIFICANTWORDS = 4

SREF='https://sampowiki.club/doku.php?do=search&id=start&sf=1&q='

STOPLIST = [u'сампо', u'какого', u'соседи', u"привет", u"знает", u"подскажите", u"здравствуйте", u"делают", u"делает", u"какие", u"есть", u"здесь", u'какой', u'куда', u'какому', u'сейчас']

def xmlmethod(mtype, mstring):
    if (mtype == 'search'): 
        request='<?xml version="1.0"?><methodCall><methodName>dokuwiki.search</methodName><params><param><value><string>'+mstring+'</string></value></param></params></methodCall>'
    elif (mtype == 'pageList'):
        request='<?xml version="1.0"?><methodCall><methodName>dokuwiki.getPagelist</methodName><params><param><value><string></string></value></param></params></methodCall>'
    response = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.HTTPHEADER, ["Content-type: text/xml"])
    c.setopt(c.URL, 'http://127.0.0.1/lib/exe/xmlrpc.php')
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.POSTFIELDS, request)
    c.perform()
    c.close()
    r = response.getvalue()
    response.close()
    return r

def getbase(w):
    nword = w.decode('utf-8').upper()
    nwordyset = morph.normalize(nword)

    nwordy = nwordyset.pop()
    searchy = nwordy.lower()
    w = searchy.encode('utf-8')
    return w


def getwiki(search):
    
    if (xmlmethod('pageList', search).find(search) > -1):
        return True
    if (xmlmethod('search', search).find('member') > -1):
        return True
    return False

def isStopWord(word):
    for i in range(0, len(STOPLIST)):
        if word.decode('utf-8').lower() == STOPLIST[i]:
            return True
    return False


def hMessage(bot, update):
    phrase=unicode(update.message.text).encode('utf-8')
    if phrase.count('?') < 1:
        return	

    cPhrase=re.sub('[?.,!#$@:]','', phrase)
    words = cPhrase.split(" ")

    counter=0
    for word in words:
        if len(word)/2 < 4:
            continue
	if isStopWord(word):
            continue
        if counter > SIGNIFICANTWORDS:
            continue
        counter=counter+1
        nword = getbase(word)
        if getwiki(nword) is True:
            bot.send_message(chat_id=update.message.chat_id, text='*'+word+'*'+'   Есть ответ  -> '+ SREF+nword)

def main():
    updater = Updater('887056733:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxI')
    dispatcher = updater.dispatcher
    handle_message = MessageHandler(Filters.text, hMessage)
    dispatcher.add_handler(handle_message)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()

