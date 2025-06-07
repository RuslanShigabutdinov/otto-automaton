from libs._dbSQLite import Database

def artNumToEan(db:Database, articleNumber:str) -> str:
    print('trying to find ean')
    data = db.showEan(articleNumber)
    if data == None:
        data = db.showEanLike(articleNumber)
        if data == None:
            return []
        eanList = [product['ean'] for product in data]
        print(f'found: {eanList}')
        return eanList
    ean = data['ean']
    print(f'found: {ean}')
    return [ean]

def getArtNumFromUrl(url: str) -> str:
    url = url.split('-')[-1]
    url = url.split('/')[0]
    return url