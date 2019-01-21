from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv, sys, time

class HyperionherbsHelper():

    def __init__(self):
        self.url = 'https://www.hyperionherbs.com/blog/'
        self.driver = webdriver.Chrome(executable_path='../utility/chromedriver.exe')

    # method to get items from given link.
    def getItems(self):
        items = []
        count = 0
        while True:
            count += 1
            try:
                self.driver.get(self.url)
                soup = BeautifulSoup(self.driver.page_source, u'html.parser')
                container = soup.find('div', attrs={'class': 'et_pb_salvattore_content'})
                articles = container.findAll('article')
                items.extend(articles)
                nxt_btn = self.driver.find_element_by_xpath("//div[@class='pagination clearfix']")
                if nxt_btn:
                    nxt_btn = nxt_btn.find_element_by_xpath('./div/a')
                    nxt_btn.click()
                    time.sleep(3)
                else:
                    break
            except:
                break
        # close driver session here
        self.driver.close()
        return items

    def getItemDtail(self, item):
        data = {}
        try:
            article_url = item.find('a')['href']
            print("article_url : "+article_url)
            res_article = requests.get(article_url)
            soup_article = BeautifulSoup(res_article.text, u'html.parser')
            try:
                article_title = soup_article.find('h1', attrs={'class': 'entry-title'})
                article_title = str(article_title.text).encode('utf-8').strip()
            except:
                article_title = None
            try:
                article_author = soup_article.find('span', attrs={'class': 'author vcard'})
                article_author = str(article_author.text).encode('utf-8').strip()
            except:
                article_author = None
            try:
                article_date = soup_article.find('span', attrs={'class': 'published'})
                article_date = str(article_date.text).encode('utf-8').strip()
            except:
                article_date = None
            try:
                description = soup_article.find('div', attrs={'class': 'entry-content'})
                description = str(description.text).encode('utf-8').strip()
            except:
                description = None
            data.update({'title': article_title})
            data.update({'author': article_author})
            data.update({'date': article_date})
            data.update({'description': description})
        except:
            pass

        return data

    # method to write csv file
    def writeCSVFile(self, data):
        try:
            with open('sample.csv', mode='w') as csv_file:
                fieldnames = ['title', 'author', 'date', 'description']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for d in data:
                    writer.writerow({'title': d['title'], 'author': d['author'], 'date': d['date'], 'description': d['description']})
                csv_file.close()
            print("File written successfully.")
        except:
            print(sys.exc_info())
            pass

    # method to start process.
    def start(self):
        items_data = []
        items = self.getItems()
        for item in items:
            data = self.getItemDtail(item)
            if len(data):
                items_data.append(data)
        
        # Going to write csv file if data here for writing.
        if len(items_data):
            self.writeCSVFile(items_data)


# main function call
if __name__ == "__main__":

    # objHH is an instance for HyperionherbsHelper
    objHH = HyperionherbsHelper()
    objHH.start()
