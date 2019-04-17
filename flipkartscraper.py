from bs4 import BeautifulSoup
import requests

url = "https://www.flipkart.com/watches/titan~brand/pr?sid=r18"
r = requests.get(url)
xsoup = BeautifulSoup(r.content)
nav = xsoup.find("nav", attrs={"class": "_1ypTlJ"})
pages = nav.find_all("a", attrs={"class": "_2Xp0TH"})
links = [page['href'] for page in pages]
for i in links:
    res = requests.get("https://www.flipkart.com" + i)
    soup = BeautifulSoup(res.content)
    x = soup.find_all("div", attrs={"class": "_3O0U0u _288RSE"})
    lst = []
    for i in x:
        f1 = i.find_all("div", recursive=False)
        lst.extend(f1)
    for i in lst:
        ibrand = i.find("div", attrs={"class": "_2B_pmu"})
        if ibrand:
            print(ibrand.text)
            iname = ibrand.next_sibling
            print(iname.getText())
            iprice = i.find("div", attrs={"class": "_1vC4OE"})
            print(iprice.text)