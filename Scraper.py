import re
import time
import requests
import json
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es_client = Elasticsearch(['http://localhost:9200'])

drop_index = es_client.indices.create(index='blogs', ignore=400)
create_index = es_client.indices.delete(index='blogs', ignore=[400, 404])

def urlparser(title, url):
    # scrape title
    p = {}
    post = title
    page = requests.get("https://www.practo.com/pune").content
    soup = BeautifulSoup(page, 'lxml')
    title_name = soup.title.string
    # scrape tags
    tag_names = ['Book Appointment Online','Covide-19_test','Dental Hospitals','X-Ray',
    'Allergist/immunologist','Ayurveda','Homoeopath','Dermatologist']
    desc = soup.findAll(attrs={"property":"article:tag"})
    
    for x in range(len(desc)):
        tag_names.append(desc[x-1]['content'])

    # payload for elasticsearch
    doc = {
        'date': time.strftime("%Y-%m-%d"),
        'title': title_name,
        'tags':json.dumps( tag_names),
        'url': url
        
    }
    print('---------------------------------------------------------------')
    print(doc)
    print('---------------------------------------------------------------')
    # ingest payload into elasticsearch
    res = es_client.index(index="blogs", doc_type="docs", body=doc)
    time.sleep(0.5)

sitemap_feed = 'http://a211431.sitemaphosting4.com/4165076/sitemap.xml'

page = requests.get(sitemap_feed)
sitemap_index = BeautifulSoup(page.content, 'html.parser')
urls = [element.text for element in sitemap_index.findAll('loc')]

for x in urls:
    urlparser(x, x)