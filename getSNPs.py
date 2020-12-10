import mwclient
from mwclient import Site
import numpy as np


def get_snp_data():
    snp_array = np.empty(1)
    site = mwclient.Site('bots.snpedia.com', path='/')

    for i, page in enumerate(site.Categories['Is_a_snp']):
        snp_array = np.append(snp_array, page.name)
        print(i)

    return snp_array
snp_array = get_snp_data()

for snp in snp_array:
    print(snp)