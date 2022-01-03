import pandas as pd
import random

filename = "data_confonet_2020.csv"
# n = sum(1 for line in open('data_confonet_2020.csv', encoding="utf8")) - 1 #number of records in file (excludes header)
# s = 300 #desired sample size
# skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
# df = pandas.read_csv(filename, skiprows=skip)


df = pd.read_csv(filename)

df_elements = df.sample(n=300)
df_rest = df.loc[~df.index.isin(df_elements.index)]

df1 = df_elements.iloc[:100,:]
df2 = df_elements.iloc[100:200,:]
df3 = df_elements.iloc[200:,:]

# print(n)
print(df_elements.shape)

df1.to_csv("test1.csv", encoding='utf-8-sig')
df2.to_csv("test2.csv", encoding='utf-8-sig')
df3.to_csv("test3.csv", encoding='utf-8-sig')
df_rest.to_csv("rest.csv", encoding="utf-8-sig")
# import cs

# file = open('data_confonet_2020.csv', encoding="utf8")

# csvreader = csv.reader(file)
# header = next(csvreader)
# print(header)