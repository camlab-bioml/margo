import pandas as pd

df = pd.read_csv("marker_database/panglao_db.csv")
t = list(set(df["tissue"]))
t = t[1:]
t.sort()
print(t)
