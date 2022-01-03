import requests
from bs4 import BeautifulSoup

URL = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do?method=GetJudgement&caseidin=0%2F0%2FFA%2F579%2F2012&dtofhearing=2020-01-03"

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
        last_paras = para.text.replace(u'\xa0', " ") + "\n" + last_paras
        # if para.text != u'\xa0':    # check for &nbsp
        #     para_count += 1
        #     para_text = para.text.strip()
        #     last_paras = para_text + " " + last_paras
        #     if len(para_text) > MIN_PARA_SIZE or para_count == 3:
        #         break

    # if len(last_paras) < MIN_PARA_SIZE:
    #     for para in reversed(case_order.find_all("h1", attrs={'align': None})):
    #         if para.text != u'\xa0':    # check for &nbsp
    #             para_count += 1
    #             para_text = para.text.strip()
    #             last_paras = para_text + " " + last_paras
    #             if len(para_text) > MIN_PARA_SIZE or para_count == 3:
    #                 break
            
    return last_paras

print(parse_case(URL))