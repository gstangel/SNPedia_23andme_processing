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
        try:
            with session.get(url) as page: #make request for next of the 110k links to be pulled
                print(page.status_code)
                soup = BeautifulSoup(page.content, 'lxml') #'lxml' is much faster than python's html parser
                rsid = url[30:len(url)] #ex: "rs6152", .text converts from soup object to string

                genotype_table = soup.find_all('table', attrs={'class': 'sortable'}) #find the table on the website with rsid variation data
                variation_data = [] #where all the studied variations and cooresponding information will be stored
                #pulls relevant data from the tables on SNPedia
                if len(genotype_table) > 0:
                    for tr in genotype_table[0].find_all('tr'):
                        for td in tr.find_all('td'):
                            if '#ff8080' in str(td):#if the color is red, its been determined to be a bad trait
                                variation_data.append('bad')
                            if '#80ff80' in str(td): #if the color is green, its been determined to be a good trait
                                variation_data.append('good')
                            if '#ffffff' in str(td):
                                variation_data.append('neutral') #if the color is white, it a neutral trait
                            variation_data.append(td.text.rstrip())#append alleles for mutation

                rsid_data[rsid] = np.array(variation_data) #use np array for ram constraints
                if len(rsid_data) % 100 == 0:
                    print(len(rsid_data))
        except Exception as e:
            print(e)
            print(url)
            
    
    def split_urls(rsid_urls) -> list:
        n=10000 
        split_urls = [rsid_urls[i * n:(i + 1) * n] for i in range((len(rsid_urls) + n - 1) // n )]  
        return split_urls
    
    def get_data():
        split_url = split_urls(rsid_urls)
        #for i in range(len(split_url)):
        with BoundedThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                for url in split_url[0]:
                    executor.submit(fetch,*(session,url))
        with open('crawl_result0.pkl', 'wb') as handle:
            pkl.dump(rsid_data, handle, protocol=pkl.HIGHEST_PROTOCOL)
                
    get_data()

  

    
    

    

links = get_rsid_links()
crawl(links)
