import requests
from bs4 import BeautifulSoup
import pprint

# get the information using requests
res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/?p=2')

# parse the information. convert from a string to html data. creates a soup object.
soup = BeautifulSoup(res.text, 'html5lib')
soup2 = BeautifulSoup(res2.text, 'html5lib')
cu_links = soup.select('.titleline')
cu_links2 = soup2.select('.titleline')
cu_subtext = soup.select('.subtext')
cu_subtext2 = soup2.select('.subtext')

mega_links = cu_links + cu_links2
mega_subtext = cu_subtext + cu_subtext2


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.find('a').get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'heading': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))
