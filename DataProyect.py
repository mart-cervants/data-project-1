from pathlib import Path
import os
import sys
from bs4 import BeautifulSoup
import requests
import csv
import re
from datetime import datetime
import pandas as pd


def extract_impact_date(link: str):

    # Impact date
    info = (
        BeautifulSoup(requests.get(link).content, "html.parser")
        .find("table", {"id": "msis-detail-table"})  # Find the table
        .find_all("p")[3]  # Get the impact date tag
        .text.strip()  # Clean the text
    )
    

    # Change format from 02 May 2022 to 2022-05-02
    return map(
        lambda x: datetime.strptime(x, "%d %b %Y").date(),
        re.findall(r"From(.*)to(.*)", info)[0],
    )


url = requests.get(
    "http://data.tga.gov.au/medicineshortages/MedicineShortagesWebService.svc/rssfeed"
)

soup = BeautifulSoup(url.content, "xml")
items = soup.find_all("item")

data = {
    "Title": [],
    "Description": [],
    "Start_date": [],
    "end_date": [],
    "link": [],
}
for i in range(28):
    title = items[i].title.text
    description = items[i].description.text
    link = items[i].link.text

    Start_date, end_date = extract_impact_date(link)

    print(Start_date, end_date)

    data["Title"].append(title)
    data["Description"].append(description)
    data["Start_date"].append(Start_date)
    data["end_date"].append(end_date)
    data["link"].append(link)
    # print("title: " + title + "description: " + description)


# filepath = Path("/TGA.csv")  
# filepath.parent.mkdir(parents=True, exist_ok=True)
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
csv_path = os.path.join(script_dir, './TGA_medlist.csv')
# writing to file
header = ["Title", "Description", "Link", "Start_date", "end_data"]
pd.DataFrame(data).to_csv(csv_path)
