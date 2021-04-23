import requests
from bs4 import BeautifulSoup
from datetime import *
import time
import locale
from win10toast import ToastNotifier
import webbrowser
import ssl



def go_to_page(adress):
    adress = f'https://digg.se{adress}'
    webbrowser.open(adress)

# Hantera ev certifikatsproblem
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



locale.setlocale(locale.LC_ALL, 'sv_SE.utf8')
today = date.today()
yesterday = today - timedelta(days=1)
curdate = time.strptime(str(yesterday), '%Y-%m-%d')

toaster = ToastNotifier()
nonewnews = True

url = 'https://www.digg.se/om-oss/nyheter'
page = requests.get(url) #verify=False

soup = BeautifulSoup(page.content,'html.parser')

results = soup.find_all('li', class_='css-0')

for result in results:
    newsheader = result.find('div', class_='css-1wwwi8').text
    date = result.find('div', class_='css-6vk0lw').text
    #print(date)
    comparedate = time.strptime(date, '%d %B %Y')
    #print(comparedate)
    link = result.find('a')['href']
    if curdate <= comparedate:
        print(newsheader)
        print(link)
        print(date)
        toaster.show_toast(f'DIGG {date}', newsheader, duration=30, threaded=False, callback_on_click=lambda: go_to_page(link))
        time.sleep(5)
        nonewnews = False
    else:
        continue

if nonewnews == True:
    toaster.show_toast('På DIGG intet nytt!', '....')

