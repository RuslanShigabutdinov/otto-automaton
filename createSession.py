from playwright.sync_api import sync_playwright
import libs._creds as _creds
from libs._googleAuth import generateTotp
from time import sleep
from _path import currentPath


def insertLoginOtto(page, server):
    page.wait_for_selector('#username', state='attached')
    page.fill('#username', server['login'])
    page.fill('#password', server['password'])
    page.click('#kc-login')

def insertLoginAfterbuy(page, server):
    page.wait_for_selector('#CybotCookiebotDialogBodyButtonDecline', state='attached')
    page.click('#CybotCookiebotDialogBodyButtonDecline')
    page.wait_for_selector('#Username', state='attached')
    page.click('#StaySignedIn')
    page.fill('#Username', server['login'])
    page.fill('#Password', server['password'])
    page.click("button[name='B1']")
    

def insertOtp(page, server):
    generatedCode = generateTotp(server['secret'])
    page.wait_for_selector('#otp', state='attached')
    page.fill('#otp', generatedCode)
    page.wait_for_selector('#kc-login', state='attached')
    page.click('#kc-login')

def setupCLicks(page):
    page.wait_for_selector('.navigation-toggle--button', state='attached')
    page.click('.navigation-toggle--button')  # скрытие sidebar
    sleep(1)
    page.wait_for_selector('#cookieBannerButtonAccept', state='attached')
    page.click('#cookieBannerButtonAccept')  # Принятие куки

def authOtto(context, base):
    page = context.new_page()
    page.goto("https://portal.otto.market/products/productMaintenance/c3e9b5cc-5667-5c50-80fe-6a72ab4b27d3")
    insertLoginOtto(page, base)
    insertOtp(page, base)
    setupCLicks(page)
    sessionFile = f'{currentPath()}/auth/otto.json'

    context.storage_state(path=sessionFile)
    print(f"Сессия сохранена в {sessionFile}")

def authAfterbuy(context, base):
    page = context.new_page()
    page.goto("https://login.afterbuy.de/Account/Login")
    insertLoginAfterbuy(page, base)
    sessionFile = f'{currentPath()}/auth/afterbuy.json'
    context.storage_state(path=sessionFile)

def manualLoginAndSaveSession():
    answer = 2
    while answer not in ['1', '2']:
        answer = input('Какой аккаунт тебя интересует: \n[1] XL\n[2] JV\n')
    ottoBase = _creds.xl
    afterbuyBase = _creds.afterBuyXl
    if answer == '2':
        ottoBase = _creds.jv
        afterbuyBase = _creds.afterBuyJv
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()

        authAfterbuy(context, afterbuyBase)
        authOtto(context, ottoBase)

        browser.close()


if __name__=='__main__':
    manualLoginAndSaveSession()