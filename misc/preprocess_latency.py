import pandas as pd



df = pd.read_csv("api/cloudping/latency2.csv", index_col=None, header=None)
df = df.applymap(lambda x: x.replace(".00", ""))
print(df)

cols = df.iloc[:,0]
df = df.iloc[:, 1:]
df.columns = cols

df.to_csv("api/cloudping/latency3.csv", index=False)