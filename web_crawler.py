import requests
from bs4 import BeautifulSoup

def get_links(url, domain):
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = set()
    links.add(url)
    av_links = soup.find_all('a')
    for link in av_links:
        new_link = link.get('href')
        if 'http' not in new_link and '+' not in new_link and 'mailto' not in new_link:
          new_link = domain + new_link
          links.add(new_link)
        elif domain in new_link:
          links.add(new_link)
    return links
  except ConnectionError:
    print('Please check your internet connection')


def get_data_url(url, domain):
  links = get_links(url, domain)
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title').text
  except AttributeError:
    title = "There is no Title on the page"
  site = {
      'title': title,
      'links': links
  }
  return site

def site_map(url):
  site_map = {}
  links = get_links(url, url)
  for link in links:
    data = get_data_url(link, url)
    site_map[link] = data
  return site_map
