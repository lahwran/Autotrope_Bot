import urllib2
import re
from BeautifulSoup import BeautifulSoup
# This is in a separate file in order to clean up the main code. The function
# takes in a url and outputs a list with the header and body text.

whitelist_tags = ['a', 'b', 'em', 'p']  # Tags we keep

remove_divs = ['quoteright', 'acaptionright', 'indent']


def get_page(url, max_length):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)

    # Get header
    header = soup.find('div', {'class': "pagetitle"})
    header = header.find('span').text

    # Get wiki text
    wiki_text = soup.find(id="wikitext").prettify()
    wiki_text = wiki_text[:wiki_text.find('<hr />')]
    soup = BeautifulSoup(wiki_text)

    # Change links to markdown
    for link in soup.findAll('a', href=True):
        link.replaceWith(' [{0}]({1}) '.format(link.text, link['href']))

    for tag in soup.findAll():
        if (tag.name.lower() == 'div' and tag.get('id', None) in remove_divs):
            tag.extract()
        elif tag.name.lower() == 'a' and 'href' in tag:
            tag.replaceWith(' [{0}]({1}) '.format(tag.text, tag['href']))
        elif not tag.name.lower() in whitelist_tags:
            tag.name = 'remove'
            tag.attrs = []

    # Change other elements to markdown, clean up in general
    wiki_text = soup.prettify()

    # remove newlines, and any whitespace around them
    wiki_text = re.sub('\s*\n\s*', '', wiki_text)

    # turn all repeating whitespace into single spaces
    wiki_text = re.sub('\s+', ' ', wiki_text)

    # match any amount of whitespace, start-of-bold, then any amount
    # of whitespace; replace it with a space and then a double-star.
    wiki_text = re.sub("\s*<b>\s*", " **", wiki_text)

    # match any amount of whitespace, end-of-bold, then any amount
    # of whitespace; replace it with a double-star and then a space.
    wiki_text = re.sub("\s*</b>\s*", "** ", wiki_text)

    # match any amount of whitespace, start-of or end-of italic, then any
    # amount of whitespace; replace it with spaces and stars.
    wiki_text = re.sub("\s*<em>\s*", " *", wiki_text)
    wiki_text = re.sub("\s*</em>\s*", "* ", wiki_text)

    # drop all remaining html tags.
    wiki_text = re.sub('</?remove */?>', '', wiki_text)

    # note: as reddit renders &nbsp; correctly, don't remove it

    wiki_text = wiki_text.replace('</p>', '')
    wiki_text = wiki_text.replace('<p>', '\n \n')

    # Limit the minimum length of the comment.

    # TODO: this is a mess; need to make it clearer what units max_length is
    # in, and don't use \n-space-\n markers as they can occur by accident.
    # also don't use .find(), as that can return -1 and cause incorrect
    # behavior.

    i = wiki_text.split('\n \n')
    j = 0
    while i < max_length:
        j += 1
        i = wiki_text.find('\n \n', j)
    wiki_text = wiki_text[:i]
    return header, wiki_text

if __name__ == '__main__':
    i = get_page('http://tvtropes.org/pmwiki/pmwiki.php/Main/TimeyWimeyBall',
                 600)
    print i
