import urllib2, re
from BeautifulSoup import BeautifulSoup
# This is in a separate file in order to clean up the main code. The function takes in a 
# url and outputs a list with the header and body text

def get_page(url, max_length):
	elements = []
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)
	
	# Get header
	header = soup.find('div', {'class':"pagetitle"})
	header = header.find('span').text
	elements.append(header)
	
	# Get wiki text
	wiki_text = soup.find(id="wikitext").prettify()
	wiki_text = wiki_text[:wiki_text.find('<hr />')]
	soup = BeautifulSoup(wiki_text)
	for div in soup.findAll('div', 'quoteright'):
		div.extract()
	for div in soup.findAll('div', 'acaptionright'):
		div.extract()
	for div in soup.findAll('div', 'indent'):
		div.extract()
	# Change links to markdown
	for link in soup.findAll('a', href=True):
		link.replaceWith('[{0}]({1})'.format(link.text, link['href']))
	wiki_text = soup.prettify()
	# Change other elements to markdown, clean up in general
	wiki_text = wiki_text.replace('<b>\n ','**')
	wiki_text = wiki_text.replace('\n </b>','**')
	wiki_text = wiki_text.replace('\n <em>\n  ',' __')
	wiki_text = wiki_text.replace('\n </em>','__')
	wiki_text = wiki_text.replace('<p>','')
	wiki_text = wiki_text.replace('</p>','')
	wiki_text = wiki_text.replace('<div id="wikitext">','')
	wiki_text = wiki_text.replace('</div>','')
	i = wiki_text.find('\n \n')
	j = 0
	while i < max_length:
		j += 1
		i = wiki_text.find('\n \n', j)
	wiki_text = wiki_text[:i]
	elements.append(wiki_text)
	return elements

