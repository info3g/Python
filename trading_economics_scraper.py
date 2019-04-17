from selenium import webdriver
import sys

driver = webdriver.Chrome(executable_path="D:\Software\chromedriver.exe")
driver.get("https://tradingeconomics.com/country-list/gdp-growth-rate")
try:
    tb = driver.find_element_by_xpath("//table[@class='table table-hover']")
    td = tb.find_elements_by_xpath(".//tbody/tr")
    for i in td:
        cntry = i.find_element_by_xpath(".//a").text
        last = i.find_element_by_xpath(".//td[@data-value]").text
        year = i.find_element_by_xpath(".//td[@style='text-align: right;']/span").text
        previous = i.find_element_by_xpath(".//td[@class='hidden-sm hidden-xs']").text
        rng = i.find_element_by_xpath(".//td[@class='hidden-sm hidden-xs' and @style='text-align: center;']").text
        print("{}  {}  {}  {}  {}".format(cntry, last, year, previous, rng))
except:
    print("An Exception occured")
    print(sys.exc_info())
driver.close()