import os
from bs4 import BeautifulSoup
import numpy as np
import pickle as pkl
from concurrent.futures import ProcessPoolExecutor
from bounded_pool_executor import BoundedProcessPoolExecutor, BoundedThreadPoolExecutor
rsid_data = {}

def get_variation_data(file):
    with open ('raw html/' + file, 'rb') as html:
        soup = BeautifulSoup(html, 'lxml')
        genotype_table = soup.find_all('table', attrs={'class': 'sortable'})
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

        rsid_data[str(file[0:-5])] = np.array(variation_data) #use np array for ram constraints
        if len(rsid_data) % 1000 == 0:
            print(len(rsid_data))
def get 
if __name__ == '__main__':
    for file in os.listdir('raw html/'):
        get_variation_data(file)

    with open('allele_data.pkl', 'wb') as handle:
            pkl.dump(rsid_data, handle, protocol=pkl.HIGHEST_PROTOCOL)