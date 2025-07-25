import sqlite3
import pandas as pd

conn = sqlite3.connect("cartoes.db")
df = pd.read_sql("SELECT * FROM cartoes_validos", conn)
print(df)
conn.close()
