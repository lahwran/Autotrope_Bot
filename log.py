# File borrowed from `wikibot`, in turn borrowed from Zack Maril
# @ https://github.com/zmaril
import re
import time


def formatted(*args):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    return "[{}] {}".format(now, " ".join(str(x) for x in args))


def norm(*args):
    print formatted(*args)


def red(*args):
    print '\033[91m{}\033[0m'.format(formatted(*args))


def yellow(*args):
    print '\033[93m{}\033[0m'.format(formatted(*args))


def green(*args):
    print '\033[92m{}\033[0m'.format(formatted(*args))


def pink(*args):
    print '\033[95m{}\033[0m'.format(formatted(*args))


def blue(*args):
    print '\033[94m{}\033[0m'.format(formatted(*args))
