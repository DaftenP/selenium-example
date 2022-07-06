from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import pandas as pd

wd = webdriver.Chrome('./WebDriver/chromedriver.exe')

file = open("work_list.csv", encoding="utf-8-sig")
result = []
i = 0
for line in file:
    i += 1
    if 'cafe' in line:
        result.append([line, ""])
        print(f'{i} - passed')
        continue
    url = 'http://' + line.lstrip('http://').lstrip('https://').rstrip('\n')
    try:
        wd.get(url)
        element = WebDriverWait(wd, 2).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "footer")))
        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('footer')
        result.append([line, data])
        print(f'{i}: {url} - crawling has been successfully')
    except:
        result.append([line, ""])
        print(f'{i}: {url} - not exist')
    finally:
        if i % 30 == 0:
            df = pd.DataFrame(result, columns=['name', 'data'])
            df.to_csv('./site_info.csv', encoding='utf-8-sig', mode='a', index=False)
            result = []
            print('data saved')

df = pd.DataFrame(result, columns=['name', 'data'])
df.to_csv('./site_info.csv', encoding='utf-8-sig', mode='a', index=False)
print('Completed..')
