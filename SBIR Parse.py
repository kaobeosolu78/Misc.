import bs4
import requests
import pickle
import re

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

companies = []
for k in range(4):
    SBIR_comp_req = requests.get("https://www.sbir.gov/sbirsearch/firm/all?fDOTtitle=&duns=&city=&zip=&fDOTstate%5B%5D=CA&fDOTstate%5B%5D=CO&fDOTstate%5B%5D=FL&fDOTstate%5B%5D=MI&fDOTstate%5B%5D=PA&fDOTstate%5B%5D=UT&awardcount%5B%5D=100_award&awardcount%5B%5D=101_award&page={}".format(k+1))
    SBIR_soup = bs4.BeautifulSoup(SBIR_comp_req.text,"html.parser")

    table = ((SBIR_soup.find("table")))
    counter = 0
    products = {}

    for tr in table.findAll("tr"):
        prod = []
        count = 0
        counter += 1

        for td in tr.findAll("td"):
            count += 1
            if count == 1:
                prod.append(td.find("a").get("href"))
                prod.append(td.text)
            if (count > 1 and count < 5):
                prod.append(td.text)

            if count == 5 and td.find("a") != None:
                prod.append(td.find("a").get("href"))

        companies.append(prod)

grants = {}

for company in companies:
    temp = 0
    boomba = {}
    name = []
    prices = []
    summ_req = requests.get("https://www.sbir.gov{}".format(company[0]))
    summ_soup = bs4.BeautifulSoup(summ_req.text,"html.parser")
    page = (len(summ_soup.find(id="sbir-search-result-pager").findAll("li")))
    print (page)
    for pag in range(page):

        sum_req = requests.get("https://www.sbir.gov{}?page={}".format(company[0],pag))
        sum_soup = bs4.BeautifulSoup(sum_req.text, "html.parser")
        div = ((sum_soup.findAll(class_="firm-details-content"))[1])

        for d in div.findAll(class_="title"):
            name.append(d.text)
        for di in div.findAll(class_="search-result-sub-title"):
            temp += (float((((di.text)[32:len(di.text)-20])).replace(",","")))
            prices.append(float((((di.text)[32:len(di.text)-20])).replace(",","")))
        company.append(temp)

        nices = []
        for k in range(len(prices)):
            nices.append([name[k],prices[k]])
        grants[company[1]] = nices

    print (grants)

pickle_out = open("grants.pkl", 'wb')
pickle.dump((grants), pickle_out, pickle.HIGHEST_PROTOCOL)
pickle_out.close()
pickle_out = open("company_guap.pkl", 'wb')
pickle.dump((companies), pickle_out, pickle.HIGHEST_PROTOCOL)
pickle_out.close()

company_guap = load_obj("company_guap")
tag = []


for company in company_guap:
    try:
        int(company[5])
        tag.append([company[1],company[5]])
    except:
        tag.append([company[1],company[6]])

sort = []
[sort.append(t[1]) for t in tag]
sorted = []
while len(sort) != 0:

    for t in tag:
        if len(sort) == 0:
            break
        max_val = (max(sort))
        if t[1] == max_val:
            sorted.append(t)
            for s in range(len(sort)):
                if max_val == sort[s]:
                    del(sort[s])
                    break
        else:
            continue
comp = []
for bort in sorted:
    [comp.append(c) for c in company_guap if bort[0] == c[1]]

print (comp)

#grants = load_obj("grants")

#grantmo = re.compile(r"")
#interest = []
#for co in comp[:30]:
#    for gran in (grants[co[1]])[0]:
#        if grantmo.search(gran) != None:
#            interest.append([co[1],grants[co[1]]])

