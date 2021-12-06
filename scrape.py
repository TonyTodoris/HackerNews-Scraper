import requests
from bs4 import BeautifulSoup
from pprint import pprint
import click


def get_hn_request(page_num):
	hn_link = 'https://news.ycombinator.com/news'
	if page_num > 0 :
		hn_link = f"{hn_link}?p{page_num}"
	return requests.get(hn_link)

def create_hn_links_and_subtext(num_pages):
	links = []
	subtext = []
	for num in range(num_pages):
		res = get_hn_request(num)
		soup = BeautifulSoup(res.text, 'html.parser')
		links = links + soup.select('.titlelink')
		subtext =  subtext + soup.select('.subtext')
	return links, subtext

def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key=lambda k:k['score'], reverse=True)

def create_custom_hn(links, subtext):
	hn = []
	for idx, item in enumerate(links):
		title = item.getText()
		href = item.get('href', None)
		vote = subtext[idx].select('.score')
		if len(vote):
			score = int(vote[0].getText().replace(' points', ''))
			if score > 99:
				hn.append({'title': title, 'link': href, 'score': score})
	return sort_stories_by_votes(hn)


@click.command()
@click.option('--pages', default=1, help='Number of pages.')
def scrape_hn_webpage(pages):
	links, subtext = create_hn_links_and_subtext(pages)
	pprint(create_custom_hn(links,subtext))

if __name__=='__main__':
	scrape_hn_webpage()
