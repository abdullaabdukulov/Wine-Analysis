import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import numpy as np


def get_site(url):
    """
        this function sends a get request
        to the website and get its response.
        parameters :
            url : url of the website
        returns :
            response of the get request of the url.
    """
    # send a get request and get the response
    response = requests.get(url)

    # return the response
    return response


# scrap all wine region links
def get_all_country_urls(page):
    """
       this function retrieves 
       country links from wine sites.
        parameters :
            page : 	response of the get request to the Wine page
        returns :
			nothing.
			(just making a .json file)
    """

    # make a beautifulsoup object using the html of the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # getting all rows related to country links
    data = soup.find_all('a', class_='filterMenu_itemLink')[5:35]
    result = {}
    for a in data:
        url = a['href'][:-23]
        country = ''.join(c for c in a.text if c.isalpha())
        result[country] = url
    # Serializing json
    json_object = json.dumps(result, indent=4)

    # Writing to countys_url.json
    with open("data/countys_url.json", "w") as outfile:
        outfile.write(json_object)
    print('Successfuly')


def get_wine_data(file, wine_url):
    """
       This function collects data for the columns "Name, Country, Varietal, wine_type, Rating, NumberOfRatings, Year,Price$"

        parameters :
            file : 	json links corresponding to all rows belonging to each country
            wine_url: url of the website
        returns :
			nothing.
			(just making a .json file)
    """

    # Opening JSON file
    with open(file, 'r') as openfile:
        # Reading from json file
        json_objects = json.load(openfile)
    errors = 0
    delimiters = ' ', '\n', '-', '.', '(', ')', ','
    regexPattern = '|'.join(map(re.escape, delimiters))
    collects = {}
    all_data = [['Name', 'Country', 'Varietal', 'Wine type', 'Rating', 'NumberOfRatings', 'Year', 'Price$']]
    for country, url in json_objects.items():
        request = requests.get(wine_url + url)
        for a in range(1, 25):
            if a > 1:
                request = requests.get(wine_url + url + '/' + str(a))
                soup = BeautifulSoup(request.text, 'html.parser')
                find_data = soup.find_all('div', class_='prodItemInfo')
                for i in find_data:
                    clean = [d.strip() for d in i.get_text().strip().split('\n') if len(d.strip()) > 0][:-7]
                    if clean:
                        pass
                    else:
                        break
                    try:
                        l = re.split(regexPattern, clean[1])
                        index_spl = l.index('from')
                        varietal = ' '.join(l[:index_spl])
                    except:
                        varietal = 'Not available'
                    try:
                        clean.append(i.find('ul', class_='prodAttr').li['title'])
                        # print(i.find('ul', class_='prodAttr').li['title'])
                    except TypeError:
                        clean.append('Not available')
                    name, wine_type, year = clean[0], clean[-1], ''.join(
                        'Not available' if len([a for a in clean[0][-5:] if a.isnumeric()]) < 2 else clean[0][-5:])
                    for j in clean:
                        o = 0
                        try:
                            if j[1] == '.':
                                raiting_average = j
                                o += 1
                        except:
                            raiting_average = np.nan
                            o += 1
                        try:
                            if j[-7:] == 'Ratings':
                                average_raiting_count = j.split()[0]
                                o += 1
                        except:
                            average_raiting_count = np.nan
                            o += 1
                        try:
                            if j[0] == '$':
                                price = j[1:]
                                o += 1
                        except:
                            price = np.nan
                            o += 1

                        if o > 4:
                            break
                    collect.append(name)
                    collect.append(country)
                    collect.append(varietal)
                    collect.append(wine_type)
                    collect.append(raiting_average)
                    collect.append(average_raiting_count)
                    collect.append(year)
                    collect.append(price)
                    all_data.append(collect)
                    collect = []
            else:
                soup = BeautifulSoup(request.text, 'html.parser')
                find_data = soup.find_all('div', class_='prodItemInfo')
                for i in find_data:
                    collect = []
                    clean = [d.strip() for d in i.get_text().strip().split('\n') if len(d.strip()) > 0][:-7]
                    try:
                        l = re.split(regexPattern, clean[1])
                        index_spl = l.index('from')
                        varietal = ' '.join(l[:index_spl])
                    except:
                        varietal = np.nan
                    try:
                        clean.append(i.find('ul', class_='prodAttr').li['title'])
                        # print(i.find('ul', class_='prodAttr').li['title'])
                    except TypeError:
                        clean.append('Not available')
                    name, wine_type, year = clean[0], clean[-1], ''.join(
                        'Not available' if len([a for a in clean[0][-5:] if a.isnumeric()]) < 2 else clean[0][-5:])
                    for j in clean:
                        o = 0
                        try:
                            if j[1] == '.':
                                raiting_average = j
                                o += 1
                        except:
                            raiting_average = np.nan
                        try:
                            if j[-7:] == 'Ratings':
                                average_raiting_count = j.split()[0]
                                o += 1
                        except:
                            average_raiting_count = np.nan
                        try:
                            if j[0] == '$':
                                price = j[1:]
                                o += 1
                        except:
                            price = np.nan
                            o += 1

                        if o > 4:
                            o = 0
                            break
                    collect.append(name)
                    collect.append(country)
                    collect.append(varietal)
                    collect.append(wine_type)
                    collect.append(raiting_average)
                    collect.append(average_raiting_count)
                    collect.append(year)
                    collect.append(price)
                    all_data.append(collect)
                    collect = []
    with open('data/vivino.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_data)
    print('Successfuly')


def _main_collect_data():
    # URL of the website
    url = 'https://www.wine.com/list/wine/7155?sortBy=mostInteresting'

    # get the response
    page = get_site(url)

    # json links corresponding to all rows belonging to each country
    get_all_country_urls(page)

    # URL of the website
    wine_url = 'https://www.wine.com'

    # collects and writes wine values matching all strings
    get_wine_data('data/countys_url.json', wine_url)


_main_collect_data()
