from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import pandas as pd

wd = webdriver.Chrome('./WebDriver/chromedriver.exe')

result = []
for i in range(1, 2000):
    try:
        wd.get('http://www.ble.or.kr/Home/Organ/ORGList.mbz?action=MAPP_0000000160')
        wd.execute_script('fn_viewData(%d)' % i)
        element = WebDriverWait(wd, 2).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "ui-view")))
        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.select('table.ui-view > tbody > tr > td')
        info_a = soup.select('table.ui-view > tbody > tr > td > a')
        info_site = soup.select('table.ui-view > tbody > tr > td > a[href]')
        name = info[6].string.strip()
        address = info[18].string.splitlines()
        address = address[-3].strip() + address[-2].strip()
        phone = info_a[0].string.strip()
        email = info[8].string.strip()
        fax = info[5].string.strip()
        try:
            site = info_site[1].attrs['href'].strip()
        except:
            site = ""
        state = info[3].string.strip()
        result.append([name, address, phone, email, fax, site, state])
        print(f'{i} : {name} {address} {phone} {email} {fax} {site} {state}')
    except:
        print(f'{i} : not exist')
        continue
    finally:
        if i % 100 == 0:
            df = pd.DataFrame(result, columns=('name', 'address', 'phone', 'email', 'fax', 'site', 'state'))
            df.to_csv('./result.csv', encoding='utf-8-sig', mode='a', index=False)
            print("Data Saved")
            result = []
wd.quit()
df = pd.DataFrame(result, columns=('name', 'address', 'phone', 'email', 'fax', 'site', 'state'))
df.to_csv('./result.csv', encoding='utf-8-sig', mode='a', index=False)
print('Completed..')
