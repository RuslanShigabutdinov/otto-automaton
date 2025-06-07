import pandas as pd
import re

def getEansFromCSV():
    df = pd.read_csv('ean_data.csv', sep=',')
    onlyEans = df[['EAN']]
    arr = onlyEans.values.tolist()
    return [i[0] for i in arr]

def extractEansFromFile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    eans = re.findall(r'\b\d{8,14}\b', text)

    return eans

if __name__ == '__main__':
    eans = extractEansFromFile('ean.txt')
    print(len(eans))