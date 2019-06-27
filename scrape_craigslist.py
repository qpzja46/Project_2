from splinter import Browser
from bs4 import BeautifulSoup
import requests

def get_urls (search_topic, end_url):
    executable_path = {"executable_path": "../chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https:/chicago.craigslist.org/search/" + search_topic
    browser.visit(url)
    url_list = []

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results_per_page = soup.find('span', class_='rangeTo').text
    total_results = soup.find('span', class_='totalcount').text
    end_page = int(total_results)//int(results_per_page) + 1

    for current_page in range(1, end_page + 1):
        results = soup.find_all('li', class_='result-row')
        for result in results:
            link = result.find('a')['href']
            if link != end_url:
                url_list.append(link)
            else:
                current_page = end_page
                break

        if current_page < end_page:
            browser.click_link_by_partial_text('next')
            html = browser.html
            soup = BeautifulSoup(html, "html.parser")

    browser.quit()
    return url_list

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = (soup.find("span", class_="postingtitletext").find("span").get_text())

    image_urls = []
    images = soup.find_all("a", class_='thumb')
    for image in images:
        image_urls.append(image["href"])

    description = soup.find("section", id = "postingbody").find('div').next_sibling[1:]

    latitude = soup.find("div", id= "map")["data-latitude"]
    longitude = soup.find("div", id ="map")["data-longitude"]
    coordinates = [latitude,longitude]

    time_posted = soup.find("time", class_ = "date timeago")["datetime"]

    listing = {
        'title': title,
        'image_urls': image_urls,
        'description': description,
        'coordinates': coordinates,
        'craiglist_url': url,
        'time_posted': time_posted
    }
    return listing

def scrape_info(search_topic, end_url):
    scrape_data = []
    url_list = get_urls(search_topic, end_url)
    record_total = len(url_list)
    for n in range(0, record_total):
        scrape_data.append(scrape_page(url_list[n]))
        print(f'Scraping Page {n} of {record_total}')
    return scrape_data

