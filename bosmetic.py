# -*- coding: utf-8 -*-

from selenium import webdriver
import requests
import sys, csv, time
from bs4 import BeautifulSoup

class BosmeticHelper():

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver")
        self.urls = [
             'https://www.bosmetic.co.il/category/547-%D7%97%D7%99%D7%A1%D7%95%D7%9C-%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%99%D7%95%D7%A4%D7%99',
             'https://www.bosmetic.co.il/prices-drop',
             'https://www.bosmetic.co.il/category/544-%D7%90%D7%95%D7%95%D7%99%D7%A8%D7%94-%D7%9C%D7%91%D7%99%D7%AA',
             'https://www.bosmetic.co.il/category/527-%D7%9C%D7%99%D7%99%D7%A3-%D7%A1%D7%98%D7%99%D7%99%D7%9C',
             'https://www.bosmetic.co.il/category/488-%D7%A9%D7%A2%D7%95%D7%A0%D7%99%D7%9D',
             'https://www.bosmetic.co.il/category/436-%D7%98%D7%99%D7%A4%D7%95%D7%97',
             'https://www.bosmetic.co.il/category/347-%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%A9%D7%99%D7%A2%D7%A8',
             'https://www.bosmetic.co.il/category/433-%D7%A7%D7%95%D7%A1%D7%9E%D7%98%D7%99%D7%A7%D7%94',
             'https://www.bosmetic.co.il/category/333-%D7%90%D7%99%D7%A4%D7%95%D7%A8'
         ]

    # method to get products by selenium + python
    def getProducts(self):
        products = []
        for url in self.urls:
            self.driver.get(url)
            self.driver.execute_script("window.scrollTo(0, 3000);")
            time.sleep(3)
            items=self.driver.find_elements_by_xpath('//ul[@class="product_list grid row"]/li')
            count=0
            for item in items:
                count=count+1
                data = {}
                try:
                    product_name=item.find_element_by_xpath('.//a[@class="product-name"]')
                    product_name = product_name.text
                    img_url = item.find_element_by_xpath(".//img[contains(@class,'replace-2x img-responsive lazy img_0 img_1e')]")
                    img_url=img_url.get_attribute("src")
                    try:
                        rating = item.find_element_by_xpath('.//div[@class="yotpo-bottomline pull-left  star-clickable"]')
                        rating=rating.text
                    except:
                        rating=0
                    product_url = item.find_element_by_xpath('.//a[@class="product-name"]')
                    product_url=product_url.get_attribute("href")
                    res = requests.get(product_url)
                    soup = BeautifulSoup(res.content, u'html.parser')
                    description = soup.find('div', attrs={'id': 'short_description_content'})
                    price = soup.find('span', attrs={'id': 'our_price_display'})
                    price=price.text
                    short_discription = soup.find('p', attrs={'class': 'clearfix align_justify'})
                    short_discription=short_discription.text
                    barcode = soup.find('p', attrs={'id': 'product_reference'})
                    barcode=barcode.text
                    if description:
                        description = description.text

                    data.update({'type': 'simple'})
                    data.update({'sku': barcode})
                    data.update({'name': product_name})
                    data.update({'published': '1'})
                    data.update({'short_discription': short_discription})
                    data.update({'description': description})
                    data.update({'in_stock': '1'})
                    data.update({'stock': '500'})
                    data.update({'regular_price': price})
                    data.update({'rating': rating})
                    data.update({'img_url': img_url})
                    products.append(data)
                except:
                    pass

        self.driver.close()
        return products

    # method to write CSV file.
    def writeCSV(self,products):
        with open("bosmetss1.csv", mode='w', encoding="utf-8", newline='') as csv_file:
            fieldnames=['Type', 'Sku', 'Name','Published','Short description','Description','In_stock','stock','Rating','Regular price','Image']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(
                    {
                        'Type': product['type'], 'Sku': product['sku'],
                        'Name': product['name'], 'Published': product['published'],
                        'Short description': product['description'], 'Description':product['short_discription'],
                        'In_stock': product['in_stock'], 'stock':product['stock'], 'Rating':product['rating'], 'Regular price':product['regular_price'],
                        'Image':product['img_url']
                    }
                )
            csv_file.close()
        print("File written successfully.")

    def start(self):
        products = self.getProducts()
        print("Total",len(products))
        if len(products):
            self.writeCSV(products)
        else:
            print("Product not found.")

        print("#" * 100)

if __name__ == "__main__":
    # objBH is an instance for BosmeticHelper
    objBH = BosmeticHelper()
    objBH.start()



