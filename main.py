from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.ketabrah.ir/")

elements = driver.find_elements(By.XPATH, "//div[@class='item']/a")[7:]
categories = {}

for element in elements:
    title = element.get_attribute('title')
    href = element.get_attribute('href')
    categories[title] = href

for i, title in enumerate(categories.keys(),1):
    print(i, title)

title_index = int(input('please select one category: '))
selected_category_title = list(categories.keys())[title_index-1]
selected_category_url = categories[selected_category_title]

driver.get(selected_category_url)
populars_url = driver.find_element(By.XPATH, "//*[@id=\"InternalPageContents\"]/div[2]/a").get_attribute('href')
driver.get(populars_url)

book_urls = driver.find_elements(By.XPATH, "//div[@class='book-list']/div[@class=\"item\"]/a[1]")

for i, url in enumerate(book_urls):
    book_urls[i] = url.get_attribute('href')

for book_url in book_urls:
    driver.get(book_url)
    book_info = driver.find_elements(By.XPATH, "//*[@id=\"BookDetails\"]/table/tbody/tr")
    for data in book_info:
        print(data.get_attribute('innerHTML'))

driver.close()