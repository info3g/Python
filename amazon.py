# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import os, sys, time, random
import requests, json, csv
from datetime import datetime

class AmazonHelper():
    nlist = []
    plist = []
    def __init__(self):
        self.main_url = "https://www.amazon.in/s?k=shirts&ref=nb_sb_noss_2"
        self.driver = webdriver.Chrome(executable_path=r'D:\Software\chromedriver.exe')
        self.driver.get(self.main_url)
        self.soup = BeautifulSoup(self.driver.page_source)


    # method to get Amazon data.
    def getAmazonData(self):
        time.sleep(random.randint(5,8))
        r2ele = self.soup.find("div", attrs={"class": "s-result-list s-search-results sg-row"})
        r2ele1 = r2ele.find("div", attrs={"class": "sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32"})
        nxtbtn = self.driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[7]/div/div/div/ul/li[7]/a")
        try:
            while(nxtbtn):
                while(r2ele1):    
                    name = r2ele1.find("span", attrs={"class": "a-size-base-plus a-color-base a-text-normal"}).text
                    price = r2ele1.find("span", attrs={"class": "a-price-whole"}).text
                    if(name and price):
                        print("{} : Rs. {}".format(name,price))
                        AmazonHelper.nlist.append(name)
                        AmazonHelper.plist.append(price)
                    else:
                        break
                    r2ele1 = r2ele1.next_sibling.next_sibling
                nxtbtn = self.driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[7]/div/div/div/ul/li[7]/a")
                nxtbtn.click()
        finally:
            self.driver.close()
            nl, pl = AmazonHelper.nlist, AmazonHelper.plist
            return nl, pl

    # method to write csv file.
    def writeCSV(self, nl, pl):        
        try:
            with open("amazon.csv", mode='a') as csv_file:
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
        nl, pl = self.getAmazonData()
        self.writeCSV(nl, pl)
if __name__ == "__main__":

    # objTH is an instance for AmazonHelper.
    objTH = AmazonHelper()
    objTH.start()
