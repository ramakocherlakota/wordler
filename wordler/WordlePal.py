import mysql.connector

class WordlePal:

    def __init__(self, scores_table="scores", starting_word="raise", debug=False, hard_mode=False):
        self.scores_table = scores_table
        self.hard_mode = hard_mode 
        self.starting_word = starting_word 
        self.debug = debug
        self.dbh = None

    def db(self):
        if self.dbh is None:
            self.dbh = mysql.connector.connect(user='wordle', password='',
                                               host='127.0.0.1',
                                               database='wordle')
        return self.dbh

    def query(self, sql):
        if self.debug:
            print(sql)
        cursor = self.db().cursor()
        cursor.execute(sql)
        return cursor

    def guess_table(self, name, guesses, responses, temporary="temporary"):
        wheres = ["a.guess = g.guess"]
        for i in range(len(guesses)):
            wheres.append(f"answer in (select answer from {self.scores_table} where guess = '{guesses[i]}' and score = '{responses[i]}')")
            if self.hard_mode:
                wheres.append(f"g.guess in (select answer from {self.scores_table} where '{guesses[i]}'= guess and '{responses[i]}' = score)")
        where_clause = "where " + " and ".join(wheres)
        sql = f"select g.guess, score, count(*) as c from {self.scores_table} a, guesses g {where_clause} group by 1, 2"
        self.query(f"drop {temporary} table if exists {name}")
        self.query(f"create {temporary} table {name} as {sql}")
        self.query(f"alter table {name} add primary key(guess, score), add key(score, guess)")

    def guess(self, guesses, responses) :
        unique_sol = self.unique_solution(guesses, responses)
        if unique_sol:
            return unique_sol
        else:
            self.guess_table("t1", guesses, responses)
            return self.min_entropy("t1")

    def get_score(self, target, guess):
        cursor = self.query(f"select score, 0 from {self.scores_table} where guess='{guess}' and answer='{target}'")
        for (score, ignore) in cursor:
            return score

    def unique_solution(self, guesses, responses):
        subqueries = []
        subquery = ""
        if len(guesses) == 0:
            return False
        for i in range(len(guesses)):
            guess = guesses[i]
            score = responses[i]
            if i > 0:
                subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
            else:
                subqueries.append(f"guess='{guess}' and score='{score}'")            
                subquery =   " and ".join(subqueries)
                sql = f"select count(*) as c, min(answer) from {self.scores_table} where {subquery} "
                csr = self.query(sql)
        for (c, answer) in csr:
            if c == 1:
                return (answer, None)
            else:
                return False

    def min_entropy(self, name):
        csr = self.query(f"select guess, sum(c * log(c) / log(2)) / sum(c) as h from {name} group by 1 order by 2, 1 limit 1")
        for (guess, entropy) in csr:
            return (guess, entropy)

    def conditional_entropy(self, guess, score):
        sql = f"select log(count(*))/log(2) as h, 0 from {self.scores_table} where guess='{guess}' and score='{score}' "
        csr = self.query(sql)
        for (h, ignore) in csr:
            return h

    def solve(self, target):
        guess = self.starting_word
        score = self.get_score(target, guess)
        entropy = self.conditional_entropy(guess, score)
        
        guesses = [guess]
        scores = [score]
        entropies = [entropy]

        while True:
            (guess, entropy) = self.guess(guesses, scores)
            score = self.get_score(target, guess)
            guesses.append(guess)
            scores.append(score)
            entropies.append(entropy)
            print([guesses, scores, entropies])
            if score == "BBBBB" or entropy is None:
                break
        return [guesses, scores, entropies]
        
