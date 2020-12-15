import mwclient
from os import path
import pickle as pkl
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from os import path

#uses mwclient to pull only the unique rsids from SNPedia (~110k individual rsids)
#The rsid number is a unique label ("rs" followed by a number) used by researchers and databases to identify a specific SNP (Single Nucleotide Polymorphism)
def get_rsids() -> list:
    if not path.exists("rsid_list.pkl"):
        print("Getting all unique SNP's...")
        site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path
        snps = [snp.name.lower() for snp in site.Categories['Is_a_snp']]#create a list of all snps stored in site object, mwclient makes this easy
        with open('rsid_list.pkl', 'wb') as file:
            pkl.dump(snps, file)
        return snps
    else:
        with open('rsid_list.pkl', 'rb') as file:
            snps = pkl.load(file)
        return snps

#mwclient supports pulling each rsid's associated data, but much slower than threaded requests 
#returns a dict of all the data for each rsid, uses BeautifulSoup to extract most relevant data
def get_rsid_data(snp_names) -> dict:
    base_url = "https://snpedia.com/index.php/"
    urls = [base_url + snp for snp in snp_names] #create list of all rsid's cooresponding link on SNPedia using the base_url
    rsid_data = {} #where the resulting data will be stored, in the form of nested dictionaries
    print("getting data")
    #this function is used to create asyncernous requests
    def make_request(url):
        genotypes = {}

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        rsid_name = soup.find(id='firstHeading') #ex: "rs6152"
        #rsid_genotypes = soup.find(id= 'sortable smwtable jquery-tablesorter')
        #print(rsid_genotypes.text)
        print(rsid_name.text)

    processes = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        for url in urls:
            processes.append(executor.submit(make_request, url))

    for task in as_completed(processes):
        print(task.result())



get_rsid_data(get_rsids())
