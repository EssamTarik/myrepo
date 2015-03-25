#!/usr/bin/env python
from werkzeug.serving import run_simple
from ref import getargs
import MySQLdb
import re
cursor=MySQLdb.connect('localhost','wsgi','wsgi','user_data').cursor()

def readroute(route,args):
	if(route=='login'):
		return [open('login.html').read()]
	elif(route=='loginprocess'):
		if(args.has_key('name') and args.has_key('password')):
			cursor.execute('select name from users where name=\'%s\' and password=\'%s\''%(args['name'],args['password']))
			try:
				res=cursor.fetchone()[0]
				return [open('welcome.html').read()%(res,'welcome '+res)]
			except TypeError:
				return ['not found']

	return ['another commit']

def application(environ,start_response):
	start_response('200 OK',[('Location','http://www.google.com'),('Content-Type','text/html')])
	args=getargs(environ)
	return ['welcome']


if __name__=='__main__':
	run_simple('localhost',8000,application,use_debugger=True,use_reloader=True)
