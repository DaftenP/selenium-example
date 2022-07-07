import requests
import pandas

file = open('work_list_5.csv', encoding='utf-8-sig')
result = []

for line in file:
    url = 'http://' + line.lstrip('http://').lstrip('https://').rstrip('\n')
    try:
        requests.get(url)
        print(f'{line}: connection is valid')
        result.append(line)

    except:
        continue
df = pandas.DataFrame(result)
df.to_csv('./filtered_data.csv', encoding='utf-8-sig', mode='a', index=False)
print('Filtering was successfully')