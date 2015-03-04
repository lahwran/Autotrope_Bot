import log
import trope
import praw
import sys
import os
import time

# By logging this, we can tell how long it takes to set up functions and log
# in to reddit.
log.pink('Starting Program')


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
    # TODO XXX FIXME CRITICAL: CATCHING ALL EXCEPTIONS AND IGNORING!
    # what exceptions do we actually want to catch here?
    except:
        return False


def is_old_enough(comment):
    current_time = int(time.time())
    created_time = comment.created_utc
    wait = 60 * 3  # 3 Minutes
    return current_time - created_time > wait


def is_legit(comment):
    if 'tvtropes.org/pmwiki/pmwiki.php/Main/' not in comment.body:
        return False
    elif comment.author == username:
        # Stops bot commenting on own posts
        return False
    elif comment.author in leave_them:
        # Stops bot commenting on bad users (coming in 3.0)
        return False
    elif comment.id in done_posts:
        # Stops bot commenting on already done comments.
        return False
    elif is_old_enough(comment):
        # Stops bot commenting on posts older than 3 minutes
        return False
    else:
        return True


def load_data():
    global username
    global password
    global subreddits_to_scan
    global leave_them
    global done_posts
    global max_length

    # Change this if using a different file
    with open('data_file.inf', 'r') as f:
        data = f.readlines()

    username = data[0].strip()
    password = data[1].strip()
    subreddits_to_scan = data[2].strip()

    leave_them = data[3].strip().split()
    done_posts = data[4].strip().split()

    max_length = int(data[5].strip())
    log.norm('Loaded Data')


def save_data():
    try:
        with open('data_file.inf', 'w+') as f:
            # Writes all existing data to the file, so that the already done
            # comments and people to leave alone are appended to it.
            f.write('{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(username,
                                                          password,
                                                          subreddits_to_scan,
                                                          ' '.join(leave_them),
                                                          ' '.join(done_posts),
                                                          max_length))
    # No point killing the program here - it already has the variables in
    # its memory
    except Exception as error:
        log.red('Fail at data save: {0}'.format(error))
    else:
        log.green('Saved Data!')

# TODO: figure out which of these actually *need* to start out with space,
# and change the ones that don't to None or ''
username = ' '
password = ' '
subreddits_to_scan = ' '
leave_them = ' '
done_posts = ' '
max_length = ' '
comment_text = (
    "{0}\n" +
    "----\n" +
    "____\n" +
    "{1}\n" +
    "\n" +
    "[Read More]({2})\n" +
    "____\n" +
    "*I am a bot. [Here is my sub](http://reddit.com/r/autotrope)*\n"
)

# Sets the path to directory of file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

try:
    # Setting up the reddit instance
    # TODO: use return values instead of globals
    load_data()
except IOError:
    log.red("Can't find datafile.")
    # sys.exit() is generally a very bad thing, but since it's at the top level
    # it should be okay. Anywhere else, it should be an exception that the top
    # level converts to a sys.exit().
    sys.exit()

r = praw.Reddit("Autotrope Bot v2.1 by /u/youareinthematrix")

try:
    # Variables set by load_data().
    r.login(username, password)
    log.green('Logged in.')
except praw.errors.InvalidUserPass:
    log.red('Bad login.')
    # sys.exit() is generally a very bad thing, but since it's at the top level
    # it should be okay. Anywhere else, it should be an exception that the top
    # level converts to a sys.exit().
    sys.exit(1)

bot = r.get_redditor(username)

while True:
    try:
        for comment in bot.get_comments(limit=500):
            if comment.score < -1:
                log.norm('Deleting {0}'.format(comment.id))
                comment.delete()

                # Limit the requests, slows down the program, stops it trying
                # to delete twice.
                time.sleep(10)
    except requests.exceptions.HTTPError:
        log.yellow('HTTP Error!')
    load_data()
