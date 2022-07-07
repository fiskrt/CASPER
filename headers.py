import pandas as pd

df = pd.read_csv("../electricity_map/US-CAL-CISO.csv")

for c in df:
    print(f'"{c}",')
