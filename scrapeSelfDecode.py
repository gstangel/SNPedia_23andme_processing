import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

file = open('snps.txt', 'r')

lines = file.readlines()
base_url = 'https://selfdecode.com/snp/'

urls = [base_url + snp.rstrip() for snp in lines]



def getData(url):
    print(url)
    html = requests.get(url)
    return html.status_code

processes = []

with ThreadPoolExecutor(max_workers=100) as executor:
    for url in urls:
        processes.append(executor.submit(getData, url))

for task in as_completed(processes):
    print(task.result())
