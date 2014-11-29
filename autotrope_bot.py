try:
	import log
	import trope
	import praw
	import sys
	import os
	import time
	import urllib2
	from BeautifulSoup import BeautifulSoup
except ImportError:
	print 'Error Importing modules. The bot will most likely crash.'

# By logging this, we can tell how long it takes to set up functions and log in to reddit.
log.pink('Starting Program')

# Gracefully kills the program
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
	wait = 60 * 3 # 3 Minutes
	return current_time - created_time > wait
	
def is_legit(comment):
	if not 'tvtropes.org/pmwiki/pmwiki.php/Main/' in comment.body:
		return False
	elif comment.author == username: # Stops bot commenting on own posts
		return False
	elif comment.author in leave_them: # Stops bot commenting on bad users (coming in 3.0)
		return False
	elif comment.id in done_posts: # Stops bot commenting on already done comments.
		return False
	elif is_old_enough(comment): # Stops bot commenting on posts older than 3 minutes
		return False
	else:
		return True
		
def load_data():
	global username, password, subreddits_to_scan, leave_them, done_posts, max_length
	try:
		with open('data_file.inf', 'r') as f: # Change this if using a different file
		  data = f.readlines()
		  
		username = data[0].strip()
		password = data[1].strip()
		subreddits_to_scan = data[2].strip()
		leave_them = data[3].strip().split() # .split() makes a list from a string, using
		done_posts = data[4].strip().split() # the spaces to sperate items.
		max_length = int(data[5].strip())
		log.norm('Loaded Data')
	
	# If we don't kill the program now, it will crash later on.
	except IOError:
		kill_program('Can\'t find datafile.')
	except Exception as error:
		kill_program('At data load: {0}'.format(error))

def save_data():
	global username, password, subreddits_to_scan, leave_them, done_posts, max_length

	try:
		with open('data_file.inf', 'w+') as f:
			# Writes all existing data to the file, so that the already done comments and
			# people to leave alone are appended to it.
			f.write('{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(username, 
														  password,
														  subreddits_to_scan,
														  ' '.join(leave_them),
														  ' '.join(done_posts),
														  max_length))
	# No point killing the program here - it already has the variables in its memory													
	except Exception as error:
		log.red('Fail at data save: {0}'.format(error))
	else:
		log.green('Saved Data!')
		
username, password, subreddits_to_scan, leave_them, done_posts, max_length = '      '	
comment_text = """\
{0}
----
____
{1}

[Read More]({2})
____
*I am a bot. [Here is my sub](http://reddit.com/r/autotrope)*"""

# Sets the path to directory of file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setting up the reddit instance
load_data()
r = praw.Reddit("Autotrope Bot v2.1 by /u/youareinthematrix")
try:
	r.login(username, password) # Variables set by load_data()
	log.green('Logged in.')
# There's no point continuing with the program if it can't login, so we kill it
except praw.errors.InvalidUserPass:
	kill_program('Bad login.')
except Exception as error:
	kill_program('At login: {0}'.format(error))

# Here's the proper start of the program, where we use a while loop to make it endless
while True:
	try: # I use a lot of try/except blocks, as the old code crashed endlessly. This way,
		 # the problem is simply ignored.
		for comment in praw.helpers.comment_stream(r,subreddits_to_scan): 
			try:
				if is_legit(comment):
					link = get_link(comment)
					if link: # Checks if the link is there.
						try:
							# Go the trope.py to see how this works
							page = trope.get_page(link, max_length)
							# Formats the raw comment text
							comment_text = comment_text.format(page[0], page[1], link)
							comment.reply(comment_text)
							log.norm('Added comment! {0}'.format(comment.id))
						except Exception as error:
							log.blue('Error at getting page: {0}'.format(error))
						finally:
							done_posts.append(comment.id) # Stops double posting
			except Exception as error:
				log.blue('Error at in main loop : {0}'.format(error))
	except KeyboardInterrupt: # Saves data on exit
		save_data()
		kill_program('Killed by user')
