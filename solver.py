import mysql.connector
import sys

cnx = mysql.connector.connect(user='wordle', password='',
                              host='127.0.0.1',
                              database='wordle')

scores_table = "scores"

def get_score(target, guess):
    query = f"select score, 0 from {scores_table} where guess='{guess}' and answer='{target}'"
    cursor = cnx.cursor()
    cursor.execute(query)
    for (score, ignore) in cursor:
        return score

def next_guess(pairs):
    subquery = ""
    subqueries = []
    for pair in pairs:
        guess, score = pair
        subqueries.append(f"answer in (select answer from {scores_table} where guess='{guess}' and score='{score}')")
        subqueries.append(f"guess in (select answer from {scores_table} where guess='{guess}' and score='{score}')")
    subquery = "where " + " and ".join(subqueries)
    query = f"select guess, sum(c * log(c) / log(2)) / sum(c) as h from (select guess, score, count(*) as c from {scores_table} {subquery} group by 1, 2) as t1 group by 1 order by 2 limit 1"
    cursor = cnx.cursor()
    cursor.execute(query)
    for (guess, h) in cursor:
        return guess

target = sys.argv[1]

if not get_score(target, target):
    print(target + " is not a valid answer")
    exit(1)

guess_score_pairs = []
guess = "raise"
n = 1
while guess != target:
    score = get_score(target, guess)
    print(f"{guess} -> {score}")
    guess_score_pairs.append([guess, score])    
    guess = next_guess(guess_score_pairs)
    n = n + 1

print(f"{target} -> BBBBB")  
print(f"{n} guesses!")

cnx.close()
