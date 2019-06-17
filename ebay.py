# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import os, sys, time, random
import requests, json, csv
from datetime import datetime

class EbayHelper():
    nlist = []
    plist = []
    def __init__(self):
        self.main_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=shirts&_sacat=0"
        self.driver = webdriver.Chrome(executable_path=r'D:\Software\chromedriver.exe')
        self.driver.get(self.main_url)
        self.soup = BeautifulSoup(self.driver.page_source)


    # method to get Ebay data.
    def getEbayData(self):
        li1 = self.soup.find("li", attrs={"data-view": "mi:1686|iid:1"})
        nxtbtn = self.driver.find_element_by_xpath("//*[@id='srp-river-results-SEARCH_PAGINATION_MODEL_V2']/div[2]/nav/a[2]")
        try:
            while(True):
                while(li1.next_sibling):    
                    name = li1.find("h3", attrs={"class": "s-item__title"}).text
                    price = li1.find("span", attrs={"class": "s-item__price"}).text
                    print("{} : {}".format(name, price))
                    EbayHelper.nlist.append(name)
                    EbayHelper.plist.append(price)
                    li1 = li1.next_sibling
                time.sleep(random.randint(3,5))
                nxtbtn.click()
        finally:
            self.driver.close()
            nl, pl = EbayHelper.nlist, EbayHelper.plist
            return nl, pl
            
    # method to write csv file.
    def writeCSV(self,nl,pl):        
        try:
            with open("ebay.csv", mode='a') as csv_file:
                fieldnames = ["Name", "Price"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i,j in zip(nl, pl):
                    writer.writerow(
                        {
                            'Name': i, 'Price': j
                        }
                    )
                csv_file.close()
            print("File written successfully.")
        except:
            print("Error occured during written file.")
            print(sys.exc_info())

    # method to start process.
    def start(self):
        nl, pl = self.getEbayData()
        self.writeCSV(nl,pl)
if __name__ == "__main__":

    # objTH is an instance for EbayHelper.
    objTH = EbayHelper()
    objTH.start()