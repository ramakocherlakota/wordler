import mysql.connector

class WordlePal:

    def __init__(self, scores_table="scores", starting_word="raise", debug=False, hard_mode=False, host="127.0.0.1", username="wordle", password="", database="wordle", keep_temporary=False):
        self.scores_table = scores_table
        self.hard_mode = hard_mode 
        self.starting_word = starting_word 
        self.debug = debug
        self.dbh = None
        self.username = username
        self.password = password
        self.database = database
        self.host = host
        if keep_temporary:
            self.temporary = ""
        else:
            self.temporary = "temporary"

    def db(self):
        if self.dbh is None:
            self.dbh = mysql.connector.connect(user=self.username, password=self.password,
                                               host=self.host,
                                               database=self.database)
        return self.dbh

    def query(self, sql, title=None):
        if self.debug:
            if title is not None:
                print(f"{title}: {sql}")
        cursor = self.db().cursor()
        cursor.execute(sql)
        return cursor

    def guess_table(self, name, guesses, responses):
        wheres = ["a.guess = g.guess"]
        for i in range(len(guesses)):
            wheres.append(f"answer in (select answer from {self.scores_table} where guess = '{guesses[i]}' and score = '{responses[i]}')")
            if self.hard_mode:
                wheres.append(f"g.guess in (select answer from {self.scores_table} where '{guesses[i]}'= guess and '{responses[i]}' = score)")
            else:
                wheres.append(f"g.guess != '{guesses[i]}'")
        where_clause = "where " + " and ".join(wheres)
        sql = f"select g.guess, score, count(*) as c from {self.scores_table} a, guesses g {where_clause} group by 1, 2"
        self.query(f"drop {self.temporary} table if exists {name}")
        self.query(f"create {self.temporary} table {name} as {sql}", "creating temp table")
        self.query(f"alter table {name} add primary key(guess, score), add key(score, guess)")

    def guess(self, guesses, responses) :
        (count, answer) = self.guessable_solution(guesses, responses)
        if count == 1:
            return [answer, None, 1]
        else:
            self.guess_table("t1", guesses, responses)
            return self.min_entropy("t1")

    def get_score(self, target, guess):
        cursor = self.query(f"select score, 0 from {self.scores_table} where guess='{guess}' and answer='{target}'", "computing score")
        for (score, ignore) in cursor:
            return score

    def guessable_solution(self, guesses, responses):
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
        csr = self.query(sql,  "guessable")
        for (c, answer) in csr:
            return (c, answer)

    def min_entropy(self, name):
        csr = self.query(f"select guess, sum(c * log(c) / log(2)) / sum(c) as h, sum(c) as total from {name} group by 1 order by 2, 1 limit 1", "min entropy")
        for (guess, entropy, count) in csr:
            return (guess, entropy, int(count))

    def conditional_entropy(self, guess, score):
        sql = f"select log(count(*))/log(2) as h, 0 from {self.scores_table} where guess='{guess}' and score='{score}' "
        csr = self.query(sql, "conditional entropy")
        for (h, ignore) in csr:
            return h

    def solve(self, target, max_iterations=20):
        guess = self.starting_word
        score = self.get_score(target, guess)
        entropy = self.conditional_entropy(guess, score)

        guesses = [guess]
        scores = [score]
        entropies = [entropy]
        counts = []

        iteration = 1
        while iteration != max_iterations:
            (guess, entropy, count) = self.guess(guesses, scores)
            score = self.get_score(target, guess)
            guesses.append(guess)
            scores.append(score)
            entropies.append(entropy)
            counts.append(count)
            if self.debug:
                print([guesses, scores, entropies, counts])
            if score == "BBBBB" or entropy is None:
                break
            iteration = iteration + 1
        return { "guesses": guesses, 
                 "scores": scores, 
                 "entropies": entropies, 
                 "counts": counts }
        
    def get_random_answer(self):
        csr = self.query("select answer, 0 from (select distinct(answer) from scores) as c order by rand() limit 1")
        for (answer, ignore) in csr:
            return answer
