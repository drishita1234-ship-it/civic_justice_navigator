import pandas as pd

df = pd.read_csv("data/keys/type_name_key.csv")
print(df.head())
print("\nColumns:", df.columns)
print("\nUnique rows:", df.shape)