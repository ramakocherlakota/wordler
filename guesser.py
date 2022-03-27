import mysql.connector
import sys

cnx = mysql.connector.connect(user='wordle', password='',
                              host='127.0.0.1',
                              database='wordle')

subquery = ""

scores_table = "all_scores"

if len(sys.argv) > 1:
    subqueries = []
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        (guess, score) = arg.split("=")
        subqueries.append(f"answer in (select answer from {scores_table} where guess='{guess}' and score='{score}')")
        subqueries.append(f"guess in (select answer from {scores_table} where guess='{guess}' and score='{score}')")
    subquery = "where " + " and ".join(subqueries)
    
query = f"select guess, sum(c * log(c) / log(2)) / sum(c) as h from (select guess, score, count(*) as c from {scores_table} {subquery} group by 1, 2) as t1 group by 1 order by 2 limit 5"

print(query)

cursor = cnx.cursor()

cursor.execute(query)

for (guess, h) in cursor:
    print(f"{guess} {h}")

cnx.close()
