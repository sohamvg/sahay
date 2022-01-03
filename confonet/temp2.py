import requests
from bs4 import BeautifulSoup
from requests.api import head

URL = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do?method=GetJudgement&caseidin=0%2F0%2FFA%2F579%2F2012&dtofhearing=2020-01-03"

MIN_PARA_SIZE = 100
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

    header_text = ""
    print(len(case_orders))
    for i in range(2, len(case_orders) - 3):
        header_text += case_orders[i].text + "\n"

    case_order = case_orders[-2].find('td')

    total_tags = 0
    paras = []
    for tag in case_order.find_all():
        if tag.name == "p" or tag.name == "h1":
            para_text = tag.text.strip().replace(u'\xa0', " ")
            if para_text and not para_text.isspace():
                paras.append(para_text)
                total_tags += 1

    # for tag in case_order.find_all():
    #     if tag.name == "p" or tag.name == "h1":
    #         tag_count += 1
    #         para_text = tag.text.strip().replace(u'\xa0', " ")
    #         if not para_text.isspace():
    tag_count = 0
    for para_text in paras:
        tag_count += 1
        para_text_low = para_text.lower()
        # print("p", float(tag_count / total_tags), "[" + para_text + "]")
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
            


    return header_text, fact_text, judgement_text, case_judgement

parsed_case = parse_case(URL)

if parsed_case:
    header_text, fact, judgement, verdict = parsed_case


    print("--------header--------")
    print(header_text)

    print("--------facts--------")
    print(fact)

    print("-----judgements------")
    print(judgement)

    print(len(fact))

    print("-------verdict-------")
    print(verdict)
