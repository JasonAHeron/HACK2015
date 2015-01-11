import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

file = open("out.txt", "w+")

def setup():
    browser = webdriver.Firefox()
    browser.get("https://pisa.ucsc.edu/class_search/index.php")
    assert 'UC Santa Cruz' in browser.title
    browser = get_all(browser)
    return browser

def get_all(browser):
    elem = browser.find_element_by_id('reg_status')  # Finds the search box
    elem.send_keys(Keys.DOWN)
    elem = browser.find_element_by_id('subject')  # Finds the search box
    elem.send_keys(Keys.DOWN)
    elem = browser.find_element_by_id('search_anchor') # Finds the SEND button
    elem.send_keys(Keys.ENTER)
    elem = browser.find_element_by_id('Rec_Dur') # Get 100 items on the page
    elem.send_keys(Keys.DOWN)
    elem.send_keys(Keys.DOWN)
    elem.send_keys(Keys.DOWN)
    elem.send_keys(Keys.ENTER)
    browser = pull_classes(browser)
    return browser


def pull_classes(browser):
    all = ""
    next_button = browser.find_element_by_xpath('//*[@id="displaying_notice"]/table/tbody/tr[2]/td/a')
    while True:
        elem = browser.find_element_by_id('results_table')
        all += elem.text
        try:
            next_button.click()
            next_button = browser.find_element_by_xpath('//*[@id="displaying_notice"]/table/tbody/tr[2]/td/a[2]')
        except:
            elem = browser.find_element_by_id('results_table')
            all += elem.text
            break

    items = []
    for string in all.split('\n'):
        try:
            class_ = re.search("(\d{5}) [A-Z]* (\w+)", string).group(0)[6:]
        except:
            continue
        if class_ not in items:
            items.append(class_)
            file.write(class_)
            file.write('\n')
    file.close()
    browser.quit()




setup()