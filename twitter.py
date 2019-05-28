# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import os, sys, time
import requests, json, csv
from datetime import datetime

class TwitterHelper():

    def __init__(self):
        self.main_url = "https://twitter.com"
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.today_date = datetime.today()

    # method to get Twitter data.
    def getTwitterData(self):
        items = []
        job_url = self.main_url + "/search?f=tweets&vertical=default&q=app%20developer&src=tyah"
        self.driver.get(job_url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        tweets = self.driver.find_elements_by_xpath("//ol[@id='stream-items-id']/li")
        print("Total tweets : ",len(tweets))
        if len(tweets):
            for tweet in tweets:
                try:
                    tweet_id = tweet.get_attribute("data-item-id")
                    author_name = tweet.find_element_by_xpath(".//span[@class='FullNameGroup']/strong")
                    if author_name:
                        author_name = str(author_name.text).encode("utf-8")
                    username = tweet.find_element_by_xpath(".//span[@class='username u-dir u-textTruncate']")
                    if username:
                        username = str(username.text).replace("@", '').strip()
                    author_img = tweet.find_element_by_xpath(".//img[@class='avatar js-action-profile-avatar']").get_attribute("src")
                    tweet_at = tweet.find_element_by_xpath(".//span[@class='_timestamp js-short-timestamp js-relative-timestamp']").text
                    # reply_to = tweet.find_element_by_xpath(".//div[@class='ReplyingToContextBelowAuthor']")
                    # if reply_to:
                    #     reply_to = reply_to.text
                    
                    tweet = tweet.find_element_by_xpath(".//div[@class='js-tweet-text-container']")
                    if tweet:
                        tweet = str(tweet.text).encode("utf-8")
                    author_url = self.main_url + "/" + str(username)
                    res = requests.get(author_url)
                    soup = BeautifulSoup(res.content, u'html.parser')
                    tweets = soup.find("a", attrs={"data-nav": "tweets"})
                    if tweets:
                        tweets = tweets.find("span", attrs={"class": "ProfileNav-value"})['data-count']
                    followings = soup.find("a", attrs={"data-nav": "following"})
                    if followings:
                        followings = followings.find("span", attrs={"class": "ProfileNav-value"})['data-count']
                    followers = soup.find("a", attrs={"data-nav": "followers"})
                    if followers:
                        followers = followers.find("span", attrs={"class": "ProfileNav-value"})['data-count']
                    favorites = soup.find("a", attrs={"data-nav": "favorites"})
                    if favorites:
                        favorites = favorites.find("span", attrs={"class": "ProfileNav-value"})['data-count']
                    lists = soup.find("a", attrs={"data-nav": "all_lists"})
                    if lists:
                        lists = lists.find("span", attrs={"class": "ProfileNav-value"}).text
                    else:
                        lists = ""

                    location = soup.find("div", attrs={"class": "ProfileHeaderCard-location"})
                    if location:
                        location = str(location.text).strip()
                    
                    items.append({
                        "tweet_id": tweet_id,
                        "author_name": author_name,
                        "author_img": author_img,
                        "username": username,
                        "tweet_at": tweet_at,
                        "tweet": tweet,
                        "tweets": tweets,
                        "followings": followings,
                        "followers": followers,
                        "favorites": favorites,
                        "lists": lists,
                        "location": location,
                    })
                except:
                    pass
         
        self.driver.close()
        return items

    # method to write csv file.
    def writeCSV(self, items):
         
        try:
            with open("twitter.csv", mode='w') as csv_file:
                fieldnames = ["Twitter Id", "Full Name", "Username", "Image", "Location", "Follwers", "Followings", "Favorites", "Lists", "Tweet", "Created At"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for item in items:
                    writer.writerow(
                        {
                            'Twitter Id': item['tweet_id'], 'Full Name': item['author_name'], 'Username': item['username'], 
                            'Image': item['author_img'], 'Location': item['location'], 'Follwers': item['followers'], 
                            'Followings': item['followings'], 'Favorites': item['favorites'], 'Lists': item['lists'], 
                            'Tweet': item['tweet'], 'Created At': item['tweet_at']
                        }
                    )
                csv_file.close()
            print("File written successfully.")
        except:
            print("Error occured during written file.")
            print(sys.exc_info())

    # method to start process.
    def start(self):
        items = self.getTwitterData()
        print("Total items : ",len(items))
        if len(items):
            self.writeCSV(items)
        else:
            print("Item not found.")
        print("#" * 100)

if __name__ == "__main__":

    # objTH is an instance for TwitterHelper.
    objTH = TwitterHelper()
    objTH.start()