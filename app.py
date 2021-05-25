from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/Admin/Downloads/chromedriver_win32/chromedriver")
browser.get(START_URL)
time.sleep(10)

new_planet_data=[]
planet_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type","planet_radius","orbital-radius","orbital_period","eccentricity"]
def scrape():
    
    
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)
        
    # with open("scrapper_2.csv", "w") as f:
    #     csvwriter = csv.writer(f)
    #     csvwriter.writerow(headers)
    #     csvwriter.writerows(planet_data)
scrape()

def scrapemoredata(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all('tr',attrs={'class','fact_row'}):
        td_tag=tr_tag.find_all('td')
        temp_list=[]
        for tdtag in td_tag:
            try:
                temp_list.append(tdtag.find_all('div',attrs={'class','value'})[0].contents[0])
            except:
                temp_list.append('')
        new_planet_data.append(temp_list)

for data in planet_data:
    scrapemoredata(data[5])

final_planet_data=[]

for index,data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])

with open('apeksha.csv','w') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)
