import requests
from time import sleep
import json
from time import sleep
from bs4 import BeautifulSoup

def parse_beer_receipt(receipt_page):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    page = requests.get(receipt_page['url'], headers={'User-Agent': user_agent})
    soup = BeautifulSoup(page.content, 'html.parser')
    main_table = soup.find("div",attrs={'class':'full info-box'})
    record={}
    if main_table is not None:
        name = receipt_page['name']
        cat = main_table.find(attrs={'itemprop':'recipeCuisine'}).text
        ingredients_table = main_table.find("div", attrs={'itemprop':'ingredients'}).find_all({"li"})
        specs_table = main_table.find("ul", attrs={'class':'specs'}).find_all({"li"})
        intruction = main_table.find_all("div", attrs = {'itemprop':'recipeInstructions'})[0].text
            
        ingredients = [i.text for i in ingredients_table]
        specs = [i.text for i in specs_table]

        record = {
            'name': name,
            'category': cat,
            'ingredients':ingredients,
            'specifications':specs,
            'intruction':intruction
            }
    return(record) 

url_get = "https://www.homebrewersassociation.org/top-50-commercial-clone-beer-recipes/"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
urls = []

page = requests.get(url_get, headers={'User-Agent': user_agent})
soup = BeautifulSoup(page.content, 'html.parser')
main_table = soup.find("ul",attrs={'id':'cat_select'})    
links = main_table.find_all("a")
urls = [link['href'] for link in links]

receipt_urls = []
for url in urls:
    page = requests.get(url, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(page.content, 'html.parser')
    main_table = soup.find_all("div",attrs={'class':'beer'})
    for link in main_table:
        url = link.find("a")['href']
        name = link.find("a").text
        record = {
            'name':name,
            'url':url
        }
        receipt_urls.append(record)

receipt_records = []
for receipt_page in receipt_urls:
    print('Extracting data from %s'%receipt_page['url'])
    #Lets wait for 5 seconds before we make requests, so that we don't get blocked while scraping. 
    #if you see errors that say HTTPError: HTTP Error 429: Too Many Requests , increase this value by 1 second, till you get the data. 
    #sleep(5)
    receipt_records.append(parse_beer_receipt(receipt_page))
    #Lets wait for 10 seconds before we make requests, so that we don't get blocked while scraping
    #sleep(10)

#Lets write these to a JSON file for now. 
with open('data.json', 'w') as outfile:
    json.dump(receipt_records, outfile, indent=4)