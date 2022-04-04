import mysql.connector

guess_guess_scores = "scores"

class Wordler:
    def __init__(self, guess_scores=[], scores_table="scores", hard_mode=False, debug=False):
        self.guess_scores = guess_scores
        self.scores_table = scores_table
        self.hard_mode = hard_mode
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
            
    def add_guess(self, guess, score):
        self.guess_scores.append([guess, score])

    def get_score(self, target, guess):
        cursor = self.query(f"select score, 0 from {self.scores_table} where guess='{guess}' and answer='{target}'")
        for (score, ignore) in cursor:
            return score

    def unique_solution(self):
        subqueries = []
        subquery = ""
        i = 0
        for guess_score in self.guess_scores:
            (guess, score) = guess_score
            if i > 0:
                subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
            else:
                subqueries.append(f"guess='{guess}' and score='{score}'")            
            i = i + 1
        subquery =   " and ".join(subqueries)
        sql = f"select count(*) as c, min(answer) from {self.scores_table} where {subquery} "
        csr = self.query(sql)
        for (c, answer) in csr:
            if c == 1:
                return (answer, None)
            else:
                return False

    def conditional_entropy(self, guess, score):
        sql = f"select log(count(*))/log(2) as h, 0 from {self.scores_table} where guess='{guess}' and score='{score}' "
        csr = self.query(sql)
        for (h, ignore) in csr:
            return h

    def next_guess(self):
        unique_sol = self.unique_solution()
        if unique_sol:
            return unique_sol
        subqueries = []
        subquery = ""
        hard_mode_subqueries = []
        hard_mode_subquery = ""
        for guess_score in self.guess_scores:
            (guess, score) = guess_score
            subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
            if self.hard_mode:
                hard_mode_subqueries.append(f"g.guess in (select answer  from {guess_guess_scores} where '{guess}'= guess and '{score}' = score)")
        subquery =  " and " + " and ".join(subqueries)
        if self.hard_mode:
            hard_mode_subquery = " and " + " and ".join(hard_mode_subqueries)
        query = f"select guess, sum(c * log(c) / log(2)) / sum(c) as h from (select g.guess, score, count(*) as c from {self.scores_table} a, guesses g where a.guess = g.guess {subquery} {hard_mode_subquery} group by 1, 2) as t1  group by 1 order by 2, 1 limit 1"
        csr = self.query(query)
        retval = None
        for (guess, entropy) in csr:
            retval = (guess, entropy)
        return retval
