import requests
from bs4 import BeautifulSoup
import json
def extract_basic_info(url):
    tags = ['foundations-ai','computer-science','artificial-intelligence','machine-learning','data-science', 'artificial-intelligence-and-machine-learning']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    information = {}
    for tag in tags:
        i = 0
        while True:
            url_new = f"{url}/tags/{tag}"
            r = requests.get(url_new, headers=headers,params={'page':i})
            soup = BeautifulSoup(r.text, 'html.parser')

            people = soup.select('article.vm-teaser')
            if not people:
                break
            for person in people:
                name_tag = person.select_one('h3.vm-teaser__title a')
                name = name_tag.text.strip()
                if name_tag['href'].startswith('/news'):
                    continue
                url_person = url + name_tag['href']
                websites = [a['href'] for a in person.select('li.icon--web a[href]')] # multiple websites
                email_tag = person.select_one('li.icon--envelope a')
                if not name or not url_person:
                    continue
                email = email_tag.text.strip() if email_tag else None
                if name not in information:
                    information[name] = {'profile_url': url_person, 'tag': [tag], 'websites': websites, 'email': email}
                else:
                    information[name]['tag'].append(tag)
            i += 1
    return information
def extract_descriptions(url, information):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for names in information:
        url = information[names]['profile_url']
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        desc_tag = soup.select_one('div.field--type-text-with-summary').get_text('\n',strip=True)
        desc_tag = desc_tag[3:] if desc_tag.startswith('Bio') else desc_tag
        information[names]['description'] = desc_tag
        


    return information
if __name__ == "__main__":
    url = "https://cs.ucdavis.edu"
    info = extract_descriptions(url, extract_basic_info(url))
    with open('basic_info.json', 'w') as f:
        json.dump(info, f, indent=4)