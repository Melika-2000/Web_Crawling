from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_categories(driver):
    elements = driver.find_elements(By.XPATH, "//div[@class='item']/a")[7:]
    categories = {}

    for element in elements:
        title = element.get_attribute('title')
        href = element.get_attribute('href')
        categories[title] = href

    return categories


def get_current_page_books_data(book_urls):
    books = []
    for book_num, book_url in enumerate(book_urls):
        # make a dictionary, which contains required information, for each book
        newBookInformation = {}
        driver.get(book_url)
        # get price
        price = driver.find_element(By.XPATH, "//*[@id=\"BookDetails\"]/div/div[2]/div/span")
        newBookInformation["price"] = price.text
        # get score
        scoreWidth = driver.find_element(By.XPATH,
                                         "/html/body/div[2]/div/main/div/article/div[1]/div[3]/a/div/div/div").get_attribute(
            "style")
        widthArray = scoreWidth.split()
        widthNum = float(widthArray[1].replace("px", "").replace(";", ""))
        score = "{:.2f}".format((widthNum * 5) / 90)
        newBookInformation["score"] = score
        # get all rows of the table containig some information about the book
        rows = driver.find_elements(By.XPATH, "//*[@id=\"BookDetails\"]/table/tbody/tr")
        # get columns of eah row and fill newBookInformation dictionary with them
        for i, row in enumerate(rows, 1):
            rowTitlePath = "//*[@id=\"BookDetails\"]/table/tbody/tr[" + str(i) + "]/td[1]"
            rowContentPath = "//*[@id=\"BookDetails\"]/table/tbody/tr[" + str(i) + "]/td[2]"
            rowTitle = driver.find_element(By.XPATH, rowTitlePath).text
            rowContent = driver.find_element(By.XPATH, rowContentPath).text
            match rowTitle:
                case "نام کتاب":
                    newBookInformation["title"] = rowContent
                case "نویسنده":
                    newBookInformation["writer"] = rowContent
                case "مترجم":
                    newBookInformation["translator"] = rowContent
                case "ناشر چاپی":
                    newBookInformation["printPublisher"] = rowContent
                case "ناشر صوتی":
                    newBookInformation["audioPublisher"] = rowContent
                case "سال انتشار":
                    newBookInformation["year_of_publication"] = rowContent
                case "موضوع کتاب":
                    newBookInformation["subject"] = rowContent
                case _:
                    pass
        # get the number of comments each book has
        try:
            comment_count = driver.find_element(By.CSS_SELECTOR, ".comment-count")
            newBookInformation["numberOfComments"] = comment_count.text
        except NoSuchElementException:
            newBookInformation["numberOfComments"] = 0

        print(newBookInformation)
        books.append(newBookInformation)
    return books


driver = initialize_driver()
driver.get("https://www.ketabrah.ir/")
categories = get_categories(driver)
all_books = []

for category in categories.keys():
    category_url = categories[category]
    driver.get(category_url)

    # navigating to popular page in the category
    populars_url = driver.find_element(By.XPATH, "//*[@id=\"InternalPageContents\"]/div[2]/a").get_attribute('href')
    driver.get(populars_url)

    # we fetch all the books in current page that are popular in the category
    book_urls = driver.find_elements(By.XPATH, "//div[@class='book-list']/div[@class=\"item\"]/a[1]")
    for i, url in enumerate(book_urls):
        book_urls[i] = url.get_attribute('href')
    current_page_books = get_current_page_books_data(book_urls)
    all_books = all_books + current_page_books


df = pd.DataFrame(all_books)
df.to_csv('output.csv', index=False, header=True)
driver.close()


