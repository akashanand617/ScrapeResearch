import requests
from bs4 import BeautifulSoup
import json
def extract_basic_info_cs(url):
    tags = ['foundations-ai','computer-science','artificial-intelligence','machine-learning','data-science', 'artificial-intelligence-and-machine-learning','software-engineering','database-systems']
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
def extract_basic_info_stat(url):
    i = 0
    information = {}
    while True:
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        r = requests.get(url + "/people",params={'page':i,'first':'','last':'','title':'','unit':'','field_sf_person_type_target_id[]':26}, headers = header)
        soup = BeautifulSoup(r.text, 'html.parser')
        people = soup.select('article.vm-teaser')
        if not people:
            break
        for person in people:
            name_tag = person.select_one('h3.vm-teaser__title a')
            name = name_tag.text.strip()
            for j in range(len(name)):
                if name[j] == ',':
                    name = name[:j]
                    break
            
            url_person = url + name_tag['href']
            websites = [a['href'] for a in person.select('li.icon--web a[href]')] # multiple websites
            email_tag = person.select_one('li.icon--envelope a')
            if not name or not url_person:
                continue
            email = email_tag.text.strip() if email_tag else None
            information[name] = {'profile_url': url_person, 'websites': websites, 'email': email, 'tag': ['statistics']}
        i += 1
    return information
def extract_descriptions(information):
    delete_names = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for names in information:
        url = information[names]['profile_url']
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        desc_tag = soup.select_one('div.field--type-text-with-summary')
        if desc_tag:
            desc_tag = desc_tag.get_text('\n',strip=True)
            desc_tag = desc_tag[3:] if desc_tag.startswith('Bio') else desc_tag
        else:
            desc_tag = None
        information[names]['description'] = desc_tag
        if not desc_tag and not information[names]['websites']:
            delete_names.append(names)

    for name in delete_names:
        del information[name]

    return information

if __name__ == "__main__":
    url_cs = "https://cs.ucdavis.edu"
    url_stat = "https://statistics.ucdavis.edu"
    info = extract_descriptions(extract_basic_info_cs(url_cs)) | extract_descriptions(extract_basic_info_stat(url_stat))
    print(len(info))
    with open('basic_info.json', 'w') as f:
        json.dump(info, f, indent=4)