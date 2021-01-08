import mwclient
from os import path
import pickle as pkl
import requests
from bounded_pool_executor import BoundedThreadPoolExecutor
from bs4 import BeautifulSoup
import lxml
import numpy as np
import sys
import asyncio
import aiohttp
import progressbar
import logging
logging.basicConfig(filename='log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#uses mwclient to pull only unique rsids from SNPedia (~110k individual rsids) and generate cooresponding links for crawling
#One example link is https://snpedia.com/index.php/Rs1804197
#The rsid number is a unique label ("rs" followed by a number) used by researchers and databases to identify a specific SNP (Single Nucleotide Polymorphism)
def get_rsid_links() -> list:
    if not path.exists("rsid_links.pkl"):
        print("Getting all unique rsID links...")
        base_url = "https://snpedia.com/index.php/"
        site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path
        rsid_links = [base_url + rsid.name.lower() for rsid in site.Categories['Apperance']]#create a list of all snps stored in site object, mwclient makes this easy
        with open('rsid_links.pkl', 'wb') as file:
            pkl.dump(rsid_links, file)
        return rsid_links
    else:
        with open('rsid_links.pkl', 'rb') as file:
            rsid_links = pkl.load(file)
        return rsid_links


#mwclient supports pulling each rsid's associated data, but much slower than threaded requests 
#returns a dict of all the data for each rsid, uses BeautifulSoup to extract most relevant data
def crawl(rsid_urls) -> dict:

    def fetch(url):
        file_name = url[30:len(url)] + ".html"
        if not path.exists('C:/Users/Home PC/Desktop/23andme/raw html/' + file_name):
            try:
                with requests.get(url) as page: #make request for next of the 110k links to be pulled
                    if page.status_code == 200:
                        with open('C:/Users/Home PC/Desktop/23andme/raw html/' + file_name, 'wb') as html_file:
                            html_file.write(page.content)
                    else:
                        logging.error(url)


            except Exception as e:
                print(e)
                print(url)
        
            
    

    
    def get_data():
        #for i in range(len(split_url)):
        with BoundedThreadPoolExecutor(max_workers=25) as executor:
            for url in rsid_urls:
                executor.submit(fetch,url)

                
    get_data()

  

    
    

    

links = get_rsid_links()
crawl(links)