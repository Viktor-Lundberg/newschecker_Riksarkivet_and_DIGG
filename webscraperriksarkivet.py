import requests
from bs4 import BeautifulSoup
from datetime import *
from win10toast import ToastNotifier
import time
import webbrowser

# Skapar funktion för att gå till nyhetens websida vid klick
def go_to_page(adress):
    adress = f'https://riksarkivet.se{adress}'
    webbrowser.open(adress)

# URL som ska scrapas och gör en förfrågan mot den med requests
URL = 'https://riksarkivet.se/nyheter-och-press'
page = requests.get(URL)

# Använder Beutifulsoup för att parsa den hämtade html:en från page
soup = BeautifulSoup(page.content, 'html.parser')

# Hittar alla div med classen newsitem bland html:en.
results = soup.find_all('div', class_='newsitem')

# Notifieringar använder toaster + variabel för att senare använda för att kolla om det finns nya nyheter
toaster = ToastNotifier()
nonewnews = True

# Hämtar dagens datum och räknar ut gårdagens datum
today = date.today()
yesterday = today - timedelta(days=1)


# Loopar igenom alla hämtade divar
for result in results:
    # Hittar publiceringsdatumet för nyheten
    pubdate = result.find('div', class_='newsitem-publishdate')
    # Hittar innehållet alltså själva nyheten
    newsarticle = result.find('p')
    # Hittar rubriken för nyheten
    header = result.find('a')['title']
    # Hittar länken för nyheten
    link = result.find('a')['href']
    # Skapar en variabel för att jämföra datum, tar publiceringsdatum och strippar från HTML
    pubdatecompare = pubdate.text.strip()
    #date_time_str = pubdatecompare
    # Publiceringsdatum enligt formatet DD MM YYYY, byter ut "svenska månadsförkortningar" mot engelska
    pubdatecompare = str.replace(pubdatecompare,'okt','oct') or str.replace(pubdatecompare,'maj','may')
    # Gör om publiceringsdatumet till ett datumobjekt.
    date_time_obj = datetime.strptime(pubdatecompare, '%d %b %Y')
    # Formaterar datumformatet till YYYY-MM-DD i en ny variabel.
    pubdatecompare2 = date_time_obj.date()
    # Med en if sats kontrollerar om publiceringsdatumet är igår eller idag för att bara få de "senaste" nyheterna
    if pubdatecompare2 > yesterday or pubdatecompare2 == yesterday:
        # Printar lite för att kolla vad vi får fram.
        print(header)
        print(link)
        print(pubdate.text.strip())
        print(newsarticle.text.strip())
        # Skapar en notifikation som vid klickning går till nyhetens webadress med hjälp av den tidigare skapade funktionen "go_to_page"
        toaster.show_toast(header,newsarticle.text.strip(), duration=30, threaded=False, callback_on_click=lambda: go_to_page(link))
        # Sover lite för att inte alla nyheter ska komma samtidigt
        time.sleep(5)
        nonewnews = False
    else:
        continue

# Skickar iväg en notis om att det inte finns några nyheter ifall variabeln nonewnews är True
if nonewnews == True:
    toaster.show_toast('På Riksarkivet intet nytt!', '....')

