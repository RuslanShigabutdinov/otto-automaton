from libs._dbSQLite import Database
from playwright.sync_api import sync_playwright
from libs._eanFinder import *

pages = {
    'products': 'afterbuy.de/afterbuy/shop/produkte.aspx?newsearch=1&DT=1',
    'ebayLister': 'afterbuy.de/afterbuy/ebayliste2.aspx?newsearch=1&DT=1'
}

def displayEbayLister(db: Database, context):
    page = context.new_page()
    page.goto(pages['products'])
    element = page.locator("[name='ProductSearchMpn']")

    element.fill('')
    input()