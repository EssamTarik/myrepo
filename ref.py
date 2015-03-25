#!/usr/bin/env python
def todict(string):
	res={}
	for keysvals in string.split('&'):
		keyval=keysvals.split('=')
		res[keyval[0]]=keyval[1]
	return res


def getargs(environ):
	args={}
	if(environ['REQUEST_METHOD']=='GET'):
		try:
			args=todict(environ['QUERY_STRING'])
		except:
			print "couldn't parse get request"
	elif(environ['REQUEST_METHOD']=='POST'):
		try:
			size=environ['CONTENT_LENGTH']
			args=todict(environ['wsgi.input'].read(int(size)))
		except:
			print 'couldnt parse post request'

	return args