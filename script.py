from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def script1(url):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.goat.com/search?query={url}")

    scroll_to_bottom(driver)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    div_element = soup.find('div', class_='SearchGrid__Wrapper-sc-1f53xpk-5 edXWKf')
    links = [link.get('href') for link in div_element.find_all('a')]

    data = [[link] for link in links]
    
    driver.quit()
    # service.stop()
    
    csv_file_path = 'link.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
