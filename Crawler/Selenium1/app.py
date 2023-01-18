"""

"""
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(driver, options = chrome_options)
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(driver)

TAGS_ATHORS = 1

def search():
    if TAGS_ATHORS == 0:
        html = 'https://quotes.toscrape.com/js-delayed/'
        inputselector = '.tag'
    else:
        html = 'https://quotes.toscrape.com/'
        inputselector = '.author'

    browser.get(html)
    i = 2
    tags = set()
    while i<=10:
        if TAGS_ATHORS == 0:
            time.sleep(12)
        else:
            time.sleep(3)

        tags_in_page = [elem.text for elem in browser.find_elements_by_css_selector(inputselector)]
        for tag in tags_in_page:
            # print(tag)
            tags.add(tag)
        try:
            # next = WebDriverWait(driver, 60).until(ExpectedConditions.elementToBeClickable('.pager .next>a'));
            browser.get(html + 'page/'+str(i))
            # next = browser.find_elements_by_css_selector('.pager .next>a') #.click()
            # next.sendKeys(Keys.ENTER)
            # time.sleep(15)
            i += 1
        except Exception:
            break

    browser.close()
    tags_str = ', '.join(sorted(tags))
    print(tags_str)
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(tags_str+'\n')

if __name__ == "__main__":
    search()
