import datetime
import requests
from bs4 import BeautifulSoup
import re


def main():
    watchedTitles = ["regelverk", "klagomål"]

    toDate = getLatestDiarieDate()
    toDateStr = toDate.strftime("%Y-%m-%d")
    latestReadDate = getLatestReadDate()
    if latestReadDate < toDate:
        fromDate = latestReadDate + datetime.timedelta(days=1)
        fromDateStr = fromDate.strftime("%Y-%m-%d")
    else:
        print(f"Already read the latest posts from {toDateStr}")
        return

    url = f"https://www.fi.se/sv/vara-register/diarieforda-arenden/AdvancedSearch/" \
          f"?recipient=&number=&from={fromDateStr}&to={toDateStr}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="diarie-results")

    if table is not None:
        rows = table.find_all("tr")[1:]

        for row in rows:
            entrySplit = row.find_all("td")
            tempRowArray = []
            for value in entrySplit:
                tempRowArray.append(value.text)
            if re.compile('|'.join(watchedTitles), re.IGNORECASE).search(tempRowArray[3]):
                print("Found matching errand: ")
                print(tempRowArray)

    setLatestReadDate(toDateStr)


def getLatestDiarieDate() -> datetime:
    url = "https://www.fi.se/sv/vara-register/diarieforda-arenden"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    firstRow = soup.find("table", class_="diarie-results").find_all("tr")[1]
    latestDate = firstRow.find_all("td")[0].text
    return datetime.datetime.strptime(latestDate, "%Y-%m-%d")


def getLatestReadDate() -> datetime:
    try:
        with open("lastReadDate.txt") as file:
            lastReadDateStr = file.read()
            lastReadDate = datetime.datetime.strptime(lastReadDateStr, "%Y-%m-%d")
    except IOError:
        with open("lastReadDate.txt", "w+") as file:
            lastReadDate = getLatestDiarieDate() + datetime.timedelta(days=-1)
            yesterdayStr = lastReadDate.strftime("%Y-%m-%d")
            file.write(yesterdayStr)
            print("No previous date read, setting last read date to a day before last diarie date.")
    return lastReadDate


def setLatestReadDate(toDateStr: str):
    with open("lastReadDate.txt", "w+") as file:
        file.write(toDateStr)


if __name__ == '__main__':
    main()
