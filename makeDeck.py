#imports here
from selenium import webdriver
import re, json,requests,sys,copy,random,string,time
import sqlite3

#selnium stiff
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Crawler():
    driver = webdriver.Chrome()

    def __init__(self,url): #completed No need for rewrite
        """Initializes the data."""
        self.url = url
        self.Get()

    def returnSoup(self,url): #completed No need for rewrite
        resp = requests.get(url)
        http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(resp.content,'html.parser')
        return soup

    def Get(self): 
        Crawler.driver.get(self.url) 
        elements = Crawler.driver.find_elements_by_xpath("//a[@class='content-item grid-cell']")
        sites= []
        deck = []
        for element in elements:
            sites.append(element.get_attribute("href"))
        for i,v in enumerate(sites):    
            Crawler.driver.get(v) 
            unicodeName = Crawler.driver.find_element_by_xpath("//td[@id='unicodename']").text
            print(f"unicodename : {unicodeName}\n")
            unicodeNumber = Crawler.driver.find_element_by_xpath("//td[@id='unicodenumber']").text
            print(f"unicodenumber : {unicodeNumber}\n")
            htmlEnity = Crawler.driver.find_element_by_xpath("//td[@id='html-entity']").text
            print(f"html-entity : {htmlEnity}\n")
            deck.append(self.newCard(unicodeName,unicodeNumber,htmlEnity))
        print(deck)
        j = json.dumps(deck)
        with open('FullDeckOfCards.json','w') as f: 
           f.write(j)
           f.close()
        return (deck) 
        #next: remove null and empty : https://stackoverflow.com/questions/19167485/removing-json-property-in-array-of-objects

    def newCard(self,unicodeName,unicodeNumber,htmlEntity):
        regEx= r'(.+) of (.+)' 
        pattern = re.compile(regEx)
        matches = pattern.finditer(unicodeName)
        for match in matches:
            v = match.group(1)
            if v == "two": 
               cardValue = 2
            elif 'three' == v: 
               cardValue = 3
            elif 'four' == v: 
               cardValue = 4
            elif 'five' == v: 
               cardValue = 5
            elif 'six' == v: 
               cardValue = 6
            elif 'seven' == v: 
               cardValue = 7
            elif 'eight' == v: 
               cardValue = 8
            elif 'nine' == v: 
               cardValue = 9
            elif 'ten' == v: 
               cardValue = "T"
            elif 'jack' == v: 
               cardValue = "J"
            elif 'queen' == v: 
               cardValue = "Q"
            elif 'king' == v: 
               cardValue = "K"
            elif 'knight' == v: 
               cardValue = "knight"
            elif 'ace' == v: 
               cardValue = "A"
            else :
               cardValue = 'joker'
            card = {"cardValue" : cardValue, "cardSuit" : match.group(2),"unicodeNumber" : unicodeNumber, "htmlEntity" : htmlEntity}
            return(card) 


Crawler = Crawler('https://www.htmlsymbols.xyz/games-symbols/playing-cards')

