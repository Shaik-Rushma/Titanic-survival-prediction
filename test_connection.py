
from db import run_query

df = run_query("""
    SELECT COUNT(*) AS total_passengers
    FROM titanic_project.passengers;
""")

print(df)
