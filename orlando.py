from selenium import webdriver
import requests
import sys, time, csv
from bs4 import BeautifulSoup

class OrlandoHelper():

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver")
        self.urls = [
            'https://www.orlando.co.il/product-category/4men/',
            'https://www.orlando.co.il/product-category/4women/',
            'https://www.orlando.co.il/product-category/hot-products/',
            'https://www.orlando.co.il/product-category/michael-kors/',
            'https://www.orlando.co.il/product-category/emporio-armani/',
            'https://www.orlando.co.il/product-category/burberry/',
            'https://www.orlando.co.il/product-category/tissot/',
            'https://www.orlando.co.il/product-category/daniel-wellington/',
         ]

    # method to get products by selenium + python
    def getProducts(self):
        products = []
        for url in self.urls:
            self.driver.get(url)
            while True:
                try:
                    items=self.driver.find_elements_by_xpath('//ul[@class="product-category-list products products-grid small-block-grid-2 medium-block-grid-3 large-block-grid-4 xlarge-block-grid-4 xxlarge-block-grid-4 columns-4 product-layout-grid"]/li')
                    for item in items:
                        data = {}
                        try:
                            img_url = item.find_element_by_xpath(".//img[contains(@class,'attachment-shop_catalog size-shop_catalog wp-post-image')]")
                            img_url=img_url.get_attribute("src")

                            product_url = item.find_element_by_xpath('.//a[@class="product-title-link"]')
                            product_url=product_url.get_attribute("href")
                            res = requests.get(product_url)
                            soup = BeautifulSoup(res.content, u'html.parser')
                            product_name = soup.find('h1', attrs={'class':'product_title entry-title'})
                            product_name = product_name.text
                            rating =  soup.find('div', attrs={'class':'star-rating'})
                            rating = rating.text
                            short_description = soup.find('div', attrs={'class': 'woocommerce-product-details__short-description'})
                            short_description=short_description.text
                            price = soup.find('p', attrs={'class': 'price'})
                            price=price.text
                            discription = soup.find('div', attrs={'class': 'woocommerce-product-details__short-description'})

                            if discription:
                                discription = discription.text
                            data.update({'name': product_name})
                            data.update({'Regular_price': price})
                            data.update({'img_url': img_url})
                            data.update({'rating': rating})
                            data.update({'discription': discription})
                            data.update({'sku': ''})
                            data.update({'short_discription': short_description})
                            data.update({'Type':'simple'})
                            data.update({'Published': '1'})
                            data.update({'In_stock': '1'})
                            data.update({'stock': '500'})
                            products.append(data)
                        except:
                            print(sys.exc_info())

                    next_page = self.driver.find_element_by_xpath("//a[@class='next page-numbers']")
                    if next_page:
                        next_page.click()
                        time.sleep(2)
                    else:
                        break
                except:
                    break
        self.driver.close()
        return products

    # method to write csv file.
    def writeCSV(self, products):
        with open("orlando.csv", mode='w', encoding="utf-8", newline='') as csv_file:
            fieldnames = ['Type', 'Sku', 'Name', 'Published', 'Short description', 'Description', 'In_stock', 'stock',
                          'Rating', 'Regular price',
                          'Image']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(
                    {
                        'Type': product['Type'], 'Sku': product['sku'], 'Name': product['name'], 'Published': product['Published'],
                        'Description': product['discription'], 'Short description': product['short_discription'], 'In_stock': product['In_stock'], 
                        'stock': product['stock'], 'Rating': product['rating'], 'Regular price': product['Regular_price'], 'Image': product['img_url']
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
    # objOH is an instance for OrlandoHelper
    objOH = OrlandoHelper()
    objOH.start()



