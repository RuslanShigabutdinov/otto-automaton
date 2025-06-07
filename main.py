from playwright.sync_api import sync_playwright
from time import sleep
from libs._eanExtract import getEansFromCSV, extractEansFromFile
import printer

sessionFile = 'authState.json'

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

def addEanToTxt(ean):
    with open('activeProducts.txt', 'a') as file:
        file.write(f'{ean}\n')

def isProductNaughty(page):
    labelsWarning = page.locator('span.obc_label.obc_label--warning')
    countLoss = labelsWarning.count()
    labelsSuccess = page.locator('span.obc_label.obc_label--success')
    countWin = labelsSuccess.count()
    printer.blue(f'errors: {countLoss}, fines: {countWin}')
    return countWin != 0

def setupCLicks(page):
    page.wait_for_selector('#cookieBannerButtonAccept', state='attached')
    page.click('#cookieBannerButtonAccept')  # Принятие куки
    sleep(.5)
    page.wait_for_selector('.navigation-toggle--button', state='attached')
    page.click('.navigation-toggle--button')  # скрытие sidebar

def searchProduct(page, ean):
    page.wait_for_selector('#searchField', state='attached')
    page.fill('#searchField', ean)
    page.click('#searchFieldButton')

def runWithSavedSession(eans):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=sessionFile)

        page = context.new_page()
        page.goto('https://portal.otto.market/products/#productoverview')

        print('Session started')

        setupCLicks(page)

        for ean in eans:
            searchProduct(page, ean)
            waitForEanToAppear(page, ean)
            if isProductNaughty(page):
                printer.red(f'found naughty product [{ean}]')
                addEanToTxt(ean)
            else:
                printer.green(f'product [{ean}] is inactive')

        input("Нажми Enter, чтобы завершить...")

        browser.close()

if __name__ == '__main__':
    # eans = getEansFromCSV()
    eans = extractEansFromFile('ean.txt')
    runWithSavedSession(eans)