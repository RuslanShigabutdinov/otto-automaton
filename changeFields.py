from playwright.sync_api import sync_playwright
from time import sleep
from libs._eanFinder import getArtNumFromUrl, artNumToEan
import keyboard
import win32clipboard
from keysConfig import *
from libs._dbSQLite import Database
from libs._afterbuy import displayEbayLister

def getContentFromClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    cleaned = data.strip()
    return cleaned

sessionFiles = {
    'otto': 'auth/otto.json',
    'afterbuy': 'auth/afterbuy.json'
}

def clickButtonIfAppears(page, buttonText="Kategorie wechseln", timeout=500):
    try:
        button = page.wait_for_selector(f'text="{buttonText}"', timeout=timeout)
        if button:
            button.click()
            print(f"Кнопка '{buttonText}' найдена и нажата")
    except:
        print(f"Кнопка '{buttonText}' не появилась за {timeout/1000} секунды")

def waitForEanToAppear(page, ean, timeout=8000):
    page.wait_for_function(f"""
        ([ean]) => {{
            const elements = document.querySelectorAll('.obc_link');
            for (const el of elements) {{
                if (el.innerHTML.includes(ean)) {{
                    return true;
                }}
            }}
            return false;
        }}
    """, arg=[ean], timeout=timeout)

def setupClicks(page):
    page.wait_for_selector('#cookieBannerButtonAccept', state='attached')
    page.click('#cookieBannerButtonAccept')  # Accept cookies

def searchProduct(page, ean):
    page.wait_for_selector('#searchField', state='attached')
    page.fill('#searchField', ean)
    page.click('#searchFieldButton')

def waitAndClick(page, element):
    page.wait_for_selector(element, state='attached', timeout=5000)
    page.click(element)

def insertEanLogic(page, db: Database):
    url = getContentFromClipboard()
    articleNumber = getArtNumFromUrl(url)
    eanArr = artNumToEan(db, articleNumber)
    ean = None
    if len(eanArr) > 0:
        ean = eanArr[0]
    if ean != None:
        try:
            searchProduct(page, ean)
            waitForEanToAppear(page, ean)
            page.wait_for_selector('a.obc_link.edit-points.obc_icon-edit', state='attached', timeout=5000)
            page.click('a.obc_link.edit-points.obc_icon-edit')
            print(f"Clicked edit button for EAN: {ean}")
        except Exception as e:
            print(f"Error processing EAN {ean}")
    else:
        page.wait_for_selector('#searchField', state='attached')
        page.fill('#searchField', ':(')
    sleep(0.5)

def insertCategoryLogic(page):
    try:
        waitAndClick(page, '#category')
        waitAndClick(page, '#catSearchResultHeader')
        searchQuery = getContentFromClipboard()
        page.fill('#categorySearch', searchQuery)
        elements = page.locator('.obc_copy100.obc_ml-2')
        count = elements.count()
        matchFound = False
        for i in range(count):
            element = elements.nth(i)
            text : str = element.inner_text().strip()
            if text.lower() == searchQuery.strip().lower():
                element.click()
                matchFound = True
                print(f"Нажата категория: {text}")
                waitAndClick(page, '#confirm')
                clickButtonIfAppears(page)
                break
        if not matchFound:
            print(f"Не найдена категория '{searchQuery}'")
        sleep(0.5)
    except:
        print('Проблема с поиском категории')

def publishProductLogic(page):
    try:
        waitAndClick(page, '#mediaAssets')
        waitAndClick(page, '#publish')
        print('Продукт опубликован')
    except:
        print('Проблема с публикацией продукта')


def listenForKeys(page, db: Database, context):
    while True:
        if keyboard.is_pressed(insertEanButton):
            insertEanLogic(page, db)
        if keyboard.is_pressed(insertCategoryButton):
            insertCategoryLogic(page)
        if keyboard.is_pressed(afterbuyButton):
            displayEbayLister(db, context)
        if keyboard.is_pressed(publishProductButton):
            publishProductLogic(page)
        if keyboard.is_pressed(exitProgramButton):
            print(f"{exitProgramButton} pressed! exiting program")
            break
        sleep(0.1)

def runWithSavedSession():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Non-headless for manual interaction
        context = browser.new_context(storage_state=sessionFiles['otto'])

        page = context.new_page()
        page.goto('https://portal.otto.market/products/#productoverview')

        print(f'''
Скрипт запущен. Управление:
{insertEanButton} - Вставляет ЕАН в поле для поиска еан, и автоматически заходит на продукт
{insertCategoryButton} - Вставляет категорию в поле для кагории. Если находит 100% сходство категории, применяет её
{publishProductButton} - Публикует товар
{exitProgramButton} - Выходит из программы
        ''')
        db = Database()
        setupClicks(page)
        listenForKeys(page, db, context)
        browser.close()

if __name__ == '__main__':
    runWithSavedSession()