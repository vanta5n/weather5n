import requests
from bs4 import BeautifulSoup


def get_weather(city):
    url = "https://www.google.com/search?q=" + "weather" + city
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

    str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str_.split('\n')
    time = data[0]
    sky = data[1]

    return temp, time, sky


if __name__ == '__main__':
    url = "https://www.google.com/search?q=" + "weather" + 'сочи'
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')
    aaa = soup.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).text
    print(aaa)
