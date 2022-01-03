import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words={'english'})

def process_fact_text(fact_text):
    processed_facts = ""
    for line in fact_text.splitlines():
        # print("testt", line)
        if len(processed_facts) > 2000:
            break

        if sum(c.isalpha() for c in line) < 30 or not any(c.islower() for c in line):
            continue

        processed_facts += line + "\n"

    return processed_facts



filename = "../datasets/data_confonet_2020.csv"
df = pd.read_csv(filename)

facts_list = []
for index, row in df.iterrows():
    processed_fact = process_fact_text(row['Fact Text'])

    if len(facts_list) > 0 and processed_fact == facts_list[-1]:
        continue
    
    facts_list.append(processed_fact)

X = vectorizer.fit_transform(facts_list)