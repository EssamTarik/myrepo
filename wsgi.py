#!/usr/bin/env python
def todict(string):
	resultDict={}
	for keysvals in string.split('&'):
		keyval=keysvals.split('=')
		resultDict[keyval[0]]=keyval[1]
	return resultDict

def talk():
	return 'talking shit'


def files():
	return open('./static/file.html').read()

def go():
	return 'going'
routes={'talk':talk,'file':files,'go':go}


class Request:
	def __init__(self,env):
		self.args={}
		self.method=env['REQUEST_METHOD']
		self.path=env['PATH_INFO'][1:]
		if self.method=='GET':
			self.parseGet(env)
		elif self.method=='POST':
			self.parsePost(env)
	def parseGet(self,env):
		try:
			data=env['QUERY_STRING']
			self.args=todict(data)
		except:
			print 'couldn\'t parse get request'
	def parsePost(self,env):
		try:
			data=env['wsgi.input'].read(int(env['CONTENT_LENGTH']))
			self.args=todict(data)
		except:
			print "could not parse post request"

class Response:
	def __init__(self,start_response):
		self.respond=start_response
		self.code='200 OK'
		self.headers=[('Content-Type','text/html')]
	def __call__(self,request):
		from Cookie import SimpleCookie

		self.respond(self.code,self.headers)
		if routes.get(request.path,None)!=None:
			global message
			message=routes[request.path]()
		return [str(message)]



def application(env,start_response):
	currentRequest=Request(env)
	response=Response(start_response)
	from Cookie import SimpleCookie
	c=SimpleCookie(env['HTTP_COOKIE'])
	global message
	message=c['name'].value
	return response(currentRequest)


#from wsgiref.simple_server import make_server
#make_server('localhost',8000,application).serve_forever()

from werkzeug.serving import run_simple
run_simple('192.168.43.134',8000,application,use_debugger=True,use_reloader=True)