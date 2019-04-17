from selenium import webdriver
import sys
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path='D:\Software\chromedriver.exe')
driver.get("https://www.fossil.com/in/en/men/watches/view-all.pageNumber1.html")
try:
    a = driver.find_element_by_xpath("//a[@aria-label='next']")
    n , st= 32, 0
    nlist = []
    plist = []
    while True:
        a = driver.find_element_by_xpath("//a[@aria-label='next']")
        if a != None:
            soup = BeautifulSoup(driver.page_source)
            art = soup.find("article", attrs={"data-productlist-index": str(st)})
            while(art != None):
                name = art.find("a", attrs={"class": "link-product-result-path text-ellipsis"}).text
                price = art.find("span", attrs={"class": "text-price"}).text
                nlist.append(name)
                plist.append(price)
                print("{} : {}".format(name, price))
                art = art.find_next_sibling()
            st = n
            n = n*2
            a.click()
    print("Length of name: ", len(nlist))
    print("Length of price: ", len(plist))
except:
    print(sys.exc_info())
finally:
    driver.close()