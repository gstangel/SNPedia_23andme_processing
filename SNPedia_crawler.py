import mwclient
from os import path
import pickle as pkl
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import lxml
import numpy as np
import sys
import asyncio
import aiohttp
import progressbar
#uses mwclient to pull only unique rsids from SNPedia (~110k individual rsids) and generate cooresponding links for crawling
#One example link is https://snpedia.com/index.php/Rs1804197
#The rsid number is a unique label ("rs" followed by a number) used by researchers and databases to identify a specific SNP (Single Nucleotide Polymorphism)
def get_rsid_links() -> list:
    if not path.exists("rsid_links.pkl"):
        print("Getting all unique rsID links...")
        base_url = "https://snpedia.com/index.php/"
        site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path
        rsid_links = [base_url + rsid.name.lower() for rsid in site.Categories['Is_a_snp']]#create a list of all snps stored in site object, mwclient makes this easy
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
    rsid_data = {} #where the resulting data will be stored, in the form of ex: 'rs123321':['AA', repute = good, magnitude = 5, description = 'AA' makes for better coders]
    
    #this function is used to create asyncernous requests
    def fetch(session, url):
        
        with session.get(url) as page: #make request for next of the 110k links to be pulled
            soup = BeautifulSoup(page.content, 'lxml') #'lxml' is much faster than python's html parser
            rsid = soup.find(id='firstHeading').text #ex: "rs6152", .text converts from soup object to string
            genotype_table = soup.find_all('table', attrs={'class': 'sortable'}) #find the table on the website with rsid variation data
            variation_data = [] #where all the studied variations and cooresponding information will be stored
            #pulls relevant data from the tables on SNPedia
            if len(genotype_table) > 0:
                for tr in genotype_table[0].find_all('tr'):
                    for td in tr.find_all('td'):
                        if '#ff8080' in str(td):#if the color is red, its been determined to be a bad trait
                            variation_data.append('bad')
                        if '#80ff80' in str(td):#if the color is green, its been determined to be a good trait
                            variation_data.append('good')
                        if '#ffffff' in str(td):
                            variation_data.append('neutral')#if the color is white, it a neutral trait
                        variation_data.append(td.text.rstrip())#append alleles for mutation

            rsid_data[rsid] = np.array(variation_data) #use np array for ram constraints
            progress.update(len(rsid_data))
    
    async def start_crawl_asynchronous():
        with ThreadPoolExecutor(max_workers=150) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                for url in rsid_urls:
                    loop.run_in_executor(executor, fetch, *(session,url))
    progress = progressbar.ProgressBar(max_value = len(rsid_urls))
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_crawl_asynchronous())
    loop.run_until_complete(future)
    

links = get_rsid_links()
crawl(links)

