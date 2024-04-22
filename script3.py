from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.goat.com/sneakers/air-jordan-4-retro-gs-white-oreo-dj4699-100")

soup = BeautifulSoup(driver.page_source, 'html.parser')


try:
	priceList = []
	price_div = soup.find_all('tr',class_="VariantPriceListItem__Root-sc-176ttgl-0 bMEivA")
	for div in price_div:
		price = div.find('span', class_= "LocalizedCurrency__Amount-sc-yoa0om-0 jDDuev").text
		span_tag = div.find('span', class_='product_variant_condition')
		if span_tag:
			condition = span_tag.text if not span_tag.find('svg') else "instant"
		else:
			condition = "instant"
		priceList.append(f"{condition} -> {price}")
except IndexError:
	priceList=[]

print(priceList)