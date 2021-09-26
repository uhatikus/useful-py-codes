import requests
from bs4 import BeautifulSoup as bs
import csv
import time

email = ''
password = ''
headers={"Referer":"https://m.vk.com/login?role=fast&to=&s=1&m=1&email="+email
,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
payload = {'email': email,'pass': password}

session = requests.Session()
page = session.get('https://m.vk.com/login')
soup = bs(page.content,'lxml')
url = soup.find('form')['action']
p = session.post(url,data=payload,headers=headers)


def date(day, month, year):
    return str(day) + "." + str(month) + "." + str(year)

def process(idvk, data, noyear, nobd, errorid, c=1):
    html = session.get('https://vk.com/' + idvk).text
    lines = html.split("\n")
    flag = True
    day = 0
    month = 0
    year = 10000
    id = 0
    name = ""
    surname = ""
    for line in lines:
        try:
            if '<title>' in line:
                name = (line.split('>')[1]).split("<")[0]
                surname = name.split(" ")[1]
                name = name.split(" ")[0]
            if 'bday]=' in line:
                flag = False
                useful = line.split('bday]=')[1]
                lst = useful.split('&')
                day = lst[0]
                month_line = lst[1]
                month = (month_line.split('bmonth]=')[1]).split('"')[0]
                if len(lst) > 2:
                    if "byear]=" in lst[2]:
                        year_line = lst[2]
                        year = (year_line.split('byear]=')[1]).split('"')[0]
                    else:
                        noyear.append(idvk)
                else:
                    noyear.append(idvk)
            if '&id=' in line:
                id = ((line.split('&id=')[1]).split('"')[0]).split("&")[0]
        except:
            errorid.append(idvk)
            print("ERROR" + idvk + " " + line)
    data.append([name, surname, date(day, month, year), id])
    if flag:
        nobd.append(idvk)





data = []
noyear = []
nobd = []
errorid = []
f = open("ids.txt")
for i in range(65):
    time.sleep(2)
    line = f.readline()[:-1]
    print(line)
    id_ = line
    process(id_, data, noyear, nobd, errorid)
    print(data)
    print(noyear)
    print(nobd)
    print(errorid)

with open("resultFinal.csv", 'w') as outcsv:
    # configure writer to write standard csv file
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for item in data:
        # Write item to outcsv
        writer.writerow([item[0], item[1], item[2], item[3]])



#/about?lst=100005270464496%3A100006967209113%3A1535726315&section=contact-info