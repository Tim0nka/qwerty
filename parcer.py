from bs4 import BeautifulSoup
import requests

url = 'https://1k.by/remont/instruments-drills/'
page = requests.get(url)


soup = BeautifulSoup(page.text, "html.parser")


# print(soup)
filteredNews = []
allTema = []


allTema = soup.findAll('a', {"class": "prod__link"})
# print(allTema)
for entry in allTema:
    print(entry.get_text())

# for data in allTema:
#     if data.find('div', class_="prod__media") is not None:
#         filteredNews.append(data.text)

# for data in filteredNews:
#     print(data)

# free-proxy-list.net/ru/
