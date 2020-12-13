import mwclient
import numpy as np
from os import path
import pickle as pkl
from time import sleep

#get all documented snps from snpedia, writes pickle if its the first run.
#this data is used to extract keywords to create gene classifications
#first run took about 4 hours to make requests for all 100k+ genes on SNPedia.
def get_documented_snps() -> np.ndarray:
    if not path.exists("snps.pkl"):#checks if already pulled snp data
        SNP_dict = {}
        site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path

        for i, page in enumerate(site.Categories['Is_a_snp']):#iterate through all SNPs on SNPedia
            print(page.text())
            SNP_dict[page.name] = page.text(cache=False)
            if i % 1000 == 0: #there are about 100000 snps, 1000 would be 1 percent of total
                print(i/1000, " Percent done") #display estimated percentage

        file = open("snps.pkl", "wb")#save the dict as a pickle for processing in other functions
        pkl.dump(SNP_dict, file,protocol=pkl.HIGHEST_PROTOCOL)
        file.close()
    #if data has already been retrived, load into dict from pickle
    else:
        print("data already saved, loading into program")
        with open('snps.pkl', 'rb') as data:
            SNP_dict = pkl.load(data)
    return SNP_dict #return np array with complete SNP data



#transform genome txt data to dict for processing
def read_your_data() -> dict:
    print("Processing the raw data.")
    genotypes = {} #dict where genotypes and alleles will be stored
    raw_data = open('raw.txt', 'r')#load raw data from 23andme txt file
    lines = raw_data.readlines()
    for line in lines: #line of the raw data, we only need rsid and genotype
        if line[0] != '#': #skip documentation in the raw data
            split_line = line.split()#we only need rsid and genotype
            genotypes[split_line[0]] = split_line[3] #make dict key and value
    return genotypes

#finds SNPS that are both on SNPedia and in your genome
def get_common_SNPs(your_data, documented_snps) -> list:
    return [snp for snp in documented_snps if snp.lower() in your_data]



documented_SNPs = get_documented_snps()

your_data = read_your_data()


your_studied_genes = get_common_SNPs(your_data, documented_SNPs)


