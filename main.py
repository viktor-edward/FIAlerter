import datetime
import requests
from bs4 import BeautifulSoup
import re


if __name__ == '__main__':
    watchedTitles = ["regelverk", "klagomål"]

    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    yesterdayStr = yesterday.strftime("%Y-%m-%d")

    URL = f'https://www.fi.se/sv/vara-register/diarieforda-arenden/AdvancedSearch/' \
          f'?recipient=&number=&from={yesterdayStr}&to={yesterdayStr}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find("table", class_="diarie-results").find_all("tr")[1:]

    for row in rows:
        entrySplit = row.find_all("td")
        tempRowArray = []
        for value in entrySplit:
            tempRowArray.append(value.text)
        if re.compile('|'.join(watchedTitles), re.IGNORECASE).search(tempRowArray[3]):
            print("Found matching errand: ")
            print(tempRowArray)
