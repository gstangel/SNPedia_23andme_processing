
import mwclient
def print_catagories() -> list:
    print("Getting all unique rsID links...")
    site = mwclient.Site('bots.snpedia.com', path='/')#SNPedia site path
    for catagory in site.Categories['Topic']:
        print(catagory.text())
print_catagories()