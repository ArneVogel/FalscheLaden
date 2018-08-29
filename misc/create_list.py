import json, requests
from bs4 import BeautifulSoup

manifest_location = "../falscheladen/manifest.json"

watchlist = "https://www.watchlist-internet.at/news/liste-betruegerischer-online-shops/"
warnungen = "https://www.onlinewarnungen.de/warnungsticker/warnung-vor-onlineshops-hier-duerfen-sie-nicht-einkaufen/"

#https://verbraucherschutz.de/fake-shops-2018-juli/
schutz = "https://verbraucherschutz.de/fake-shops-"
years = ["2017", "2018"]
months = [x.lower() for x in ["Januar", "Februar", "Maerz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]]

def create_matching(domain):
    domain = domain.split("(")[0]
    domain = domain.replace(" ", "")
    if "co.uk" in domain:
        domain = ".".join(domain.split(".")[-3:])
    else:
        domain = ".".join(domain.split(".")[-2:])
    return '*://*.' + domain + '/*'

def get_watchlist_domains(url):
    domains = set()
    filter_list = ["Genannt werden", "<strong>", "Die Prüfung", "Die Aufzählung"]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for div in soup.findAll("div", class_="article-content"):
        for p in div.findAll("p"):
            if not any (f in str(p) for f in filter_list):
                p = str(p)
                p = p.replace("<p>", "")
                p = p.replace("</p>", "")
                links = p.split("<br/>")
                for link in links:
                    l = link.split(" (")[0]
                    l = l.replace(" ", "")
                    domains.add(l)
    return domains

def get_warnungen_domains(url):
    domains = set()
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for li in soup.findAll("li"):
        if " | " in str(li) and "<a" not in str(li):
            li = str(li)
            li = li.split(" ")[0]
            li = li.replace("<li>", "")
            li = li.replace(" ", "")
            li = li.replace("|", "")
            domains.add(li)
    return domains

def get_schutz_domains(url):
    domains = set()
    r = requests.get(url)
    if r.status_code is not 200:
        return domains
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find("div", class_="entry-content")
    p = div.find("p")
    p = str(p)
    p = p.replace("<p>", "")
    l = p.split("<br/>")
    for link in l:
        link = link.replace("\n", "")
        domains.add(link.split(" ")[0])
    return domains

with open(manifest_location) as f:
    data = json.load(f)

fake_shops = set()
fake_shops = fake_shops.union(get_warnungen_domains(warnungen))
fake_shops = fake_shops.union(get_watchlist_domains(watchlist))
for year in years:
    for month in months:
        url = "" + schutz + year + "-" + month + "/"
        fake_shops = fake_shops.union(get_schutz_domains(url))
    
# ['*://*.mozilla.org/*', '*://*.wikipedia.org/*']
fake_shop_list = list()
for fs in fake_shops:
    fake_shop_list.append(create_matching(fs))
    
data["content_scripts"][0]["matches"] = fake_shop_list

with open(manifest_location, 'w') as f:
    json.dump(data, f,sort_keys = True, indent = 4,
               ensure_ascii = False)