from libs._dbSQLite import Database
from libs._eanFinder import *
from libs._clipboard import getContentFromClipboard

page = 'https://afterbuy.de/afterbuy/ebayliste2.aspx?newsearch=1&DT=1'

def displayEbayLister(db: Database, context):
    url = getContentFromClipboard()
    articleNumber = getArtNumFromUrl(url)
    eanArr = artNumToEan(db, articleNumber)
    ean = None
    if len(eanArr) > 0:
        ean = eanArr[0]
    if ean != None:
        try:
            page = context.new_page()
            page.goto(page)
            element = page.locator("[name='lAWean']")
            element.fill(ean)
            page.click('#ctl00_innerContentPlaceHolder_AllBox_ebaylister_btn_Suchen')
        except:
            print('Ошибка при поиске товара в afterbuy')