import mwclient
from mwclient import Site
import numpy as np
from os import path
import pickle as pkl

#get all documented snps from snpedia, writes pickle if its the first run
def get_documented_snps() -> np.ndarray:
    if not path.exists("snps.pkl"):#checks if already pulled snp data
        snp_array = np.empty(1) #empty numpy array
        site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path

        for i, page in enumerate(site.Categories['Is_a_snp']):#iterate through all SNPs on SNPedia
            snp_array = np.append(snp_array, str(page.name).lower())#append to array
            if i % 10000 == 0: #there are about 100000 snps, 10000 would be 10 percent of total
                print(i / 1000, " percent complete") #display estimated percentage complete
        print("100 percent complete, writing pkl")
        file = open("snps.pkl", "wb")
        pkl.dump(snp_array, file)
        file.close()
    #if data has already been retrived, load into np array
    else:
        print("data already saved, loading into array")
        snp_array = np.load("snps.pkl", allow_pickle=True)
    return snp_array #return np array with complete SNP data


#transform genome txt data to dict for processing
def read_your_data() -> dict:
    print("Processing the raw data.")
    genotypes = {} #dict where genotypes and alleles will be stored
    raw_data = open('raw.txt', 'r')#load raw data from 23andme txt file
    lines = raw_data.readlines()#line of the raw data, we only need rsid and genotype
    for line in lines:
        if line[0] != '#': #skip documentation in the raw data
            split_line = line.split()
            genotypes[split_line[0]] = split_line[3]
    return genotypes

def process_your_data(your_data, documented_SNPs) -> list:
    your_studied_genes = []
    print(len(documented_SNPs))
    print(len(your_data))
    for SNP in documented_SNPs:
        if str(SNP) in your_data:
            your_studied_genes.append(SNP)
    return your_studied_genes

documented_SNPs = get_documented_snps()
your_data = read_your_data() 

your_studied_genes = process_your_data(your_data, documented_SNPs)

print(len(your_studied_genes))

