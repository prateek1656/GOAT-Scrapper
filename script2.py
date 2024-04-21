from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import csv


def script2():
    base_url = "https://www.goat.com/"

    csv_file_path = 'link.csv'
    urls = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                urls.append(base_url + row[0])
            
    all_image_src_lists = []
    update_data = []
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=800x600")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--minimized")  
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
    
    with webdriver.Chrome(options=chrome_options) as driver:
        for url in tqdm(urls,desc="Processing URLs", unit="URL"):
            
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_element = soup.find('div', class_='swiper-wrapper')
            try:
                image_src_list = [img['src'] for img in div_element.find_all('img')]
            except AttributeError:
                image_src_list = []
            all_image_src_lists.append(image_src_list)
            
            try:
                name = soup.find('h1', class_="ProductInfo__Name-sc-yvcr9v-2 bMmuxU").text
            except:
                name = ""
            info_div_tags = soup.find_all(class_="XUSFT")

            try:
                release = info_div_tags[0].text
            except IndexError:
                release = ""
                
            try:
                sku = info_div_tags[1].text
            except IndexError:
                sku = ""
                
            try:
                nickname = info_div_tags[2].text
            except IndexError:
                nickname = ""
                
            try:
                colorway = info_div_tags[3].text
            except IndexError:
                colorway = ""
                
            try:
                color = info_div_tags[4].text
            except IndexError:
                color = ""
                
            try:
                upper_material = info_div_tags[5].text
            except IndexError:
                upper_material = ""
                
            try:
                technology = info_div_tags[6].text
            except IndexError:
                technology = ""
                
            try:
                category = info_div_tags[7].text
            except IndexError:
                category = ""
        
            sizes = []
            prices = []
            divs = soup.find_all('div', class_='SizeAndPrice__Root-sc-1w2dirf-0 kbeuwT')
            for div in divs:
                size_contents = div.find('div', class_="SizeAndPrice__Size-sc-1w2dirf-1 crstVY").text
                sizes.append(size_contents)
                offer_contents = div.find('div', class_= "OutOfStock__Root-sc-yu1qkl-0 iDYLqB")            
                price_contents = div.find('span', class_= "LocalizedCurrency__Amount-sc-yoa0om-0 jDDuev SizeAndPrice__Price-sc-1w2dirf-2 dfmgGG")
                if(price_contents):
                    prices.append(price_contents.text)
                else:
                    prices.append(offer_contents.text)
            
            image_urls_str = '\n'.join(image_src_list)
            update_data.append([url,image_urls_str, name, release, sku, nickname, colorway, category, color, upper_material, technology, ', '.join(sizes), ', '.join(prices)])

        csv_file_path = 'product-data.csv'
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(update_data)
            print(update_data)
        driver.quit()
