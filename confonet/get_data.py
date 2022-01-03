import requests
from bs4 import BeautifulSoup
import csv

MIN_PARA_SIZE = 170

def parse_case(url):
    case_page = requests.get(url)
    case_soup = BeautifulSoup(case_page.content, "html.parser")
    case_orders = case_soup.find_all("table", attrs={'width':'100%', 'style': None})
    last_paras = ""
    if len(case_orders) < 2:
        return last_paras

    case_order = case_orders[-2].find('td')
    para_count = 0
    for para in reversed(case_order.find_all("p", attrs={'align': None})):
        if para.text != u'\xa0':    # check for &nbsp
            para_count += 1
            para_text = para.text.strip()
            last_paras = para_text + " " + last_paras
            if len(para_text) > MIN_PARA_SIZE or para_count == 3:
                break

    if len(last_paras) < MIN_PARA_SIZE:
        for para in reversed(case_order.find_all("h1", attrs={'align': None})):
            if para.text != u'\xa0':    # check for &nbsp
                para_count += 1
                para_text = para.text.strip()
                last_paras = para_text + " " + last_paras
                if len(para_text) > MIN_PARA_SIZE or para_count == 3:
                    break
            
    return last_paras

header = ['Case No.', 'Date of Filling', 'Date of Disposal', 'Case Verdict']
final_data = []
final_data.append(header)

for page_no in range(1, 86):
    URL = " http://cms.nic.in/ncdrcusersWeb/servlet/search.GetHtml?method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&stid=0&did=0&stdate=01/01/2020&enddate=31/12/2020&par1=NotApp&fmt=T&searchOpt=jud&filterBy=on&dateByPar=dtod&start=" + str(page_no) + "&jsrc=FULL&searchBy=6" # url for search by date b/w 01/01/2020 & 30/09/2020

    print(page_no, "---------")

    page = requests.get(url = URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(id="one")
    for case in results[1:]:
        case_info = case.find_all("td")
        case_number = case_info[0].text.strip()
        case_url = "http://cms.nic.in/ncdrcusersWeb/" + case_info[0].find("a")['href']
        case_last_para = parse_case(case_url)
        if case_last_para != "":
            date_of_filling = case_info[5].text
            date_of_disposal = case_info[6].text

            if case_last_para != final_data[-1][3]:
                row = [case_number, date_of_filling, date_of_disposal, case_last_para]
                final_data.append(row)


with open('data_1.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_data)
