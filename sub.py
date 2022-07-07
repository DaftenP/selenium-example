from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import pandas as pd


def close_handles(self, driver):
    global main_handle

    handles = driver.window_handles
    size = len(handles)

    main_handle = driver.current_window_handle
    for x in range(size):
        if handles[x] != main_handle:
            driver.switch_to.window(handles[x])
            driver.close()

    driver.switch_to.window(main_handle)

    driver.switch_to.frame(0)


wd = webdriver.Chrome('./WebDriver/chromedriver.exe')

file = open("work_list_5.csv", encoding="utf-8-sig")
result = []
i = 0
success = 0
for line in file:
    i += 1
    if 'cafe' in line:
        result.append([line.rstrip('\n'), ""])
        print(f'{i} - passed')
        continue
    url = 'http://' + line.lstrip('http://').lstrip('https://').rstrip('\n')
    try:
        wd.get(url)
        element = WebDriverWait(wd, 2).until(
            expected_conditions.presence_of_element_located((By.ID, "foot")))
        close_handles(wd)
        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('#foot')
        result.append([line.rstrip('\n'), data])
        print(f'{i}: {url} - crawling has been successfully')
        success += 1
    except:
        result.append([line.rstrip('\n'), ""])
        print(f'{i}: {url} - not exist')
    finally:
        if i % 30 == 0:
            df = pd.DataFrame(result)
            df.to_csv('./site_info.csv', encoding='utf-8-sig', mode='a', index=False)
            result = []
            print('data saved')

df = pd.DataFrame(result)
df.to_csv('./site_info.csv', encoding='utf-8-sig', mode='a', index=False)
print(f'{success} data has stored successfully..')
