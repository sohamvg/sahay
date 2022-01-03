import requests
from bs4 import BeautifulSoup
import csv

MIN_PARA_SIZE = 80

loss_keywords = ["dismissed", "dismissed.", "dismissed,", "op is not entitled to", "opposite party is not entitled to"]

win_keywords = ["complaint is allowed", "petition is allowed", "appeal is allowed", "op shall refund", "opposite party shall refund",
"op shall pay", "opposite party shall pay", "op is entitled to pay", "opposite party is entitled to pay", "op is entitled to refund",
"opposite party is entitled to", "to be paid to the complainant"]

neutral_keywords = ["disposed", "disposed.", "order is being passed", "order is passed"]

def parse_case(url):
    case_page = requests.get(url)
    case_soup = BeautifulSoup(case_page.content, "html.parser")
    case_orders = case_soup.find_all("table", attrs={'width':'100%', 'style': None})
    
    fact_text = ""
    judgement_text = ""
    case_judgement = 2

    if len(case_orders) < 2:
        return fact_text

    is_judgement = False

    case_header = ""
    for i in range(2, len(case_orders) - 3):
        case_header += case_orders[i].text + "\n"

    case_order = case_orders[-2].find('td')

    total_tags = 0
    paras = []
    for tag in case_order.find_all():
        if tag.name == "p" or tag.name == "h1":
            para_text = tag.text.strip().replace(u'\xa0', " ")
            if para_text and not para_text.isspace():
                paras.append(para_text)
                total_tags += 1

    tag_count = 0
    for para_text in paras:
        tag_count += 1
        para_text_low = para_text.lower()
        if float(tag_count / total_tags) > 0.5:
            if any(x in para_text_low for x in loss_keywords):
                if case_judgement == 1:
                    case_judgement = 2
                else:
                    case_judgement = 0
                is_judgement = True
                
            if any(x in para_text_low for x in win_keywords):
                if case_judgement == 0:
                    case_judgement = 2
                else:
                    case_judgement = 1
                is_judgement = True

            if any(x in para_text_low for x in neutral_keywords):
                is_judgement = True

        if is_judgement:
            judgement_text += para_text + "\n"
        else:
            fact_text += para_text + "\n"


    if len(judgement_text) < MIN_PARA_SIZE:
        for para in reversed(case_order.find_all("p", attrs={'align': None})):
            judgement_text = para.text.replace(u'\xa0', " ") + "\n" + judgement_text
            if len(judgement_text) > MIN_PARA_SIZE:
                break

    if len(judgement_text) < MIN_PARA_SIZE:
        for para in reversed(case_order.find_all("h1", attrs={'align': None})):
            judgement_text = para.text.replace(u'\xa0', " ") + "\n" + judgement_text
            if len(judgement_text) > MIN_PARA_SIZE:
                break
            
    return case_header, fact_text, judgement_text, case_judgement


header = ['Case No.', 'Date of Filling', 'Date of Disposal', 'Case Header', 'Fact Text', 'Judgement Text', 'Judgement']
final_data = []
final_data.append(header)

case_statistics = [0,0,0]

for page_no in range(1, 90):
    URL = " http://cms.nic.in/ncdrcusersWeb/servlet/search.GetHtml?method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&method=GetHtml&stid=0&did=0&stdate=01/01/2020&enddate=31/12/2020&par1=NotApp&fmt=T&searchOpt=jud&filterBy=on&dateByPar=dtod&start=" + str(page_no) + "&jsrc=FULL&searchBy=6" # url for search by date b/w 01/01/2020 & 30/09/2020

    print(page_no, "---------")

    page = requests.get(url = URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(id="one")
    for case in results[1:]:
        case_info = case.find_all("td")
        case_number = case_info[0].text.strip()
        case_url = "http://cms.nic.in/ncdrcusersWeb/" + case_info[0].find("a")['href']

        parse_result = parse_case(case_url)
        if parse_result:
            case_header, fact_text, judgement_text, judgement = parse_result
            if judgement_text != "" and fact_text != "" and len(fact_text) < 20000 and len(case_header) < 20000 and len(judgement_text) < 20000:
                date_of_filling = case_info[5].text
                date_of_disposal = case_info[6].text

                if judgement_text != final_data[-1][5]:
                    row = [case_number, date_of_filling, date_of_disposal, case_header, fact_text, judgement_text, judgement]
                    case_statistics[int(judgement)] += 1
                    final_data.append(row)


with open('data_v2.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_data)

print("---case statistics----")
print(case_statistics)
