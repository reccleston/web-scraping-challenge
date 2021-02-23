import pandas as pd
import time
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def main():
    return scrape()

def startSplinter(url):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    return browser

def scrapeMarsHemispheres():
    browser = startSplinter('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    hemisphere_image_urls = []

    for i in range(0,4):
        browser.find_by_css('.thumb')[i].click() # clicks on hemisphere button on Homepage

        # Image page actions 
        browser.find_by_text('Open').click()
        img_page_html = browser.html
        img_page_soup = BeautifulSoup(img_page_html, 'html')
        img = img_page_soup.find_all('img', class_='wide-image')[0]
        title = img_page_soup.find('h2', class_='title').text.strip(' Enhanced') + 'e'
        img_url = 'https://astrogeology.usgs.gov' + img['src']

        hemisphere_image_urls.append({title: img_url})
        browser.back()
    browser.quit()
    return hemisphere_image_urls

def scrapeMarsFacts():
    mars_facts_table = pd.read_html('https://space-facts.com/mars/')[0]
    mars_facts_table.iloc[:,0] = mars_facts_table.iloc[:,0].str.strip(':')
    mars_facts_table = mars_facts_table.rename(columns={0: 'Fact Topics', 1: 'Fact Value'})
    mars_facts_table_html = mars_facts_table.to_html().replace('\n', '')
    return mars_facts_table_html

def scrapedFeatureImage():
    browser = startSplinter('https://www.jpl.nasa.gov/images?query=mars')
    browser.find_by_css('.text-theme-red')[1].click() # finds and clicks the 'SORT BY' menu
    browser.find_by_tag('option')[2].click() # finds and clicks the 'LATEST' option
    browser.find_by_css('.SearchResultCard').first.click() # finds and clicks first/featured image
    time.sleep(2) # allows page to load, lest error 
    featured_img_html = browser.html
    img_soup = BeautifulSoup(featured_img_html, 'lxml')
    featured_img_url = img_soup.find_all('img', class_='BaseImage object-scale-down')[0]['data-src']
    browser.quit()
    return featured_img_url

def scrapeNASAArticles():
    nasa_results = {'news_titles': [],
                    'p_text': []}
    browser = startSplinter('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
  
    html = browser.html
    pg_soup = BeautifulSoup(html, 'html')
    articles = pg_soup.find_all('div', class_='list_text')
    for article in articles:
        try: 
            nasa_results['news_titles'].append(article.find('div', class_='content_title').text.strip())
            nasa_results['p_text'].append(article.find('div', class_='article_teaser_body').text.strip())
        except AttributeError:
            print('Nothing to add apparently!')
    browser.quit()
    return nasa_results

def scrape():
    nasa_article_results = scrapeNASAArticles()
    featured_image_url = scrapedFeatureImage()
    mars_facts_table = scrapeMarsFacts()
    hemisphere_image_urls = scrapeMarsHemispheres()
    return [nasa_article_results, featured_image_url, mars_facts_table, hemisphere_image_urls]

if __name__ == '__main__':
	main() 