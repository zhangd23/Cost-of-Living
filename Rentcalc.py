#! python3
# Python project - scrape data from Rent.com 

import requests, csv, bs4, sys, re, math

def ziplookup(zipcode):             # Looks up zipcode and finds all results
    listBeds = []                   # Calculates urls to scrape
    listCosts = []                  # Calls function to scrape urls

    print('Looking up rent data in area code ' + ' '.join(zipcode)+'...')
    res = requests.get('http://www.rent.com/zip-' + ' '.join(zipcode))
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('span', class_='total-listings-count')
    display_results = int(results[0].getText())

    for i in range(1, math.ceil(display_results/20)+1):
        url = 'http://www.rent.com/zip-'+' '.join(zipcode)+'/page='+' '.join(str(i))
        zipscrape(url, listBeds, listCosts)
        
    listBeds = listBeds[1::2]
    
    for i in range (0, len(listBeds)):
        beds, cost = formatting(listBeds[i].getText(), listCosts[i].getText())
        costpertenant = costper(beds, cost)
        f.writerow([beds, cost, costpertenant])

def zipscrape(address, beds, cost):
    res = requests.get(address)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    price = soup.find_all('p', class_='prop-rent bullet-separator strong')
    bedcount = soup.find_all('span', class_='prop-beds bullet-separator')

    beds += bedcount
    cost += price
    return beds, cost

def formatting(bedno, priceno):         #Uses regular expressions to format list
    bedRegex = re.compile(r'\d|Studio')
    fbed = bedRegex.findall(bedno)
    priceRegex = re.compile(r'\d{3,5}')
    fprice = priceRegex.findall(priceno)
    return fbed, fprice

def costper(bedno, priceno):
    if len(bedno)&len(priceno)==1:
        for i in bedno:
            maxbeds = 1
            if i.isdigit():
                bednumber = int(i)
                if bednumber > maxbeds:
                    maxbeds = bednumber
        priceper = int(priceno[0])/maxbeds
        return priceper
    else:
        return "NA"

def scrape(zipcode):
    ziplookup(zipcode)   
    print('Finished gathering rent information in area code '+' '.join(zipcode))
    
f = csv.writer(open("Rent Information.csv", "w", newline=''))
f.writerow(["Beds", "Price", "Price per tenant"])

zip1 = sys.argv[1:2]
scrape(zip1)
