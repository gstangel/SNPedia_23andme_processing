import mwclient
from os import path
import pickle as pkl
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from os import path
import lxml

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
def crawl(rsid_links) -> dict:
    rsid_data = {} #where the resulting data will be stored, in the form of nested dictionaries

    #this function is used to create syncernous requests
    def make_request(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        rsid = soup.find(id='firstHeading').text #ex: "rs6152"

        genotype_table = soup.find_all('table', attrs={'class': 'sortable'})

        variation_data = [] 
        #pulls relevant data from the tables on SNPedia
        for tr in genotype_table[0].find_all('tr'):
            for td in tr.find_all('td'):
                if '#ff8080' in str(td):#if the color is red, its been determined to be a bad trait
                    variation_data.append('bad')
                if '#80ff80' in str(td):#if the color is green, its been determined to be a good trait
                    variation_data.append('good')
                if '#ffffff' in str(td):
                    variation_data.append('neutral')#if the color is white, it a neutral trait
                variation_data.append(td.text.rstrip())

        rsid_data[rsid] = variation_data
        print(rsid)

    #make_request("https://www.snpedia.com/index.php/i3003401")

    processes = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        for url in rsid_links:
            processes.append(executor.submit(make_request, url))
    with open('crawl_result.pkl', 'wb') as handle:
        pkl.dump(rsid_data, handle, protocol=pkl.HIGHEST_PROTOCOL)
    

links = get_rsid_links()
crawl(links)
