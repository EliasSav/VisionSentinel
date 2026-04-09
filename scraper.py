import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def extract_m3u8_streams(sitemap_url):
    """Extrage automat link-urile m3u8 active."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')

    camera_links =""
    for loc in soup.find_all('loc'):
        link = loc.text
        if not any(link.endswith(ext) for ext in ['.jpg', '.png']):
            camera_links.append(link)

    stream_urls = {}
    for page_url in camera_links[:10]:
        try:
            driver.get(page_url)
            time.sleep(3)

            page_source = driver.page_source
            html_soup = BeautifulSoup(page_source, 'html.parser')

            video_tag = html_soup.find('source', type='application/x-mpegURL')
            if video_tag and 'src' in video_tag.attrs:
                stream_urls[page_url] = video_tag['src']

        except Exception as e:
            continue

    driver.quit()
    return stream_urls