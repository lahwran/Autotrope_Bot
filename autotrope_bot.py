import log
import trope
import praw
import sys
import os
import time
import urllib2
from BeautifulSoup import BeautifulSoup

log.pink('Starting Program')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def kill_program(reason):
	log.red('Killing Program!')
	log.red(reason)
	sys.exit()

def get_link(comment):
  try:
	for word in comment.body.split(' '):
		if 'tvtropes.org/pmwiki/pmwiki.php/Main/' in word:
			link = word
		if link.find('](') != -1:
			s = link.find('(http')
			e = link.find(')')
			link = link[s+1:e]
	return link
  except:
	return False
	
def is_old_enough(comment):
	current_time = int(time.time())
	created_time = comment.created_utc 
	wait = 60 * 3
	return current_time - created_time > wait
	
def is_legit(comment):
	if not 'tvtropes.org/pmwiki/pmwiki.php/Main/' in comment.body:
		return False
	elif comment.author == username:
		return False
	elif comment.author in leave_them:
		return False
	elif comment.id in done_posts:
		return False
	elif is_old_enough(comment):
		return False
	else:
		return True
def load_data():
	global username, password, subreddits_to_scan, leave_them, done_posts, max_length
	try:
		with open('data_file.inf', 'r') as f:
		  data = f.readlines()
		username = data[0].strip()
		password = data[1].strip()
		subreddits_to_scan = data[2].strip()
		leave_them = data[3].strip().split()
		done_posts = data[4].strip().split()
		max_length = int(data[5].strip())
		sub = 'autotrope_test'
		log.norm('Loaded Data')
	except IOError:
		kill_program('Can\'t find datafile.')
	except Exception as error:
		kill_program('At data load: {0}'.format(error))

def save_data():
	global username, password, subreddits_to_scan, leave_them, done_posts, max_length

	try:
		with open('data_file.inf', 'w+') as f:
			f.write('{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(username, password, subreddits_to_scan, ' '.join(leave_them), ' '.join(done_posts), max_length))
	except Exception as error:
		log.red('Fail at data save: {0}'.format(error))
	else:
		log.green('Saved Data!')

username, password, subreddits_to_scan, leave_them, done_posts, max_length = '      '	
load_data()
r = praw.Reddit("Test Autotrope Bot by /u/youareinthematrix")
try:
	r.login(username, password)
	log.green('Logged in.')
except praw.errors.InvalidUserPass:
	kill_program('Bad login.')
except Exception as error:
	kill_program('At login: {0}'.format(error))

while True:
	try:
		for comment in praw.helpers.comment_stream(r,subreddits_to_scan):
			try:
				if is_legit(comment):
					link = get_link(comment)
					if link:
						try:
							page = trope.get_page(link, max_length)
							comment_text = "{0}\n----\n____\n{1}\n\n[Read More]({2})\n____\n*I am a bot. [Here is my sub](http://reddit.com/r/autotrope)*".format(page[0], page[1], link)
							comment.reply(comment_text)
							log.norm('Added comment! {0}'.format(comment.id))
						except Exception as error:
							log.blue('Error at getting page: {0}'.format(error))
						finally:
							done_posts.append(comment.id)
					else:
						log.yellow('{0} has a url, but it can\'t be found!'.format(comment.id))
			except Exception as error:
				log.blue('Error at in main loop : {0}'.format(error))
	except KeyboardInterrupt:
		save_data()
		kill_program('Killed by user')
			
				

