from selenium import webdriver
from selenium.common import NoSuchElementException
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

for i, title in enumerate(categories.keys(), 1):
    print(i, title)

title_index = int(input('please select one category: '))
selected_category_title = list(categories.keys())[title_index - 1]
selected_category_url = categories[selected_category_title]

driver.get(selected_category_url)
populars_url = driver.find_element(By.XPATH, "//*[@id=\"InternalPageContents\"]/div[2]/a").get_attribute('href')
driver.get(populars_url)

book_urls = driver.find_elements(By.XPATH, "//div[@class='book-list']/div[@class=\"item\"]/a[1]")

for i, url in enumerate(book_urls):
    book_urls[i] = url.get_attribute('href')

books=[]
for book_num,book_url in enumerate(book_urls):
    #make a dictionary, which contains required information, for each book
    newBookInformation={}
    driver.get(book_url)
    #get price
    price=driver.find_element(By.XPATH,"//*[@id=\"BookDetails\"]/div/div[2]/div/span")
    newBookInformation["price"] = price.text
    #get score
    scoreWidth = driver.find_element(By.XPATH, "/html/body/div[2]/div/main/div/article/div[1]/div[3]/a/div/div/div").get_attribute("style")
    widthArray=scoreWidth.split()
    widthNum=float(widthArray[1].replace("px","").replace(";",""))
    score="{:.2f}".format((widthNum*5)/90)
    newBookInformation["score"] = score
    #get all rows of the table containig some of the information about the book
    rows = driver.find_elements(By.XPATH, "//*[@id=\"BookDetails\"]/table/tbody/tr")
    #get columns of eah row and fill newBookInformation dictionary with them
    for i, row in enumerate(rows, 1):
        rowTitlePath = "//*[@id=\"BookDetails\"]/table/tbody/tr[" + str(i) + "]/td[1]"
        rowContentPath = "//*[@id=\"BookDetails\"]/table/tbody/tr[" + str(i) + "]/td[2]"
        rowTitle=driver.find_element(By.XPATH,rowTitlePath).text
        rowContent=driver.find_element(By.XPATH,rowContentPath).text
        match rowTitle:
            case "نام کتاب":
                newBookInformation["title"]=rowContent
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
    #get the number of comments each book has
    try:
        comment_count = driver.find_element(By.CSS_SELECTOR, ".comment-count")
        newBookInformation["numberOfComments"] = comment_count.text
    except NoSuchElementException:
        newBookInformation["numberOfComments"]=0



    print(newBookInformation)
    books.append(newBookInformation)
driver.close()
