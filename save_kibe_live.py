#!venv/bin/python
from datetime import datetime
import gspread
import pandas as pd
import requests
import xmltodict
from gspread import WorksheetNotFound

SHEET_LINK = 'https://docs.google.com/spreadsheets/d/1yQFIRC1dF9rWpXaQYxT78-WwO_egei7xJFye--rtBts'


def load_rss():
    # RSS feed urls for channels to watch (Every YouTube channel has its own feed)
    # You can add more than one channels.
    # In this case Kibe had 2 main channels where he hosted his live shows
    urls = ['https://www.youtube.com/feeds/videos.xml?channel_id=UC8Am29Ya-UUSjgwg8Vz-sgA',
            'https://www.youtube.com/feeds/videos.xml?channel_id=UCi9Bsr4XDlN7_JaL3H0WF9g'
            ]

    # creating HTTP response object from given url
    items = []
    for feed in urls:
        resp = requests.get(feed)
        # saving the xml file
        name = feed.split('=')[-1]
        file_name = f'kibefeed_{name}.xml'
        with open(file_name, 'wb') as f:
            f.write(resp.content)
        news_items = parse_xml(file_name)
        items.extend(news_items)
    read_url(SHEET_LINK, items)


def parse_xml(xmlfile):
    with open(xmlfile) as xmlfeed:
        xml = xmltodict.parse(xmlfeed.read())
        videos = xml['feed']['entry']
        data = []
        for entry in videos:
            date = entry['published']
            date_2 = datetime.fromisoformat(date)
            title = entry['title']
            link = entry['link']['@href']
            data.append({'Date': str(date_2).split('+')[0], 'Title': title.strip(), 'Link': link.strip()})
        return data


def read_url(url, data):
    data = pd.DataFrame(data=data)
    # You need a google service account json to allow a program to edit your google sheet
    # You must add the service account to be an editor in your google sheet
    # More details and guidelines are found in gspread documentation.
    gc = gspread.service_account(filename='your-google-service-account.json')
    sheet = gc.open_by_url(url)
    current_worksheet = month_str()
    try:
        worksheet = sheet.worksheet(current_worksheet)
    except WorksheetNotFound:
        worksheet = sheet.add_worksheet(current_worksheet, 100, 10, 0)
    existing_data = pd.DataFrame(worksheet.get_all_records())
    new_data = pd.concat([data, existing_data]).drop_duplicates().reset_index(drop=True)
    new_data = new_data.sort_values(by='Date', ascending=False)
    worksheet.clear()
    worksheet.update([new_data.columns.values.tolist()] + new_data.values.tolist())


def month_str():
    today = datetime.now()
    year, month = str(today.year), str(today.month)
    if len(month) == 1:
        month = '0' + month
    return f"{year}/{month}"


if __name__ == "__main__":
    load_rss()
