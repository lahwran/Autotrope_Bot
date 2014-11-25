# File borrowed from	wikibot, in turn borrowed from Zack Maril @ https://github.com/zmaril
import re, time

def formatted(*args):
	now = time.strftime("%Y-%m-%d %H:%M:%S")
	return "["+now+"] "+" ".join(map(str,args))


def norm(*args):
	print apply(formatted,args)

def red(*args):
	print '\033[91m'+apply(formatted,args)+'\033[0m'

def yellow(*args):
	print '\033[93m'+apply(formatted,args)+'\033[0m'

def green(*args):
	print '\033[92m'+apply(formatted,args)+'\033[0m'
		
def pink(*args):
	print '\033[95m'+apply(formatted,args)+'\033[0m'
		
def blue(*args):
	print '\033[94m'+apply(formatted,args)+'\033[0m'
